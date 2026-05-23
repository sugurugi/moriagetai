"""
EVENT BOT
=========================================
概要:
  Discordサーバー向けのイベント日程調整BOT

機能:
  - 言語選択（ENG / JPN / CHI）
  - モード選択
      📅 日程のみ
      🕐 開始時間のみ
      📅🕐 日程・開始時間
  - ボタンで候補日を選択（複数月対応・最大30日）
  - 開始時間候補をモーダルで入力（最大10個）
  - リアクションで投票・解除（複数選択OK）
  - 投票データはPostgreSQLに永続保存

コマンド:
  /moriagetai  → BOTを起動

環境変数（Railwayで設定）:
  DISCORD_TOKEN   : BotのトークンKey
  DATABASE_URL    : PostgreSQL接続URL

制限:
  - 候補日: 最大30日
  - 開始時間候補: 最大10個
  - 月選択: 今月から12ヶ月先まで
=========================================
"""

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import calendar
import asyncpg
import os

# ===== 設定 =====
TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]

DATE_EMOJIS = [
    "🍕","🍔","🌮","🍜","🍣","🍱","🍛","🍝","🥗","🍤",
    "🍙","🍚","🍞","🥪","🍗","🍖","🥩","🍳","🥘","🫕",
    "🍲","🥣","🌯","🥙","🧆","🍿","🧁","🍩","🍦","🎂"
]  # 最大30日（20日超えは時間選択不可）
MAX_REACTION_DATES = 20  # Discordのリアクション上限
TIME_EMOJIS = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
WEEKDAYS_EN = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

