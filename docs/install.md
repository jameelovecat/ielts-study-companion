# 各平台安装指南

本项目提供两种版本：

- **完整版本**：保存到本地学习目录，可使用学习模板、复习脚本和参考资料。适用于 Codex、Claude Code 和 WorkBuddy。
- **豆包工作聊天版**：Skill 规则内置在单个文件中。资料需在对话中上传，进度由助手整理成可复制内容；不自动读写本地文件或安排提醒。

## Codex 与 Claude Code

需要 Node.js 22.20 或更新版本。终端运行：

```bash
npx skills add jameelovecat/ielts-study-companion --skill ielts-study -g -a codex -a claude-code
```

`-g` 表示安装到个人目录，在不同项目中都可以使用。安装时若出现已有同名 Skill 的提示，先查看现有版本再决定是否更新。安装后重新打开 Codex 或 Claude Code 会话，再说「开始雅思备考」。

更新时运行：

```bash
npx skills update ielts-study
```

如果你不想用终端，也可以把仓库链接发给 Codex 或 Claude Code，并让它按当前应用支持的方式安装 `skills/ielts-study/`；先检查同名目录，保留已有内容后再处理。

Skills CLI 也支持其他兼容 Agent。可按[CLI支持列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)选择对应名称安装；是否能使用本地记录和脚本，取决于该 Agent 的文件与命令权限。

## WorkBuddy

1. [下载 WorkBuddy 完整版压缩包](../dist/ielts-study-workbuddy.zip)。
2. 打开 WorkBuddy 的「专家 · 技能 · 连接器」→「技能」→「添加技能」→「上传技能」，选择压缩包。
3. 安装后在对话中说「开始雅思备考」。

WorkBuddy 可能在首次读取或保存学习文件时请求相应权限。只选择你希望它访问的学习目录。学习资料仍由你自己提供，项目不附带真题文件或音频。

## 豆包工作

豆包版是对话适配版，文件位于 `skills/ielts-study-doubao/`，下载包为[豆包工作聊天版](../dist/ielts-study-doubao.zip)。它适合在豆包工作对话中练习、讨论学习计划，并处理当前对话上传的教材和记录。每次练习后，助手可以给出可复制的记录更新；下次继续时上传最新记录即可。

要把它作为技能安装，需要通过豆包开放平台上传技能包并完成平台流程。公开上架要求企业资质认证和审核；企业内部发布由企业管理员审核。通过后，用户可在豆包工作客户端的技能入口安装。仅下载压缩包不会自动把技能添加到账户。

此版本不能像本地 Agent 那样读取你的电脑文件夹、自动更新文件、运行本地复习脚本或创建系统提醒。需要这些能力时，使用完整版本，或另行建设带远程工具和存储服务的豆包应用。

## 更新与资料安全

- 更新 Skill 前先确认现有进度文件已保存在私有学习目录，并保留同名 Skill 中的用户修改。
- 不要把个人学习档案、成绩、真题 PDF、音频或录音上传到公开仓库。
- 本仓库只发布 Skill、空白模板和公开说明，不包含版权真题资料。
- Skills CLI、WorkBuddy 和豆包工作平台的功能会调整；遇到界面变化时以各平台当前说明为准。

平台说明：[Skills CLI](https://www.skills.sh/docs/cli) · [WorkBuddy 技能](https://open.workbuddy.cn/en/docs/skill) · [豆包技能接入指南](https://open.doubao.com/document/doubao-developer-guide/skill-integration-guide)
