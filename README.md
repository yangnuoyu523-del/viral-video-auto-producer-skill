Viral Video Auto Producer Skill
这是一个给 Codex 使用的短视频自动生产 Skill，用于把“爆款视频学习 → 爆款公式提炼 → 素材选题 → 原创脚本 → 分镜/剪辑方案 → 可编辑剪映草稿”串成一套可复用工作流。

它最适合这类场景：

小红书 / B站 / YouTube 爆款视频学习
科技产品视频、AI 机器人资讯视频
根据每日素材自动选题
先给爆款公式候选，等用户确认后再写脚本
自动生成口播稿、逐秒脚本、字幕、标签、信息卡
输出可编辑剪映草稿，而不是只给一条成片视频
目录结构
viral-video-auto-producer
├── SKILL.md
├── README.md
├── agents
│   └── openai.yaml
├── references
│   ├── environment.md
│   ├── github-publish.md
│   └── workflow.md
├── scripts
│   ├── build_editable_jianying_draft.py
│   └── validate_environment.py
└── templates
    ├── editable_draft_config.example.json
    └── formula_confirmation_card.md
核心流程
用户提供爆款视频链接、账号链接或历史学习资料。
Codex 使用视频分析 / 小红书抓取工具提取文案、节奏、分镜、评论反馈。
Skill 总结多个可复用的爆款公式。
在生成正式脚本前，必须先让用户确认使用哪个爆款公式、文案结构和剪辑规律。
用户提供当天素材、产品链接或新闻链接。
Skill 自动选题，生成标题、封面文案、口播稿、逐秒脚本、分镜表和剪辑建议。
生成剪映工程配置。
使用脚本创建可编辑剪映草稿。
校验草稿素材路径、轨道、音频、字幕和工程文件。
重要原则
一个视频只选一个主爆款公式，不把多个公式混在一起。
学习的是结构，不复刻别人的具体表达。
生成脚本前必须等待用户确认公式。
文案要像真人报道，避免 AI 味和尴尬梗。
剪映草稿要尽量保持可编辑，不默认压成单条视频。
所有素材都要复制到草稿内部，避免剪映提示素材无法访问。
环境要求
最低要求：

Python 3.9+
Git
Codex
剪映桌面版
jianying-editor skill
imageio-ffmpeg
pymediainfo
推荐同时安装：

video-analyzer：分析 B站、YouTube、本地视频
Spider_XHS：抓取公开小红书内容
de-ai-writing：中文文案去 AI 味
prompt-master：优化提示词和生成质量
安装依赖：

python3 -m pip install --user imageio-ffmpeg pymediainfo
配置剪映 skill 路径：

export JY_SKILL_ROOT="$HOME/.codex/skills/jianying-editor"
可选 API 配置
如果要自动分析、自动写脚本、生成视频素材，可以在 .env 中配置：

OPENAI_API_KEY=你的OpenAIKey
ARK_API_KEY=你的火山方舟Key
DOUBAO_API_KEY=你的火山方舟Key
DOUBAO_TEXT_MODEL=Doubao-Seed-2.0-pro
DOUBAO_VIDEO_MODEL=Doubao-Seedance-1.5-pro
JY_SKILL_ROOT=$HOME/.codex/skills/jianying-editor
说明：

DOUBAO_TEXT_MODEL 用于文案、分析、脚本生成。
DOUBAO_VIDEO_MODEL 只在需要生成新视频素材时使用。
剪映草稿生成本身不一定需要大模型 API。
具体模型 ID 可能变化，以上名称需要以服务商控制台为准。
如何检查环境
python ~/.codex/skills/viral-video-auto-producer/scripts/validate_environment.py
如果返回：

{
  "ok": true
}
说明基本环境可用。

如何使用
在 Codex 中可以这样说：

使用 viral-video-auto-producer，我给你爆款视频学习资料和今天的 AI 机器人素材。先学习爆款视频，总结公式候选，等我确认公式后，再生成脚本和可编辑剪映草稿。
或者：

用 viral-video-auto-producer 分析这个账号 2025 年 2 月的高赞视频，学习文案结构和剪辑规律，形成可复用爆款公式。
生成剪映草稿时，Skill 会优先使用：

python scripts/build_editable_jianying_draft.py --config project_config.json
配置文件格式可以参考：

templates/editable_draft_config.example.json
剪映草稿注意事项
新版 macOS 剪映可能使用加密工程文件。为了提高成功率，本 Skill 的草稿生成脚本会：

把视频转成 H.264 / AAC MP4
把音频转成 AAC M4A
把所有素材放进草稿内部 materials/
生成多轨可编辑时间线
补齐 draft_info.json、template-2.tmp、draft_settings
更新 root_meta_info.json
校验所有素材路径都在草稿文件夹内部
如果剪映仍无法打开，说明当前剪映版本和底层草稿库不兼容。这时可以保留配置文件，改用手动导入素材或生成成片 MP4 作为兜底。

上传 GitHub
进入本 skill 目录：

cd ~/.codex/skills/viral-video-auto-producer
初始化并提交：

git init
git add .
git commit -m "Initial viral video auto producer skill"
在 GitHub 创建空仓库后推送：

git remote add origin https://github.com/你的用户名/viral-video-auto-producer-skill.git
git branch -M main
git push -u origin main
更多说明见：

references/github-publish.md
不要上传的内容
不要提交：

.env
API Key
cookies
下载的视频素材
用户私有数据
剪映草稿工程
生成后的 MP4 / MOV / MP3 / M4A
建议添加 .gitignore：

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
推荐使用方式
这个 Skill 不只是一个剪映工具，而是一套内容生产方法。

最好的使用方式是：

先给 Codex 爆款账号或爆款视频。
让它学习结构，建立公式库。
每天给它素材。
让它先提出公式候选。
你确认公式后，它再写脚本和剪辑工程。
这样可以避免“一个视频塞太多方法”，保持内容风格稳定，也更接近真实爆款视频的生产逻辑。