TEXTS = {
    "ENG": {
        "select_lang":    "Please select a language.",
        "select_mode":    "Please select a mode.",
        "mode_date":      "📅 Date only",
        "mode_time":      "🕐 Time only",
        "mode_both":      "📅🕐 Date & Time",
        "select_month":   "Select months for candidate dates (multiple OK, up to 12 months). Tap again to deselect.\nSelected: {selected}",
        "select_date":    "Select candidate dates in **{year}/{month}** (up to 30 dates). Green = selected.\n⚠️ Over 20 dates: date & time cannot be combined (use separate modes).\nSelected: {selected}",
        "next_page":      "17+ →",
        "prev_page":      "← 1-16",
        "back_month":     "← Months",
        "back_mode":      "← Mode",
        "back_lang":      "← Language",
        "confirm_month":  "✅ Confirm Months",
        "confirm_date":   "✅ Confirm Dates",
        "confirmed":      "✅ Confirmed!",
        "input_time":     "⏰ Enter up to 10 time candidates separated by spaces.\nExample: `18:00 18:30 19:00`",
        "table_header":   "📅 Event Schedule",
        "time_header":    "🕐 Select Start Time",
        "no_one":         "-",
        "hint":           "React with the emoji for your preferred date(s)! You can select multiple.",
        "time_hint":      "React with the emoji for your preferred time(s)! You can select multiple.",
        "not_selected":   "(none)",
        "err_no_date":    "⚠️ Please select at least one date before confirming.",
        "err_no_month":   "⚠️ Please select at least one month before proceeding.",
        "err_max_date":   "⚠️ You can select up to {max} dates maximum.",
        "err_other_user": "You cannot interact with someone else's session.",
        "err_too_many_dates": "⚠️ You selected {n} dates (over 20). Date & Time combined mode is unavailable. Please use separate modes.",
        "select_all":        "✅ Select All",
        "deselect_all":      "🔄 Deselect All",
        "people":         "{n} votes",
    },
    "JPN": {
        "select_lang":    "言語を選択してください。",
        "select_mode":    "モードを選択してください。",
        "mode_date":      "📅 日程のみ",
        "mode_time":      "🕐 開始時間のみ",
        "mode_both":      "📅🕐 日程・開始時間",
        "select_month":   "候補日の月を選んでください（複数可・最大12ヶ月）。もう一度押すと解除。\n選択中: {selected}",
        "select_date":    "**{year}/{month}月** の候補日を選んでください（最大30日）。緑色＝選択済み。\n⚠️ 21日以上選択した場合は日程・開始時間の同時出力はできません。別々のモードをご利用ください。\n選択中: {selected}",
        "next_page":      "17日以降 →",
        "prev_page":      "← 1〜16日",
        "back_month":     "← 月選択に戻る",
        "back_mode":      "← モード選択に戻る",
        "back_lang":      "← 言語選択に戻る",
        "confirm_month":  "✅ 月を確定",
        "confirm_date":   "✅ 日付確定",
        "confirmed":      "✅ 確定しました！",
        "input_time":     "⏰ 開始時間の候補をスペース区切りで入力してください（最大10個）\n例: `18:00 18:30 19:00`",
        "table_header":   "📅 イベント予定日",
        "time_header":    "🕐 開始時間を選択してください",
        "no_one":         "ー",
        "hint":           "絵文字をタップして希望の日程に投票してください！複数選択OK。",
        "time_hint":      "絵文字をタップして希望の開始時間に投票してください！複数選択OK。",
        "not_selected":   "（未選択）",
        "err_no_date":    "⚠️ 確定する前に日付を1つ以上選んでください。",
        "err_no_month":   "⚠️ 次へ進む前に月を1つ以上選んでください。",
        "err_max_date":   "⚠️ 候補日は最大{max}日まで選択できます。",
        "err_other_user": "他の人の操作はできません。",
        "err_too_many_dates": "⚠️ {n}日選択されています（20日超）。日程・開始時間の同時出力はできません。それぞれ別のモードでご利用ください。",
        "select_all":        "✅ 全選択",
        "deselect_all":      "🔄 全解除",
        "people":         "{n}人",
    },
    "CHI": {
        "select_lang":    "请选择语言。",
        "select_mode":    "请选择模式。",
        "mode_date":      "📅 仅日期",
        "mode_time":      "🕐 仅开始时间",
        "mode_both":      "📅🕐 日期和开始时间",
        "select_month":   "请选择候选日期的月份（可多选，最多12个月）。再次点击取消选择。\n已选: {selected}",
        "select_date":    "请选择 **{year}/{month}月** 的候选日期（最多30天）。绿色＝已选。\n⚠️ 超过20天时，无法同时输出日期和时间，请分别使用对应模式。\n已选: {selected}",
        "next_page":      "17日以后 →",
        "prev_page":      "← 1〜16日",
        "back_month":     "← 返回月份选择",
        "back_mode":      "← 返回模式选择",
        "back_lang":      "← 返回语言选择",
        "confirm_month":  "✅ 确认月份",
        "confirm_date":   "✅ 确认日期",
        "confirmed":      "✅ 已确认！",
        "input_time":     "⏰ 请输入开始时间候选，用空格分隔（最多10个）\n例: `18:00 18:30 19:00`",
        "table_header":   "📅 活动预定日期",
        "time_header":    "🕐 请选择开始时间",
        "no_one":         "ー",
        "hint":           "请点击表情符号为您希望的日期投票！可多选。",
        "time_hint":      "请点击表情符号为您希望的开始时间投票！可多选。",
        "not_selected":   "（未选择）",
        "err_no_date":    "⚠️ 确认前请至少选择一个日期。",
        "err_no_month":   "⚠️ 继续前请至少选择一个月份。",
        "err_max_date":   "⚠️ 最多可选{max}个候选日期。",
        "err_other_user": "您无法操作他人的会话。",
        "err_too_many_dates": "⚠️ 已选{n}天（超过20天）。无法同时输出日期和时间，请分别使用对应模式。",
        "select_all":        "✅ 全选",
        "deselect_all":      "🔄 取消全选",
        "people":         "{n}人",
    }
}

COLS = 5
COL_WIDTH = 16

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
db: asyncpg.Pool = None


