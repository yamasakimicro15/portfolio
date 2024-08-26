from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)

# SQLiteデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fortune.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースモデルの定義
class FortuneHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    zodiac_sign = db.Column(db.String(10), nullable=False)
    fortune = db.Column(db.String(20), nullable=False)
    lucky_item = db.Column(db.String(20), nullable=False)
    warning = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FortuneHistory {self.name} - {self.fortune}>'

# 初回実行時にデータベースを作成する
with app.app_context():
    db.create_all()

# 運勢、ラッキーアイテム、注意喚起のリストを定義します
fortunes = ["最吉", "超吉", "大吉", "半吉", "チョビ吉", "吉害", "寸吉", "ギャン吉", "ドン底", "極楽", "微吉", "ホームラン"]
lucky_items = ["財布", "携帯", "腕時計", "帽子", "本", "ペン", "コーヒー", "キーホルダー", "カバン", "イヤホン"]
warnings = [
    "今日は大きな決断を避けましょう。",
    "衝動買いに注意。",
    "感情のコントロールがカギです。",
    "今日は人とのトラブルに注意。",
    "少し慎重になった方が良いかも。",
    "いつもより冷静に行動しましょう。",
    "過信せず、慎重に進んでください。",
    "物事が思い通りにいかないかも。"
]

# 生年月日から星座を計算する関数
def get_zodiac_sign(birthdate):
    date = datetime.strptime(birthdate, "%Y-%m-%d")
    month, day = date.month, date.day
    zodiac_ranges = [
        ((3, 21), (4, 19), "牡羊座"), ((4, 20), (5, 20), "牡牛座"), ((5, 21), (6, 20), "双子座"),
        ((6, 21), (7, 22), "蟹座"), ((7, 23), (8, 22), "獅子座"), ((8, 23), (9, 22), "乙女座"),
        ((9, 23), (10, 22), "天秤座"), ((10, 23), (11, 21), "蠍座"), ((11, 22), (12, 21), "射手座"),
        ((12, 22), (1, 19), "山羊座"), ((1, 20), (2, 18), "水瓶座"), ((2, 19), (3, 20), "魚座")
    ]
    for start, end, sign in zodiac_ranges:
        if (month, day) >= start and (month, day) <= end:
            return sign
    return "不明"

# Flaskのルート設定
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ユーザーの入力を取得
        name = request.form['name']
        birthdate = request.form['birthdate']

        # 占い結果を生成
        zodiac_sign = get_zodiac_sign(birthdate)
        fortune = random.choice(fortunes)
        lucky_item = random.choice(lucky_items)
        warning = random.choice(warnings)

        # 結果をデータベースに保存
        new_result = FortuneHistory(
            name=name,
            birthdate=birthdate,
            zodiac_sign=zodiac_sign,
            fortune=fortune,
            lucky_item=lucky_item,
            warning=warning
        )
        db.session.add(new_result)
        db.session.commit()

        # 結果ページにリダイレクト
        return redirect(url_for('result', result_id=new_result.id))

    # 初期のフォームページのHTMLテンプレート
    html_template = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>今日の運勢最高NO.1</title>
        <style>
            body {
                font-family: 'Verdana', sans-serif;
                text-align: center;
                background: linear-gradient(to bottom, #1a1a2e, #16213e);
                color: white;
                margin: 0;
                padding: 20px;
                overflow-y: auto;
            }
            h1 {
                font-size: 4em;
                margin-top: 50px;
                color: #ffd700;
                text-shadow: 0 0 20px #fff, 0 0 30px #ffd700;
                animation: title-glow 2s infinite alternate;
            }
            @keyframes title-glow { 0% { text-shadow: 0 0 20px #fff; } 100% { text-shadow: 0 0 80px #ffd700; } }
            form {
                font-size: 1.5em;
                margin-top: 30px;
                display: inline-block;
                text-align: left;
            }
            label {
                display: block;
                margin: 10px 0;
            }
            input[type="text"], input[type="date"] {
                width: 100%;
                padding: 10px;
                font-size: 1em;
                border: 2px solid #ffd700;
                border-radius: 5px;
                background-color: #2b2b52;
                color: #ffd700;
                margin-bottom: 20px;
            }
            button {
                font-size: 1.5em;
                padding: 15px 30px;
                border: 2px solid #ffd700;
                border-radius: 10px;
                background-color: #2b2b52;
                color: #ffd700;
                cursor: pointer;
                transition: all 0.3s;
            }
            button:hover {
                background-color: #ffd700;
                color: #2b2b52;
                transform: scale(1.1);
                box-shadow: 0 0 20px #ffd700;
            }
        </style>
    </head>
    <body>
        <h1>今日の運勢最高NO.1</h1>
        <form action="/" method="POST">
            <label for="name">名前:</label>
            <input type="text" id="name" name="name" required>
            <label for="birthdate">生年月日:</label>
            <input type="date" id="birthdate" name="birthdate" required>
            <button type="submit">占う</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_template)

# 結果ページのルート
@app.route('/result/<int:result_id>')
def result(result_id):
    # 結果をデータベースから取得
    result = FortuneHistory.query.get_or_404(result_id)

    # 結果ページのHTMLテンプレート
    html_template = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>{{ result.name }}さんの占い結果</title>
        <style>
            body {
                font-family: 'Verdana', sans-serif;
                text-align: center;
                background: linear-gradient(to bottom, #1a1a2e, #16213e);
                color: white;
                margin: 0;
                padding: 20px;
                overflow-y: auto;
            }
            .result-container {
                margin-top: 50px;
                font-size: 1.5em;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px #000;
                background-color: rgba(0, 0, 0, 0.8);
                color: #ffd700;
                text-shadow: 0 0 10px #ffd700;
                max-width: 90%;
                word-wrap: break-word;
            }
            h1 {
                font-size: 4em;
                color: #ffd700;
                text-shadow: 0 0 20px #fff, 0 0 30px #ffd700;
                animation: title-glow 2s infinite alternate;
            }
            @keyframes title-glow { 0% { text-shadow: 0 0 20px #fff; } 100% { text-shadow: 0 0 80px #ffd700; } }
        </style>
    </head>
    <body>
        <h1>{{ result.name }}さんの占い結果</h1>
        <div class="result-container">
            <h2>運勢: {{ result.fortune }}</h2>
            <h3>星座: {{ result.zodiac_sign }}</h3>
            <h3>ラッキーアイテム: {{ result.lucky_item }}</h3>
            <h3>注意喚起: {{ result.warning }}</h3>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, result=result)

# アプリケーションを起動します（ポート5001で動作します）
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
