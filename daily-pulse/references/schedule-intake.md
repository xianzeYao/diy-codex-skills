# Schedule Intake

Use this when the user wants to learn a knowledge point, public course, paper list, technical route, routine, or recurring study plan.

## Principle

Do not require the user to provide a complete Schedule row. If they say "把 CS231n 加入 Schedule" or "我想学 SE(3)", start a short clarification loop and infer safe defaults.

## Minimum Needed

Create a Schedule row once these are clear:

- `名称`: what they want to learn.
- `类型`: 公开课, 知识点, 习惯, or 项目路线.
- `状态`: default to 进行中.
- `节奏`: default to 每周 if unknown.
- `下一步行动`: infer a first step if obvious; otherwise ask.

Optional fields can be left blank:

- 进度
- 下次推进
- 备注

## Question Strategy

Ask at most two short questions before creating a draft Schedule row. Prefer concrete choices.

Good questions:

- "这是公开课、知识点、技术路线，还是周期习惯？"
- "你希望按什么节奏推进：每天、工作日、每周，还是先不定？"
- "第一步要我帮你定，还是你已经知道下一步？"
- "有没有课程链接、repo、论文列表？有的话我放到备注里。"

If the user does not know the next action, create one:

- For a public course: `打开 syllabus，完成 Lecture 1 并写笔记`.
- For a knowledge point: choose the named concept and use `整理 <topic> 的核心定义、常见表示和一个最小例子`.
- For a technical route: `先画路线大纲，并找出前三个资源`.
- For a foundation route: do not create a vague next action. Choose a named first topic, such as `KL divergence`, `Bayes rule`, `matrix multiplication shapes`, `gradient descent`, `SE(3) transform composition`, or `Jacobian`, then define a small exercise.
- For a routine: `完成第一次打卡并记录 baseline`.

## Creation Defaults

Use these defaults when unspecified:

```text
状态: 进行中
节奏: 每周
下次推进: blank unless the user gives a day/date
进度: Not started
备注: include matching hints when the user wants the plan to be selected only when it relates to the day's tasks
```

## Output After Creation

After creating or drafting the Schedule row, tell the user:

```text
已加入 Schedule:
- 名称: ...
- 类型: ...
- 节奏: ...
- 下一步行动: ...

这些字段先留空: ...
```

Then ask whether they want to generate the first concrete Task now or let the next morning brief pick it up.