# ===== DB初期化 =====
async def init_db():
    global db
    db = await asyncpg.create_pool(DATABASE_URL)
    # 既存テーブルにrow_orderカラムがなければ追加
    await db.execute("ALTER TABLE polls ADD COLUMN IF NOT EXISTS row_order INT DEFAULT 0")

    await db.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            message_id BIGINT,
            emoji TEXT,
            date TEXT,
            weekday TEXT,
            lang TEXT,
            row_order INT DEFAULT 0,
            PRIMARY KEY (message_id, emoji)
        )
    """)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS poll_votes (
            message_id BIGINT,
            emoji TEXT,
            username TEXT,
            PRIMARY KEY (message_id, emoji, username)
        )
    """)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS time_polls (
            message_id BIGINT,
            emoji TEXT,
            time TEXT,
            lang TEXT,
            PRIMARY KEY (message_id, emoji)
        )
    """)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS time_votes (
            message_id BIGINT,
            emoji TEXT,
            username TEXT,
            PRIMARY KEY (message_id, emoji, username)
        )
    """)


# ===== ユーティリティ =====
def tx(lang, key, **kwargs):
    text = TEXTS[lang][key]
    return text.format(**kwargs) if kwargs else text

def get_weekday(year, month, day):
    try:
        return WEEKDAYS_EN[datetime(year, month, day).weekday()]
    except ValueError:
        return ""

def pad(text, width):
    length = sum(2 if ord(c) > 0x2E7F else 1 for c in text)
    return text + " " * max(0, width - length)

def get_date_str(selected_dates, lang):
    if not selected_dates:
        return tx(lang, "not_selected")
    return "  ".join(
        f"{d['month']}/{d['day']}"
        for d in sorted(selected_dates, key=lambda x: (x['year'], x['month'], x['day']))
    )

def get_month_str(selected_months, lang):
    if not selected_months:
        return tx(lang, "not_selected")
    return "  ".join(f"{m['year']}/{m['month']}" for m in sorted(selected_months, key=lambda x: (x['year'], x['month'])))


# ===== テーブル生成 =====
async def build_table_from_db(message_id, lang):
    rows = await db.fetch("SELECT emoji, date, weekday FROM polls WHERE message_id=$1 ORDER BY row_order", message_id)
    if not rows:
        return None
    date_data = {r['emoji']: {"date": r['date'], "weekday": r['weekday'], "users": []} for r in rows}
    votes = await db.fetch("SELECT emoji, username FROM poll_votes WHERE message_id=$1", message_id)
    for v in votes:
        if v['emoji'] in date_data:
            date_data[v['emoji']]["users"].append(v['username'])

    items = list(date_data.items())
    lines = ["```", tx(lang, "table_header"), "━" * (COLS * COL_WIDTH)]
    for row_start in range(0, len(items), COLS):
        row_items = items[row_start:row_start + COLS]
        lines.append("".join(
            pad(f"{e}:{info['date']}({info['weekday']})" if info['weekday'] else f"{e}:{info['date']}", COL_WIDTH)
            for e, info in row_items
        ))
        lines.append("".join(pad(tx(lang, "people", n=len(info["users"])), COL_WIDTH) for _, info in row_items))
        max_u = max(len(info["users"]) for _, info in row_items)
        if max_u == 0:
            lines.append("".join(pad(tx(lang, "no_one"), COL_WIDTH) for _ in row_items))
        else:
            for i in range(max_u):
                lines.append("".join(
                    pad(info["users"][i] if i < len(info["users"]) else "", COL_WIDTH)
                    for _, info in row_items
                ))
        lines.append("─" * (COLS * COL_WIDTH))
    lines += [tx(lang, "hint"), "```"]
    return "\n".join(lines)


async def build_time_table_from_db(message_id, lang):
    rows = await db.fetch("SELECT emoji, time FROM time_polls WHERE message_id=$1 ORDER BY emoji", message_id)
    if not rows:
        return None
    time_data = {r['emoji']: {"time": r['time'], "users": []} for r in rows}
    votes = await db.fetch("SELECT emoji, username FROM time_votes WHERE message_id=$1", message_id)
    for v in votes:
        if v['emoji'] in time_data:
            time_data[v['emoji']]["users"].append(v['username'])

    lines = ["```", tx(lang, "time_header"), "━" * 36]
    for emoji, info in time_data.items():
        users = info["users"]
        user_str = " ".join(users) if users else tx(lang, "no_one")
        lines.append(f"{emoji} {info['time']}  [{tx(lang, 'people', n=len(users))}]  {user_str}")
    lines += [tx(lang, "time_hint"), "```"]
    return "\n".join(lines)


