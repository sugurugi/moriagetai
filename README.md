# 🍕 EVENT BOT

> 🇯🇵 日本語の説明は[こちら](#-日本語)
> 
> 🇺🇸 English documentation [here](#-english)
> 
> 🇨🇳 中文说明请点击[这里](#-中文)

---

## 🇯🇵 日本語

Discord上でイベントの日程・開始時間を調整するBOTです。

### ✨ 機能

- 🌐 多言語対応（English / 日本語 / 中文）
- 📅 ボタンで候補日を選択（複数月対応・最大30日）
- 🕐 開始時間候補をポップアップで入力（最大10個）
- 🍕 リアクションで投票・解除（複数選択OK）
- 💾 PostgreSQLで投票データを永続保存
- 📊 3つのモード：日程のみ / 開始時間のみ / 日程＋開始時間

### 🚀 セットアップ

#### 1. Discord Developer Portal でBOTを作成

1. https://discord.com/developers/applications にアクセス
2. 「New Application」→ 名前をつけて作成
3. 「Bot」タブ → トークンをコピー
4. 「Privileged Gateway Intents」で以下をON：
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

#### 2. 必要なもの

- Python 3.10以上
- PostgreSQL（またはRailwayのPostgreSQLアドオン）

#### 3. 環境変数を設定

```
DISCORD_TOKEN=あなたのBotトークン
DATABASE_URL=PostgreSQLの接続URL
```

#### 4. 依存パッケージをインストール

```bash
pip install discord.py asyncpg
```

#### 5. 起動

```bash
python main.py
```

### ☁️ Railwayへのデプロイ

1. [Railway](https://railway.app) にGitHubでログイン
2. 「New Project」→「Deploy from GitHub repo」
3. このリポジトリを選択
4. PostgreSQLアドオンを追加
5. Variables に `DISCORD_TOKEN` と `DATABASE_URL` を設定
6. Start Command に `python main.py` を設定

### 📖 使い方

```
/moriagetai
```

1. 言語を選択（ENG / JPN / CHI）
2. モードを選択（日程のみ / 開始時間のみ / 日程＋開始時間）
3. 月・日付をボタンで選択
4. 開始時間候補を入力
5. チャンネルに投票表が投稿される！

### ⚠️ 制限事項

- 候補日：最大30日（21日以上は日程と開始時間の同時出力不可）
- 開始時間候補：最大10個
- 月選択：今月から12ヶ月先まで

### 📄 ライセンス

MIT License - 自由に使用・改変・配布できます。

### 🤝 コントリビューション

PRや Issue 大歓迎です！

---

## 🇺🇸 English

A Discord BOT for coordinating event schedules and start times.

### ✨ Features

- 🌐 Multi-language support (English / 日本語 / 中文)
- 📅 Select candidate dates with buttons (multi-month, up to 30 days)
- 🕐 Enter start time candidates via popup (up to 10)
- 🍕 Vote and unvote with reactions (multiple selections OK)
- 💾 Persistent vote data with PostgreSQL
- 📊 3 modes: Date only / Time only / Date & Time

### 🚀 Setup

#### 1. Create a BOT on Discord Developer Portal

1. Go to https://discord.com/developers/applications
2. Click "New Application" and give it a name
3. Go to "Bot" tab → Copy the token
4. Enable the following under "Privileged Gateway Intents":
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

#### 2. Requirements

- Python 3.10+
- PostgreSQL (or Railway PostgreSQL add-on)

#### 3. Set environment variables

```
DISCORD_TOKEN=your_bot_token
DATABASE_URL=your_postgresql_url
```

#### 4. Install dependencies

```bash
pip install discord.py asyncpg
```

#### 5. Run

```bash
python main.py
```

### ☁️ Deploy to Railway

1. Log in to [Railway](https://railway.app) with GitHub
2. "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Add PostgreSQL add-on
5. Set `DISCORD_TOKEN` and `DATABASE_URL` in Variables
6. Set Start Command to `python main.py`

### 📖 Usage

```
/moriagetai
```

1. Select language (ENG / JPN / CHI)
2. Select mode (Date only / Time only / Date & Time)
3. Select months and dates with buttons
4. Enter start time candidates
5. A voting table is posted in the channel!

### ⚠️ Limitations

- Candidate dates: up to 30 (over 20 dates: Date & Time combined mode unavailable)
- Start time candidates: up to 10
- Month selection: current month to 12 months ahead

### 📄 License

MIT License - Free to use, modify, and distribute.

### 🤝 Contributing

PRs and Issues are welcome!

---

## 🇨🇳 中文

一个用于协调活动日程和开始时间的Discord机器人。

### ✨ 功能

- 🌐 多语言支持（English / 日本語 / 中文）
- 📅 通过按钮选择候选日期（支持跨月，最多30天）
- 🕐 通过弹窗输入开始时间候选（最多10个）
- 🍕 通过表情符号投票和取消投票（可多选）
- 💾 使用PostgreSQL永久保存投票数据
- 📊 3种模式：仅日期 / 仅开始时间 / 日期＋开始时间

### 🚀 安装步骤

#### 1. 在Discord Developer Portal创建机器人

1. 访问 https://discord.com/developers/applications
2. 点击"New Application"并命名
3. 进入"Bot"标签页 → 复制Token
4. 在"Privileged Gateway Intents"中开启以下选项：
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

#### 2. 环境要求

- Python 3.10以上
- PostgreSQL（或Railway的PostgreSQL插件）

#### 3. 设置环境变量

```
DISCORD_TOKEN=你的Bot Token
DATABASE_URL=PostgreSQL连接URL
```

#### 4. 安装依赖

```bash
pip install discord.py asyncpg
```

#### 5. 启动

```bash
python main.py
```

### ☁️ 部署到Railway

1. 使用GitHub登录 [Railway](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. 选择此仓库
4. 添加PostgreSQL插件
5. 在Variables中设置 `DISCORD_TOKEN` 和 `DATABASE_URL`
6. 将Start Command设置为 `python main.py`

### 📖 使用方法

```
/moriagetai
```

1. 选择语言（ENG / JPN / CHI）
2. 选择模式（仅日期 / 仅开始时间 / 日期＋开始时间）
3. 通过按钮选择月份和日期
4. 输入开始时间候选
5. 投票表将发布到频道中！

### ⚠️ 限制

- 候选日期：最多30天（超过20天时，日期和时间无法同时输出）
- 开始时间候选：最多10个
- 月份选择：当前月到未来12个月

### 📄 许可证

MIT License - 可自由使用、修改和分发。

### 🤝 贡献

欢迎提交PR和Issue！

---

## 🇯🇵 ローカルでの起動方法

RailwayなしでPC上で直接動かす方法です。

### 1. リポジトリをダウンロード

```bash
git clone https://github.com/sugurugi/moriagetai.git
cd moriagetai
```

または右上の「Code」→「Download ZIP」でダウンロードして解凍してください。

### 2. Pythonのインストール

https://www.python.org/downloads/ からPython 3.10以上をインストール。
インストール時に **「Add Python to PATH」** にチェックを入れること！

### 3. 依存パッケージをインストール

```bash
pip install discord.py asyncpg
```

### 4. PostgreSQLの準備

- [PostgreSQL公式サイト](https://www.postgresql.org/download/)からインストール
- データベースを作成してURLをメモしておく

### 5. 環境変数を設定

Windowsの場合：
```
set DISCORD_TOKEN=あなたのトークン
set DATABASE_URL=あなたのPostgreSQL URL
```

Mac/Linuxの場合：
```
export DISCORD_TOKEN=あなたのトークン
export DATABASE_URL=あなたのPostgreSQL URL
```

### 6. 起動

```bash
python main.py
```

`✅ BOT起動:` と表示されれば成功です！

⚠️ **注意**: コマンドプロンプトを閉じるとBOTも止まります。

---

## 🇺🇸 Running Locally

How to run the BOT on your PC without Railway.

### 1. Download the repository

```bash
git clone https://github.com/sugurugi/moriagetai.git
cd moriagetai
```

Or click "Code" → "Download ZIP" and extract it.

### 2. Install Python

Install Python 3.10+ from https://www.python.org/downloads/
Make sure to check **"Add Python to PATH"** during installation!

### 3. Install dependencies

```bash
pip install discord.py asyncpg
```

### 4. Set up PostgreSQL

- Install from [PostgreSQL official site](https://www.postgresql.org/download/)
- Create a database and note down the URL

### 5. Set environment variables

Windows:
```
set DISCORD_TOKEN=your_token
set DATABASE_URL=your_postgresql_url
```

Mac/Linux:
```
export DISCORD_TOKEN=your_token
export DATABASE_URL=your_postgresql_url
```

### 6. Run

```bash
python main.py
```

If you see `✅ BOT起動:`, it's working!

⚠️ **Note**: Closing the terminal will stop the BOT.

---

## 🇨🇳 本地运行方法

不使用Railway，直接在电脑上运行BOT的方法。

### 1. 下载仓库

```bash
git clone https://github.com/sugurugi/moriagetai.git
cd moriagetai
```

或点击右上角"Code"→"Download ZIP"下载并解压。

### 2. 安装Python

从 https://www.python.org/downloads/ 安装Python 3.10以上版本。
安装时务必勾选 **"Add Python to PATH"**！

### 3. 安装依赖

```bash
pip install discord.py asyncpg
```

### 4. 准备PostgreSQL

- 从[PostgreSQL官网](https://www.postgresql.org/download/)安装
- 创建数据库并记下连接URL

### 5. 设置环境变量

Windows:
```
set DISCORD_TOKEN=你的Token
set DATABASE_URL=你的PostgreSQL URL
```

Mac/Linux:
```
export DISCORD_TOKEN=你的Token
export DATABASE_URL=你的PostgreSQL URL
```

### 6. 启动

```bash
python main.py
```

看到 `✅ BOT起動:` 就表示成功了！

⚠️ **注意**: 关闭终端窗口会导致BOT停止运行。


---

## 🇯🇵 トラブルシューティング

### BOTがオフラインになった
1. Railwayのプロジェクトを開く
2. BOTのサービス → 「Deployments」タブ
3. 「Redeploy」をクリック
4. それでも直らない場合はDiscord Developer Portalでトークンをリセットして、RailwayのVariablesを更新する

### スラッシュコマンドが出てこない
- Discordを完全に再起動する
- しばらく待つ（最大1時間かかる場合あり）

### インタラクションに失敗しましたと表示される
- BOTがクラッシュしている可能性がある → Railwayのログを確認する
- Discordを再起動して再度試す

### リアクションが反応しない
- BOTがオフラインになっている可能性がある → Railwayを確認する
- Server Members IntentがONになっているか確認する

### データが消えた
- RailwayのPostgreSQLが正常に動作しているか確認する
- BOTサービスのVariablesに `DATABASE_URL` が設定されているか確認する

---

## 🇺🇸 Troubleshooting

### BOT is offline
1. Open your Railway project
2. Click the BOT service → "Deployments" tab
3. Click "Redeploy"
4. If it still doesn't work, reset the token in Discord Developer Portal and update the Railway Variables

### Slash command doesn't appear
- Fully restart Discord
- Wait a while (may take up to 1 hour)

### "Interaction failed" error
- The BOT may have crashed → Check Railway logs
- Restart Discord and try again

### Reactions don't work
- The BOT may be offline → Check Railway
- Make sure Server Members Intent is enabled

### Data was lost
- Check that Railway PostgreSQL is running properly
- Make sure `DATABASE_URL` is set in the BOT service Variables

---

## 🇨🇳 故障排除

### 机器人离线了
1. 打开Railway项目
2. 点击BOT服务 → "Deployments"标签
3. 点击"Redeploy"
4. 如果仍然无效，请在Discord Developer Portal重置Token，并更新Railway的Variables

### 斜杠命令不显示
- 完全重启Discord
- 等待一段时间（最多可能需要1小时）

### 显示"交互失败"错误
- BOT可能已崩溃 → 检查Railway日志
- 重启Discord后再试

### 表情符号反应无效
- BOT可能离线 → 检查Railway
- 确认Server Members Intent已开启

### 数据丢失了
- 检查Railway的PostgreSQL是否正常运行
- 确认BOT服务的Variables中已设置`DATABASE_URL`
