# IELTS Study Companion

用你自己的 Codex 或 Claude Code，搭建一个记得学习进度的雅思备考助手。

**告诉它你有多久 → 练真题 → 分析错因 → 积累表达 → 到期复习。**

这是一个本地优先的助手工作流与 Skill 项目，面向中文用户。无需部署网站，无需为本项目配置额外的 API 密钥；需要可用的 Codex 或 Claude Code，以及 Python 3.10 及以上版本。AI 工具本身可能收费。

## 三步开始

### １．下载项目

```bash
git clone https://github.com/jameelovecat/ielts-study-companion.git
cd ielts-study-companion
python3 scripts/study.py init
```

也可以在 GitHub 选择 Code → Download ZIP，解压后进入目录，运行初始化命令。

### ２．在项目目录打开 AI 工具

```bash
codex
# 或者
claude
```

Codex 使用项目里的 `AGENTS.md`，Claude Code 使用 `CLAUDE.md`；两者都指向同一份备考规则。不必先安装全局 Skill。

把这句话发给它：

> 帮我初始化雅思备考。先了解我的考试类型、目标和可用时间，再索引我的本地真题资料。暂时没有考试日期也可以先开始。

### ３．提供自己的资料

把有权使用的 PDF 和音频放进 `workspace/materials/`，或在 `workspace/config.json` 的 `material_roots` 中填写原有文件夹的绝对路径。助手也可以替你配置。

```bash
python3 scripts/study.py index
```

索引仅按文件路径发现资料，**不自动识别册数、题目页、答案或音频对应关系**。助手需阅读核对后，将定位信息写进资料索引；扫描 PDF 可能需要本地 OCR。

## 你可以直接说

- 「我有 30 分钟，安排今天的练习。」
- 「我做完了剑 18 Test 1 听力 Section 2，帮我批改。」
- 「这道判断题为什么是 NOT GIVEN？给我看定位句。」
- 「练一套口语，一次问我一题。」
- 「帮我批改这篇作文，保留我的观点。」
- 「复习今天到期的表达。」

默认先了解你、再建议学习顺序；不固定从某册开始。考试类型未确认时，不混用 Academic 与 General Training 的阅读、写作材料。

## 能做什么

| 功能 | 工作方式 |
|---|---|
| 按时间安排 | 根据最近记录、弱项和可用时间推荐练习 |
| 听力、阅读 | 从你的资料定位题目、答案和原文，批改并解释错因 |
| 写作 | 词数、四项反馈、估分与保留原意的修改 |
| 口语 | 考官一问一答；文字回答无法评估发音 |
| 学习记录 | 各科分别跟踪进度，区分完成、计划和仅讨论 |
| 表达复习 | 本地词条，按到期日抽查，脚本更新复习间隔 |

AI 负责对话与解析，Python 脚本负责初始化、文件索引及复习日期计算。**不是自动评分引擎，也不保证提分或官方评分精度。**录音、转写和计时取决于所在工具环境；没有实际计时能力时使用者自行设定计时器，助手不能声称有后台提醒。

## 文件与隐私

```text
skills/ielts-study/       两种工具共用的备考规则
scripts/study.py           零第三方依赖的辅助命令
templates/                空白档案和记录模板
examples/                 明确标记的虚构演示
workspace/                初始化后生成，你自己的资料和记录
```

`workspace/` 默认被 Git 忽略。真题、录音、作文、记录和密钥不得提交到公开仓库。资料默认不上传；但将摘录、作文或音频交给 AI 时，会受到所使用 AI 服务的数据政策约束，**本地保存不等于离线推理**。麦克风录制、云端转写与额外外部服务需要事先确认。

仓库不分发剑桥真题、音频、答案、现成题库或他人的个人记录。MIT 许可证仅覆盖本项目自己的代码、指令和模板，不授予第三方材料的使用权。

## 资料参考

可以参考社区整理的 [zeeklog／IELTS 雅思资料库](https://github.com/zeeklog/IELTS)，查看其真题、听力音频和写作等资料目录。

该仓库是独立的第三方项目，与本项目无隶属关系。GitHub 上公开可访问不代表其中所有资料均获开放许可；下载、使用或再分发前，请自行确认原作者及出版方的版权与授权。本项目只提供参考链接，不附带、镜像或自动下载其中的资料。

取得有权使用的资料后，可以放入本地 `workspace/materials/`，或将现有资料目录配置到 `material_roots`，再运行索引命令。

## 辅助命令

```bash
python3 scripts/study.py init
python3 scripts/study.py index
python3 scripts/study.py due --date 2026-11-01
python3 scripts/study.py review expr-demo --result correct --date 2026-11-01
python3 -m unittest discover -s tests -v
```

`review` 要使用表达本中实际存在的 ID；`expr-demo` 仅为示例。默认工作目录为当前项目的 `workspace/`，可用 `--workspace /path/to/private-folder` 指定其他位置。

更多格式见 [数据约定](docs/data-format.md)。想分享改进，欢迎提交 Issue 或 Pull Request；请使用虚构例子复现问题，勿附版权真题或私人数据。

由 Jamee／加米发起，从个人备考实践中整理。
