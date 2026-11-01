# 使用指南

## 首次建立系统

安装与启动见[首页](../README.md#怎么用)。助手先读取已有记录，了解考试类型、目标、时间与资料，再安排需要补足的真题诊断。诊断可分次完成，不同测试条件分别记录。

结合诊断，默认每科优先推荐一本主教材或一门课程，核验内容并说明章节、理由、时间和复查节点。用户确认后安排周计划；已有教材可继续使用，不强迫替换。

## 三种入口

- **分项学习**：接续确认教材的章节，解释方法、完成小练习、记录来源与进度。
- **真题练习**：从上次停下处继续；训练与完整模拟分开，后者不边做边泄露答案。
- **复习**：先回忆，再反馈；错题和表达依到期日安排，复习不等于重新完成一套题。

批改参照[来源与评分流程](../skills/ielts-study/references/learning-and-assessment.md)。口语训练每题给目标和建议时长，提供贴近本人表达版、参考版与搭配；仅有转写时不评分发音。

## 日程与提醒

计划保存到私有备考计划，提醒需另行确认并通过应用实际创建。两类提醒可分别暂停；没有到期复习内容时保持安静。可用通知方式及是否支持后台读取本地记录取决于应用，不是本项目自带推送服务。

## 数据位置

助手确定私有工作区，所有脚本显式使用 `--workspace`。初始化不会覆盖现有记录，会生成学习档案、资料索引、诊断记录、计划、课程进度、错题本和表达本。

当前脚本实现初始化、资料文件索引及JSON表达本的到期筛选和日期更新。诊断、教学、教材推荐、批改、错题复习记录、提醒配置和页面搭建由AI助手按Skill完成，不是脚本自动实现的功能。

## 辅助命令

从仓库运行：

```bash
python3 scripts/study.py --workspace /path/to/private-study init
python3 scripts/study.py --workspace /path/to/private-study index
python3 scripts/study.py --workspace /path/to/private-study due --date 2026-11-01
python3 scripts/study.py --workspace /path/to/private-study review expr-0001 --result correct --date 2026-11-01
python3 -m unittest discover -s tests -v
```

独立安装Skill时，将 `scripts/study.py` 替换为Skill目录内脚本的绝对路径。ID使用真实词条ID，日期采用学习者所在时区。完整数据格式见[数据约定](../skills/ielts-study/references/data-format.md)。
