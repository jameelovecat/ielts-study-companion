#!/usr/bin/env python3
"""Build downloadable WorkBuddy and Doubao Work Skill archives."""

from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
FULL_SKILL = ROOT / "skills" / "ielts-study"
DOUBAO_SKILL = ROOT / "skills" / "ielts-study-doubao"
DIST = ROOT / "dist"

WORKBUDDY_FRONTMATTER = """---
name: ielts-study
display_name: 雅思备考陪伴
display_name_en: IELTS Study Companion
description: Helps learners plan and continue IELTS practice with study records, focused lessons, mock tests and expression review.
description_zh: 根据学习目标和时间安排雅思练习、分项学习与表达复习。
description_en: Plan and continue IELTS practice, lessons and expression review around the learner's goals and available time.
examples_zh:
  - "开始雅思备考，先帮我了解目前水平。"
  - "带我做一轮Part 1专项口语训练。"
  - "查看我已上传的备考记录，安排今天的学习。"
examples_en:
  - "Help me plan IELTS study around my available time."
  - "Run a focused Part 1 speaking drill."
version: 1.0.0
author: 加米实验室
---
"""


def add_workbuddy_metadata(content: str) -> str:
    parts = content.split("---", 2)
    if len(parts) != 3 or not parts[0].startswith("\n") and parts[0]:
        raise ValueError("Cannot locate SKILL.md frontmatter")
    body = parts[2].lstrip("\n")
    return WORKBUDDY_FRONTMATTER + "\n" + body


def add_to_zip(archive: zipfile.ZipFile, source: Path, prefix: str, metadata: bool = False) -> None:
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.is_symlink() or ".DS_Store" in path.parts or "__pycache__" in path.parts:
            continue
        name = Path(prefix) / path.relative_to(source)
        data = path.read_bytes()
        if metadata and path.name == "SKILL.md":
            data = add_workbuddy_metadata(data.decode("utf-8")).encode("utf-8")
        archive.writestr(name.as_posix(), data)


def build() -> list[Path]:
    if not (FULL_SKILL / "SKILL.md").is_file():
        raise FileNotFoundError(FULL_SKILL / "SKILL.md")
    if not (DOUBAO_SKILL / "SKILL.md").is_file():
        raise FileNotFoundError(DOUBAO_SKILL / "SKILL.md")
    DIST.mkdir(exist_ok=True)
    workbuddy = DIST / "ielts-study-workbuddy.zip"
    doubao = DIST / "ielts-study-doubao.zip"
    with zipfile.ZipFile(workbuddy, "w", zipfile.ZIP_DEFLATED) as archive:
        add_to_zip(archive, FULL_SKILL, "ielts-study", metadata=True)
    with zipfile.ZipFile(doubao, "w", zipfile.ZIP_DEFLATED) as archive:
        add_to_zip(archive, DOUBAO_SKILL, "", metadata=False)
    return [workbuddy, doubao]


if __name__ == "__main__":
    for package in build():
        print(f"{package.relative_to(ROOT)} ({package.stat().st_size:,} bytes)")
