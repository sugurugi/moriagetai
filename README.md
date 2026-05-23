

https://github.com/user-attachments/assets/4e9c0a1a-7f3f-46af-ae0e-4280587435a6

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
