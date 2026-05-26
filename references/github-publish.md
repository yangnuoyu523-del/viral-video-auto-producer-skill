# 如何把这个 Skill 上传到 GitHub

## 1. 进入 Skill 文件夹

```bash
cd ~/.codex/skills/viral-video-auto-producer
```

## 2. 初始化 Git 仓库

```bash
git init
git add .
git commit -m "Initial viral video auto producer skill"
```

如果你之前已经初始化过 Git，可以跳过 `git init`。

## 3. 在 GitHub 创建新仓库

打开 GitHub，新建一个空仓库，例如：

```text
viral-video-auto-producer-skill
```

建议不要勾选自动创建 `README`、`.gitignore` 或 license，避免和本地第一次推送冲突。

## 4. 绑定远程仓库并推送

把下面的 `<你的用户名>` 换成你的 GitHub 用户名：

```bash
git remote add origin https://github.com/<你的用户名>/viral-video-auto-producer-skill.git
git branch -M main
git push -u origin main
```

如果你习惯用 SSH，可以用：

```bash
git remote add origin git@github.com:<你的用户名>/viral-video-auto-producer-skill.git
git branch -M main
git push -u origin main
```

## 5. 其他电脑如何安装

方式一：让 Codex 安装 GitHub skill。

```text
安装这个 skill：https://github.com/<你的用户名>/viral-video-auto-producer-skill
```

方式二：手动 clone 到 Codex skills 目录。

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/<你的用户名>/viral-video-auto-producer-skill.git ~/.codex/skills/viral-video-auto-producer
```

安装后重启 Codex，让它重新读取 skill 列表。

## 6. 不要上传的内容

不要提交这些文件：

- `.env`
- API key
- 小红书/平台 cookies
- 下载的视频素材
- 用户私有数据
- 剪映草稿工程
- 生成后的成片和音频

建议在仓库根目录添加 `.gitignore`：

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

## 7. 更新 Skill 后如何同步到 GitHub

每次修改 skill 后执行：

```bash
cd ~/.codex/skills/viral-video-auto-producer
git status
git add .
git commit -m "Update skill workflow"
git push
```
