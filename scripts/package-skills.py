#!/usr/bin/env python3
"""Build the current IELTS Speaking Coach packages for WorkBuddy and ChatGPT."""

from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEAKING_SKILL = ROOT / "skills" / "ielts-speaking-coach"
DIST = ROOT / "dist"

WORKBUDDY_FRONTMATTER = """---
name: ielts-speaking-coach
display_name: 雅思口语陪练
display_name_en: IELTS Speaking Coach
description: IELTS speaking mock tests, focused Part drills, speaking diaries, expression review, and learning plans.
description_zh: 雅思口语模考、Part专项训练、自由表达、表达复习与学习计划。
description_en: IELTS speaking mock tests, focused Part drills, speaking diaries, expression review, and learning plans.
examples_zh:
  - "带我做一轮Part 1专项训练，先让我自己回答。"
  - "开始一次完整口语模考，结束后再统一反馈。"
  - "我想自由说三分钟，聊聊今天发生的事。"
version: 1.0.0
author: 加米实验室
---
"""


def add_workbuddy_metadata(content: str) -> str:
    parts = content.split("---", 2)
    if len(parts) != 3:
        raise ValueError("Cannot locate SKILL.md frontmatter")
    body = parts[2].lstrip("\n")
    return WORKBUDDY_FRONTMATTER + "\n" + body


def add_to_zip(
    archive: zipfile.ZipFile,
    source: Path,
    prefix: str,
    workbuddy_metadata: bool = False,
) -> None:
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.is_symlink() or ".DS_Store" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(source)
        if relative.parts[0] == "adapters":
            continue
        name = Path(prefix) / relative
        data = path.read_bytes()
        if workbuddy_metadata and path.name == "SKILL.md":
            data = add_workbuddy_metadata(data.decode("utf-8")).encode("utf-8")
        archive.writestr(name.as_posix(), data)


def build() -> list[Path]:
    if not (SPEAKING_SKILL / "SKILL.md").is_file():
        raise FileNotFoundError(SPEAKING_SKILL / "SKILL.md")

    DIST.mkdir(exist_ok=True)
    workbuddy = DIST / "ielts-speaking-coach-workbuddy.zip"
    chatgpt = DIST / "ielts-speaking-coach-chatgpt.zip"

    with zipfile.ZipFile(workbuddy, "w", zipfile.ZIP_DEFLATED) as archive:
        add_to_zip(archive, SPEAKING_SKILL, "ielts-speaking-coach", workbuddy_metadata=True)
    with zipfile.ZipFile(chatgpt, "w", zipfile.ZIP_DEFLATED) as archive:
        add_to_zip(archive, SPEAKING_SKILL, "ielts-speaking-coach")

    return [workbuddy, chatgpt]


if __name__ == "__main__":
    for package in build():
        print(f"{package.relative_to(ROOT)} ({package.stat().st_size:,} bytes)")
