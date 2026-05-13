#!/usr/bin/env python3
"""Upload local images to Notion and insert image blocks.

Requires a Notion integration token in NOTION_TOKEN or NOTION_API_KEY. The
integration must have access to the target page/block.

Example:
    upload_notion_images.py --page-id 35e2735ce8f981a0aa29eaab1e30eeae \
      /tmp/tracevla-figure.png --caption "TraceVLA overview" --cleanup

    upload_notion_images.py --page-id 35e2735ce8f981a0aa29eaab1e30eeae \
      --after-text "PointWorld predicts future 3D scene motion" \
      /tmp/pointworld-method.png --caption "PointWorld method overview"
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import uuid
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError


API_BASE = "https://api.notion.com/v1"
DEFAULT_VERSION = "2026-03-11"


def notion_token() -> str:
    token = os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_API_KEY")
    if not token:
        raise SystemExit("Set NOTION_TOKEN or NOTION_API_KEY before uploading images.")
    return token


def read_json(req: request.Request) -> dict:
    for attempt in range(3):
        try:
            with request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise SystemExit(f"Notion API error {exc.code}: {detail}") from exc
            time.sleep(2**attempt)
        except URLError as exc:
            if attempt == 2:
                raise SystemExit(f"Notion API connection error: {exc}") from exc
            time.sleep(2**attempt)
    raise SystemExit("Notion API request failed after retries.")


def api_json(method: str, url: str, token: str, version: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", version)
    req.add_header("Content-Type", "application/json")
    return read_json(req)


def create_upload(path: Path, token: str, version: str) -> dict:
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return api_json(
        "POST",
        f"{API_BASE}/file_uploads",
        token,
        version,
        {
            "mode": "single_part",
            "filename": path.name,
            "content_type": content_type,
        },
    )


def multipart_body(field: str, path: Path, content_type: str) -> tuple[bytes, str]:
    boundary = f"----notion-upload-{uuid.uuid4().hex}"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return head + path.read_bytes() + tail, boundary


def send_upload(upload_url: str, path: Path, token: str, version: str) -> dict:
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body, boundary = multipart_body("file", path, content_type)
    req = request.Request(upload_url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", version)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(body)))
    return read_json(req)


def rich_text_plain_text(items: list[dict]) -> str:
    return "".join(item.get("plain_text", "") for item in items)


def block_plain_text(block: dict) -> str:
    block_type = block.get("type")
    if not block_type:
        return ""
    data = block.get(block_type, {})
    text = rich_text_plain_text(data.get("rich_text", []))
    caption = rich_text_plain_text(data.get("caption", []))
    return "\n".join(part for part in (text, caption) if part)


def list_children(block_id: str, token: str, version: str) -> list[dict]:
    children: list[dict] = []
    start_cursor = None
    while True:
        url = f"{API_BASE}/blocks/{block_id}/children?page_size=100"
        if start_cursor:
            url += f"&start_cursor={start_cursor}"
        req = request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Notion-Version", version)
        data = read_json(req)
        children.extend(data.get("results", []))
        if not data.get("has_more"):
            return children
        start_cursor = data.get("next_cursor")


def find_anchor(parent_id: str, needle: str, token: str, version: str) -> tuple[str, str]:
    stack: list[tuple[str, list[dict]]] = [(parent_id, list_children(parent_id, token, version))]
    needle_folded = needle.casefold()
    while stack:
        current_parent_id, children = stack.pop()
        for block in children:
            if needle_folded in block_plain_text(block).casefold():
                return current_parent_id, block["id"]
            if block.get("has_children"):
                stack.append((block["id"], list_children(block["id"], token, version)))
    raise SystemExit(f"anchor text not found under target page/block: {needle!r}")


def image_block(upload_id: str, caption: str) -> dict:
    caption_rich_text = [{"type": "text", "text": {"content": caption}}] if caption else []
    return {
        "type": "image",
        "image": {
            "type": "file_upload",
            "file_upload": {"id": upload_id},
            "caption": caption_rich_text,
        },
    }


def append_image(
    block_id: str,
    upload_id: str,
    caption: str,
    token: str,
    version: str,
    after_block_id: str | None = None,
) -> dict:
    payload: dict = {"children": [image_block(upload_id, caption)]}
    if after_block_id:
        payload["position"] = {
            "type": "after_block",
            "after_block": {"id": after_block_id},
        }
    return api_json(
        "PATCH",
        f"{API_BASE}/blocks/{block_id}/children",
        token,
        version,
        payload,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", type=Path, nargs="+", help="Local image files")
    parser.add_argument("--page-id", "--block-id", dest="block_id", required=True, help="Target Notion page or block ID")
    parser.add_argument("--after-block-id", help="Insert each image after this existing child block instead of appending at the end")
    parser.add_argument("--after-text", help="Find the first block containing this text and insert images after it")
    parser.add_argument("--caption", default="", help="Caption to reuse for every uploaded image")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="Notion-Version header")
    parser.add_argument("--cleanup", action="store_true", help="Delete local image files after successful upload")
    args = parser.parse_args()

    token = notion_token()
    uploaded: list[dict[str, str]] = []
    target_block_id = args.block_id
    after_block_id = args.after_block_id

    if args.after_text:
        if after_block_id:
            raise SystemExit("Use only one of --after-block-id or --after-text.")
        target_block_id, after_block_id = find_anchor(args.block_id, args.after_text, token, args.version)

    for image in args.images:
        image = image.expanduser().resolve()
        if not image.is_file():
            raise SystemExit(f"not a file: {image}")

        created = create_upload(image, token, args.version)
        upload_id = created["id"]
        upload_url = created.get("upload_url") or f"{API_BASE}/file_uploads/{upload_id}/send"
        sent = send_upload(upload_url, image, token, args.version)
        if sent.get("status") != "uploaded":
            raise SystemExit(f"upload did not complete for {image}: {sent}")

        appended = append_image(target_block_id, upload_id, args.caption, token, args.version, after_block_id)
        image_block_id = ""
        if appended.get("results"):
            image_block_id = appended["results"][0].get("id", "")
        uploaded.append(
            {
                "file": str(image),
                "file_upload_id": upload_id,
                "image_block_id": image_block_id,
                "inserted_after": after_block_id or "",
            }
        )
        if image_block_id:
            after_block_id = image_block_id

        if args.cleanup:
            image.unlink()

    print(json.dumps({"uploaded": uploaded}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