# ===== 投稿ヘルパー =====
async def post_date_table(channel, selected_dates, lang):
    sorted_dates = sorted(selected_dates, key=lambda x: (x['year'], x['month'], x['day']))
    msg = await channel.send("...")
    for i, d in enumerate(sorted_dates):
        emoji = DATE_EMOJIS[i]
        await db.execute(
            "INSERT INTO polls (message_id, emoji, date, weekday, lang, row_order) VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT DO NOTHING",
            msg.id, emoji, f"{d['month']}/{d['day']}", get_weekday(d['year'], d['month'], d['day']), lang, i
        )
    content = await build_table_from_db(msg.id, lang)
    await msg.edit(content=content)
    for i in range(len(sorted_dates)):
        await msg.add_reaction(DATE_EMOJIS[i])


async def post_time_table(channel, time_list, lang):
    msg = await channel.send("...")
    for i, t_str in enumerate(time_list[:10]):
        emoji = TIME_EMOJIS[i]
        await db.execute(
            "INSERT INTO time_polls (message_id, emoji, time, lang) VALUES ($1,$2,$3,$4) ON CONFLICT DO NOTHING",
            msg.id, emoji, t_str, lang
        )
    content = await build_time_table_from_db(msg.id, lang)
    await msg.edit(content=content)
    for i in range(len(time_list[:10])):
        await msg.add_reaction(TIME_EMOJIS[i])


# ===== 言語選択 =====
class LangSelectView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=180)
        self.user_id = user_id
        for lang in ["ENG", "JPN", "CHI"]:
            btn = discord.ui.Button(label=lang, style=discord.ButtonStyle.primary)
            btn.callback = self.make_cb(lang)
            self.add_item(btn)

    def make_cb(self, lang):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(tx("ENG", "err_other_user"), ephemeral=True)
                return
            await interaction.response.edit_message(content=tx(lang, "select_mode"), view=ModeSelectView(self.user_id, lang))
        return cb


