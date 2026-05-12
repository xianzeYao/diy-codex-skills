#!/usr/bin/env python3
"""Upload local images to Notion and insert image blocks.

Requires a Notion integration token in NOTION_TOKEN or NOTION_API_KEY. The
integration must have access to the target page/block.

Example:
    upload_notion_images.py --page-id 35e2735ce8f981a0aa29eaab1e30eeae \
      /tmp/tracevla-figure.png --caption "TraceVLA overview" --cleanup
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from urllib import request
from urllib.error import HTTPError


API_BASE = "https://api.notion.com/v1"
DEFAULT_VERSION = "2026-03-11"


def notion_token() -> str:
    token = os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_API_KEY")
    if not token:
        raise SystemExit("Set NOTION_TOKEN or NOTION_API_KEY before uploading images.")
    return token


def read_json(req: request.Request) -> dict:
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Notion API error {exc.code}: {detail}") from exc


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


def append_image(block_id: str, upload_id: str, caption: str, token: str, version: str) -> dict:
    caption_rich_text = [{"type": "text", "text": {"content": caption}}] if caption else []
    return api_json(
        "PATCH",
        f"{API_BASE}/blocks/{block_id}/children",
        token,
        version,
        {
            "children": [
                {
                    "type": "image",
                    "image": {
                        "type": "file_upload",
                        "file_upload": {"id": upload_id},
                        "caption": caption_rich_text,
                    },
                }
            ]
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", type=Path, nargs="+", help="Local image files")
    parser.add_argument("--page-id", "--block-id", dest="block_id", required=True, help="Target Notion page or block ID")
    parser.add_argument("--caption", default="", help="Caption to reuse for every uploaded image")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="Notion-Version header")
    parser.add_argument("--cleanup", action="store_true", help="Delete local image files after successful upload")
    args = parser.parse_args()

    token = notion_token()
    uploaded: list[dict[str, str]] = []

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

        append_image(args.block_id, upload_id, args.caption, token, args.version)
        uploaded.append({"file": str(image), "file_upload_id": upload_id})

        if args.cleanup:
            image.unlink()

    print(json.dumps({"uploaded": uploaded}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
