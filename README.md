[README.md](https://github.com/user-attachments/files/28290763/README.md)
# Viral Video Auto Producer Skill

这是一个给 Codex 使用的短视频自动生产 Skill。

它把一条完整的视频生产流程串起来：

- 学习网上爆款视频
- 提炼可复用爆款公式
- 根据用户素材自动选题
- 先让用户确认爆款公式、文案结构和剪辑规律
- 生成原创标题、口播稿、逐秒脚本和分镜
- 自动生成可编辑剪映草稿
- 校验工程文件和素材路径

适合用于：

- 小红书爆款视频学习
- B站爆款视频学习
- YouTube 短视频学习
- AI 机器人资讯视频
- 科技产品视频
- 每日素材自动选题和脚本生成
- 可编辑剪映工程自动生成

## 目录结构

```text
viral-video-auto-producer/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    environment.md
    github-publish.md
    workflow.md
  scripts/
    build_editable_jianying_draft.py
    validate_environment.py
  templates/
    editable_draft_config.example.json
    formula_confirmation_card.md
```

## 核心原则

一个视频只使用一个主爆款公式。

不要把多个爆款公式混在同一个视频里，否则视频会变得没有重点。

这个 Skill 会先学习爆款视频的结构，而不是复制别人的具体表达。

在正式写脚本之前，它必须先让用户确认：

- 使用哪个爆款公式
- 使用什么文案结构
- 使用什么剪辑规律

确认之后，才会继续生成脚本和剪映工程。

## 工作流程

### 1. 爆款学习

用户提供爆款视频、账号主页或历史学习资料。

Skill 会分析：

- 视频文案
- 开头 3 秒钩子
- 脚本结构
- 分镜规律
- 情绪节奏
- 标题封面策略
- 评论反馈
- 可复用爆款公式

### 2. 公式确认

Skill 会给出几个爆款公式候选。

每个候选会说明：

- 适合什么素材
- 开头怎么做
- 文案结构是什么
- 剪辑节奏是什么
- 有什么风险
- 需要补什么素材

用户确认一个公式后，才进入脚本生成。

### 3. 素材选题

用户提供当天素材、新闻链接、产品链接或视频素材。

Skill 会优先选择最有趣、最容易吸引人的选题，而不是强行覆盖所有素材。

### 4. 脚本生成

输出内容包括：

- 标题
- 封面文案
- 口播稿
- 逐秒脚本
- 分镜表
- 字幕和画面标签
- 剪辑建议
- 素材缺口
- 事实核查清单

### 5. 剪映草稿生成

Skill 会生成可编辑剪映草稿。

草稿会尽量保留这些轨道：

- 视频切片轨
- 口播音频轨
- BGM 音频轨
- 字幕轨
- 标签轨
- 信息卡轨
- 待核实提示轨

为了避免剪映提示素材丢失，脚本会把素材复制到草稿内部。

## 环境要求

最低需要：

- Python 3.9 或更高版本
- Git
- Codex
- 剪映桌面版
- jianying-editor skill
- imageio-ffmpeg
- pymediainfo

推荐安装：

- video-analyzer
- Spider_XHS
- de-ai-writing
- prompt-master

安装依赖：

```bash
python3 -m pip install --user imageio-ffmpeg pymediainfo
```

配置剪映 skill 路径：

```bash
export JY_SKILL_ROOT="$HOME/.codex/skills/jianying-editor"
```

## 可选 API 配置

如果要自动分析、自动写脚本或生成视频素材，可以在 `.env` 中配置：

```bash
OPENAI_API_KEY=你的OpenAIKey
ARK_API_KEY=你的火山方舟Key
DOUBAO_API_KEY=你的火山方舟Key
DOUBAO_TEXT_MODEL=Doubao-Seed-2.0-pro
DOUBAO_VIDEO_MODEL=Doubao-Seedance-1.5-pro
JY_SKILL_ROOT=$HOME/.codex/skills/jianying-editor
```

说明：

- 文案分析和脚本生成可以使用 OpenAI 或 Doubao 文本模型。
- 视频素材生成可以使用 Doubao Seedance。
- 剪映草稿生成本身不一定需要大模型 API。
- 具体模型 ID 可能变化，请以服务商控制台为准。

## 检查环境

运行：

```bash
python ~/.codex/skills/viral-video-auto-producer/scripts/validate_environment.py
```

如果返回 `ok: true`，说明基本环境可用。

## 使用方法

在 Codex 中可以这样说：

```text
使用 viral-video-auto-producer，我给你爆款视频学习资料和今天的 AI 机器人素材。先学习爆款视频，总结公式候选，等我确认公式后，再生成脚本和可编辑剪映草稿。
```

也可以这样说：

```text
用 viral-video-auto-producer 分析这个账号 2025 年 2 月的高赞视频，学习文案结构和剪辑规律，形成可复用爆款公式。
```

## 生成可编辑剪映草稿

脚本入口：

```bash
python scripts/build_editable_jianying_draft.py --config project_config.json
```

配置文件示例：

```text
templates/editable_draft_config.example.json
```

## 上传 GitHub

进入 skill 目录：

```bash
cd ~/.codex/skills/viral-video-auto-producer
```

初始化并提交：

```bash
git init
git add .
git commit -m "Initial viral video auto producer skill"
```

推送到 GitHub：

```bash
git remote add origin https://github.com/你的用户名/viral-video-auto-producer-skill.git
git branch -M main
git push -u origin main
```

## 不要上传的内容

不要上传：

- `.env`
- API Key
- cookies
- 下载的视频素材
- 用户私有数据
- 剪映草稿工程
- 生成后的 MP4、MOV、MP3、M4A

建议添加 `.gitignore`：

```gitignore
.env
outputs/
tmp/
*.mp4
*.mov
*.m4a
*.mp3
*.ogg
*.wav
*.cookie
cookies*
```

## 推荐使用方式

最好的用法是：

1. 先给 Codex 爆款账号或爆款视频。
2. 让它学习结构，建立爆款公式库。
3. 每天给它新素材。
4. 让它先提出公式候选。
5. 用户确认公式后，再生成脚本和剪辑工程。

这样可以保持视频主线清晰，也更接近真实爆款内容的生产逻辑。