# ===== モード選択 =====
class ModeSelectView(discord.ui.View):
    def __init__(self, user_id, lang):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.lang = lang
        for mode, key in [("date","mode_date"),("time","mode_time"),("both","mode_both")]:
            btn = discord.ui.Button(label=tx(lang, key), style=discord.ButtonStyle.primary)
            btn.callback = self.make_cb(mode)
            self.add_item(btn)
        back = discord.ui.Button(label=tx(lang, "back_lang"), style=discord.ButtonStyle.secondary, row=1)
        back.callback = self.go_back
        self.add_item(back)

    def make_cb(self, mode):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
                return
            if mode == "time":
                await interaction.response.send_modal(TimeInputModal(self.lang, None, "time", interaction.channel))
            else:
                await interaction.response.edit_message(
                    content=tx(self.lang, "select_month", selected=tx(self.lang, "not_selected")),
                    view=MonthSelectView(self.user_id, self.lang, [], mode)
                )
        return cb

    async def go_back(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        await interaction.response.edit_message(content=tx(self.lang, "select_lang"), view=LangSelectView(self.user_id))


# ===== 月選択 =====
class MonthSelectView(discord.ui.View):
    def __init__(self, user_id, lang, selected_months, mode):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.lang = lang
        self.selected_months = selected_months
        self.mode = mode
        now = datetime.now()
        for i in range(12):
            m = (now.month - 1 + i) % 12 + 1
            y = now.year + (now.month - 1 + i) // 12
            is_sel = any(x['year'] == y and x['month'] == m for x in selected_months)
            btn = discord.ui.Button(
                label=f"{y}/{m}",
                style=discord.ButtonStyle.success if is_sel else discord.ButtonStyle.secondary,
                row=i // 4
            )
            btn.callback = self.make_cb(m, y)
            self.add_item(btn)
        confirm = discord.ui.Button(label=tx(lang, "confirm_month"), style=discord.ButtonStyle.danger, row=3)
        confirm.callback = self.confirm_cb
        self.add_item(confirm)
        back = discord.ui.Button(label=tx(lang, "back_mode"), style=discord.ButtonStyle.secondary, row=3)
        back.callback = self.go_back
        self.add_item(back)

    def make_cb(self, month, year):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
                return
            existing = next((x for x in self.selected_months if x['year'] == year and x['month'] == month), None)
            if existing:
                self.selected_months.remove(existing)
            else:
                self.selected_months.append({"year": year, "month": month})
            await interaction.response.edit_message(
                content=tx(self.lang, "select_month", selected=get_month_str(self.selected_months, self.lang)),
                view=MonthSelectView(self.user_id, self.lang, self.selected_months, self.mode)
            )
        return cb

    async def confirm_cb(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        if not self.selected_months:
            await interaction.response.send_message(tx(self.lang, "err_no_month"), ephemeral=True)
            return
        first = sorted(self.selected_months, key=lambda x: (x['year'], x['month']))[0]
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=first['year'], month=first['month'], selected=tx(self.lang, "not_selected")),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, 0, [], self.mode)
        )

    async def go_back(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        await interaction.response.edit_message(content=tx(self.lang, "select_mode"), view=ModeSelectView(self.user_id, self.lang))


# ===== 日付選択 =====
class DateSelectView(discord.ui.View):
    def __init__(self, user_id, lang, selected_months, month_idx, selected_dates, mode, page=0):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.lang = lang
        self.selected_months = sorted(selected_months, key=lambda x: (x['year'], x['month']))
        self.month_idx = month_idx
        self.selected_dates = selected_dates
        self.mode = mode
        self.page = page
        cur = self.selected_months[month_idx]
        self.cur_year = cur['year']
        self.cur_month = cur['month']
        _, last_day = calendar.monthrange(self.cur_year, self.cur_month)
        days = range(1, min(17, last_day + 1)) if page == 0 else range(17, last_day + 1)

        for day in days:
            wd = get_weekday(self.cur_year, self.cur_month, day)
            is_sel = any(d['year'] == self.cur_year and d['month'] == self.cur_month and d['day'] == day for d in selected_dates)
            btn = discord.ui.Button(label=f"{day}({wd})", style=discord.ButtonStyle.success if is_sel else discord.ButtonStyle.secondary)
            btn.callback = self.make_day_cb(day)
            self.add_item(btn)

        if page == 0 and last_day > 16:
            nb = discord.ui.Button(label=tx(lang, "next_page"), style=discord.ButtonStyle.primary, row=4)
            nb.callback = self.next_page
            self.add_item(nb)
        elif page == 1:
            pb = discord.ui.Button(label=tx(lang, "prev_page"), style=discord.ButtonStyle.primary, row=4)
            pb.callback = self.prev_page
            self.add_item(pb)

        if month_idx > 0:
            pm = discord.ui.Button(label=f"← {self.selected_months[month_idx-1]['month']}月", style=discord.ButtonStyle.secondary, row=4)
            pm.callback = self.prev_month
            self.add_item(pm)

        if month_idx < len(self.selected_months) - 1:
            nm = discord.ui.Button(label=f"{self.selected_months[month_idx+1]['month']}月 →", style=discord.ButtonStyle.primary, row=4)
            nm.callback = self.next_month
            self.add_item(nm)
        else:
            confirm = discord.ui.Button(label=tx(lang, "confirm_date"), style=discord.ButtonStyle.danger, row=4)
            confirm.callback = self.confirm_cb
            self.add_item(confirm)

        back = discord.ui.Button(label=tx(lang, "back_month"), style=discord.ButtonStyle.secondary, row=4)
        back.callback = self.go_back
        self.add_item(back)

        # 全選択・全解除（row=4に収まる場合のみ）
        sel_all = discord.ui.Button(label=tx(lang, "select_all"), style=discord.ButtonStyle.primary, row=4)
        sel_all.callback = self.select_all_cb
        self.add_item(sel_all)

        desel_all = discord.ui.Button(label=tx(lang, "deselect_all"), style=discord.ButtonStyle.secondary, row=4)
        desel_all.callback = self.deselect_all_cb
        self.add_item(desel_all)

    def make_day_cb(self, day):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
                return
            existing = next((d for d in self.selected_dates if d['year'] == self.cur_year and d['month'] == self.cur_month and d['day'] == day), None)
            if existing:
                self.selected_dates.remove(existing)
            else:
                if len(self.selected_dates) >= len(DATE_EMOJIS):
                    await interaction.response.send_message(tx(self.lang, "err_max_date", max=len(DATE_EMOJIS)), ephemeral=True)
                    return
                self.selected_dates.append({'year': self.cur_year, 'month': self.cur_month, 'day': day})
            await interaction.response.edit_message(
                content=tx(self.lang, "select_date", year=self.cur_year, month=self.cur_month, selected=get_date_str(self.selected_dates, self.lang)),
                view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx, self.selected_dates, self.mode, self.page)
            )
        return cb

    async def next_page(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=self.cur_year, month=self.cur_month, selected=get_date_str(self.selected_dates, self.lang)),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx, self.selected_dates, self.mode, 1)
        )

    async def prev_page(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=self.cur_year, month=self.cur_month, selected=get_date_str(self.selected_dates, self.lang)),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx, self.selected_dates, self.mode, 0)
        )

    async def next_month(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        next_m = self.selected_months[self.month_idx + 1]
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=next_m['year'], month=next_m['month'], selected=get_date_str(self.selected_dates, self.lang)),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx + 1, self.selected_dates, self.mode, 0)
        )

    async def prev_month(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        prev_m = self.selected_months[self.month_idx - 1]
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=prev_m['year'], month=prev_m['month'], selected=get_date_str(self.selected_dates, self.lang)),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx - 1, self.selected_dates, self.mode, 0)
        )

    async def confirm_cb(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        if not self.selected_dates:
            await interaction.response.send_message(tx(self.lang, "err_no_date"), ephemeral=True)
            return
        # 21日以上かつbothモードの場合は警告
        if self.mode == "both" and len(self.selected_dates) > MAX_REACTION_DATES:
            await interaction.response.send_message(
                tx(self.lang, "err_too_many_dates", n=len(self.selected_dates)), ephemeral=True)
            return
        if self.mode == "date":
            await interaction.response.edit_message(content=tx(self.lang, "confirmed"), view=None)
            await post_date_table(interaction.channel, self.selected_dates, self.lang)
        else:
            await interaction.response.send_modal(TimeInputModal(self.lang, self.selected_dates, self.mode, interaction.channel))

    async def go_back(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        await interaction.response.edit_message(
            content=tx(self.lang, "select_month", selected=get_month_str(self.selected_months, self.lang)),
            view=MonthSelectView(self.user_id, self.lang, self.selected_months, self.mode)
        )

    async def select_all_cb(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        import calendar as cal
        _, last_day = cal.monthrange(self.cur_year, self.cur_month)
        for day in range(1, last_day + 1):
            exists = any(d['year'] == self.cur_year and d['month'] == self.cur_month and d['day'] == day for d in self.selected_dates)
            if not exists and len(self.selected_dates) < len(DATE_EMOJIS):
                self.selected_dates.append({'year': self.cur_year, 'month': self.cur_month, 'day': day})
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=self.cur_year, month=self.cur_month, selected=get_date_str(self.selected_dates, self.lang)),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx, self.selected_dates, self.mode, self.page)
        )

    async def deselect_all_cb(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(tx(self.lang, "err_other_user"), ephemeral=True)
            return
        self.selected_dates = [d for d in self.selected_dates if not (d['year'] == self.cur_year and d['month'] == self.cur_month)]
        await interaction.response.edit_message(
            content=tx(self.lang, "select_date", year=self.cur_year, month=self.cur_month, selected=get_date_str(self.selected_dates, self.lang)),
            view=DateSelectView(self.user_id, self.lang, self.selected_months, self.month_idx, self.selected_dates, self.mode, self.page)
        )


# ===== 時間入力モーダル =====
class TimeInputModal(discord.ui.Modal):
    def __init__(self, lang, selected_dates, mode, channel=None):
        title_map = {"ENG": "Enter Time Candidates", "JPN": "開始時間を入力", "CHI": "输入开始时间"}
        super().__init__(title=title_map.get(lang, "時間入力"))
        self.lang = lang
        self.selected_dates = selected_dates
        self.mode = mode
        self.channel = channel
        self.time_input = discord.ui.TextInput(
            label={"ENG": "Time candidates", "JPN": "時間候補", "CHI": "时间候选"}.get(lang, "時間候補"),
            placeholder={"ENG": "e.g. 18:00 18:30 19:00", "JPN": "例: 18:00 18:30 19:00", "CHI": "例: 18:00 18:30 19:00"}.get(lang, ""),
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.time_input)

    async def on_submit(self, interaction: discord.Interaction):
        time_list = self.time_input.value.strip().split()
        if not time_list:
            await interaction.response.send_message("❌", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        channel = self.channel or interaction.channel
        if self.mode == "time":
            await post_time_table(channel, time_list, self.lang)
        else:
            await post_date_table(channel, self.selected_dates, self.lang)
            await post_time_table(channel, time_list, self.lang)


# ===== スラッシュコマンド =====
@tree.command(name="moriagetai", description="Event schedule coordinator")
async def moriagetai(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🌐 Select Language / 言語選択 / 选择语言",
        view=LangSelectView(interaction.user.id),
        ephemeral=True
    )


# ===== リアクションイベント =====
@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user.bot:
        return
    emoji = str(reaction.emoji)
    msg_id = reaction.message.id

    row = await db.fetchrow("SELECT lang FROM polls WHERE message_id=$1 AND emoji=$2", msg_id, emoji)
    if row:
        await db.execute(
            "INSERT INTO poll_votes (message_id, emoji, username) VALUES ($1,$2,$3) ON CONFLICT DO NOTHING",
            msg_id, emoji, user.display_name
        )
        content = await build_table_from_db(msg_id, row['lang'])
        if content:
            await reaction.message.edit(content=content)

    row = await db.fetchrow("SELECT lang FROM time_polls WHERE message_id=$1 AND emoji=$2", msg_id, emoji)
    if row:
        await db.execute(
            "INSERT INTO time_votes (message_id, emoji, username) VALUES ($1,$2,$3) ON CONFLICT DO NOTHING",
            msg_id, emoji, user.display_name
        )
        content = await build_time_table_from_db(msg_id, row['lang'])
        if content:
            await reaction.message.edit(content=content)


@bot.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
    if user.bot:
        return
    emoji = str(reaction.emoji)
    msg_id = reaction.message.id

    row = await db.fetchrow("SELECT lang FROM polls WHERE message_id=$1 AND emoji=$2", msg_id, emoji)
    if row:
        await db.execute("DELETE FROM poll_votes WHERE message_id=$1 AND emoji=$2 AND username=$3", msg_id, emoji, user.display_name)
        content = await build_table_from_db(msg_id, row['lang'])
        if content:
            await reaction.message.edit(content=content)

    row = await db.fetchrow("SELECT lang FROM time_polls WHERE message_id=$1 AND emoji=$2", msg_id, emoji)
    if row:
        await db.execute("DELETE FROM time_votes WHERE message_id=$1 AND emoji=$2 AND username=$3", msg_id, emoji, user.display_name)
        content = await build_time_table_from_db(msg_id, row['lang'])
        if content:
            await reaction.message.edit(content=content)


@bot.event
async def on_ready():
    await init_db()
    await tree.sync()
    print(f"✅ BOT起動: {bot.user}")


bot.run(TOKEN)
