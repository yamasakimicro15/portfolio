from flask import Flask, render_template_string
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

# 人の名前と生年月日のリストを定義します
people = [
    {"name": "山崎", "birthdate": "1990-03-21"},
    {"name": "山田", "birthdate": "1985-04-15"},
    {"name": "山内", "birthdate": "1992-05-23"},
    {"name": "木内", "birthdate": "1988-06-01"},
    {"name": "とおる", "birthdate": "1994-07-30"},
    {"name": "馬木", "birthdate": "1991-08-08"},
    {"name": "どん兵衛", "birthdate": "1983-09-15"},
    {"name": "竹内", "birthdate": "1986-10-22"},
    {"name": "東川", "birthdate": "1990-11-29"},
    {"name": "ケンイチ", "birthdate": "1984-12-31"},
    {"name": "mori富士", "birthdate": "1993-01-17"},
    {"name": "馬場園", "birthdate": "1995-02-25"},
    {"name": "エンガワ", "birthdate": "1987-03-05"},
    {"name": "パカ縄", "birthdate": "1996-04-10"},
    {"name": "裏", "birthdate": "1989-05-28"},
    {"name": "KIMURA", "birthdate": "1991-06-30"}
]

# 運勢、ラッキーアイテム、注意喚起のリストを定義します
fortunes = ["最吉", "超吉", "大吉", "半吉", "チョビ吉", "仙吉", "寸吉", "ギャン吉", "ドン底", "極楽", "微吉", "ホームラン"]
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
@app.route('/')
def index():
    # リストからランダムに15人を選びます
    selected_people = random.sample(people, 15)

    # WebページのHTMLテンプレートを定義します
    html_template = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>本日のヒーロー</title>
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
            #roulette-container {
                margin-top: 100px;
            }
            #roulette {
                font-size: 3em;
                margin: 20px auto;
                height: 100px;
                line-height: 100px;
                border: 5px solid #ffd700;
                padding: 0 40px;
                border-radius: 10px;
                background-color: rgba(0, 0, 0, 0.8);
                box-shadow: 0 0 30px #ffd700;
                animation: rotate 1s infinite linear;
                color: #ffd700;
                letter-spacing: 2px;
            }
            @keyframes rotate { 0% { transform: rotateY(0deg); } 100% { transform: rotateY(360deg); } }
            .highlight { animation: pop 1s ease forwards, glow 1s infinite alternate; }
            @keyframes pop { 0% { transform: scale(1); } 100% { transform: scale(3); color: #ff69b4; } }
            @keyframes glow { 0% { text-shadow: 0 0 20px #ffd700; } 100% { text-shadow: 0 0 60px #ffd700; } }
            button {
                font-size: 1.5em;
                padding: 15px 30px;
                margin: 20px;
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
            .result-container {
                margin-top: 20px;
                font-size: 1.5em;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px #000;
                background-color: rgba(0, 0, 0, 0.8);
                color: #ffd700;
                text-shadow: 0 0 10px #ffd700;
                animation: reveal 2s ease forwards;
                max-width: 90%;
                word-wrap: break-word;
            }
            @keyframes reveal { 0% { opacity: 0; transform: translateY(-10px); } 100% { opacity: 1; transform: translateY(0); } }
            h1 {
                font-size: 4em;
                margin-top: 50px;
                color: #ffd700;
                text-shadow: 0 0 20px #fff, 0 0 30px #ffd700;
                animation: title-glow 2s infinite alternate;
            }
            @keyframes title-glow { 0% { text-shadow: 0 0 20px #fff; } 100% { text-shadow: 0 0 80px #ffd700; } }
            .shooting-star {
                position: absolute;
                top: -10%;
                left: 110%;
                width: 5px;
                height: 5px;
                background: white;
                box-shadow: 0 0 20px white;
                animation: shooting-star 2s infinite linear;
            }
            .shooting-star:nth-child(2) { animation-delay: 1s; }
            .shooting-star:nth-child(3) { animation-delay: 2s; }
            @keyframes shooting-star { 0% { transform: translateX(100%) translateY(-100%); } 100% { transform: translateX(-100%) translateY(100%); } }
        </style>
    </head>
    <body>
        <div id="roulette-container">
            <h1>本日のヒーロー</h1>
            <div id="roulette">---</div>
            <button onclick="startRoulette()">スタート</button>
            <button onclick="stopRoulette()">ストップ</button>
        </div>
        <div id="fortune" class="result-container"></div>
        <div id="zodiac" class="result-container"></div>
        <div id="lucky-item" class="result-container"></div>
        <div id="warning" class="result-container"></div>
        <div class="shooting-star"></div>
        <div class="shooting-star"></div>
        <div class="shooting-star"></div>

        <script>
            const people = {{ selected_people | tojson }};
            const fortunes = {{ fortunes | tojson }};
            const luckyItems = {{ lucky_items | tojson }};
            const warnings = {{ warnings | tojson }};
            let rouletteInterval, isRouletteRunning = false;

            function startRoulette() {
                if (rouletteInterval) clearInterval(rouletteInterval);
                let index = 0;
                isRouletteRunning = true;
                document.body.classList.add('flash');
                rouletteInterval = setInterval(() => {
                    document.getElementById('roulette').innerText = people[index].name;
                    index = (index + 1) % people.length;
                }, 50);
            }

            function stopRoulette() {
                if (rouletteInterval) clearInterval(rouletteInterval);
                if (isRouletteRunning) {
                    const selectedPerson = people[Math.floor(Math.random() * people.length)];
                    displayResult('fortune', `${selectedPerson.name}さんの運勢は: ${fortunes[Math.floor(Math.random() * fortunes.length)]}`);
                    displayResult('zodiac', `あなたの星座は: ${getZodiacSign(selectedPerson.birthdate)}`);
                    displayResult('lucky-item', `今日のラッキーアイテム: ${luckyItems[Math.floor(Math.random() * luckyItems.length)]}`);
                    displayResult('warning', `本日の注意喚起: ${warnings[Math.floor(Math.random() * warnings.length)]}`);
                    document.getElementById('roulette').innerText = selectedPerson.name;
                    document.getElementById('roulette').classList.add('highlight');
                    setTimeout(() => document.getElementById('roulette').classList.remove('highlight'), 2000);
                    isRouletteRunning = false;
                    document.body.classList.remove('flash');

                    // 結果をデータベースに保存
                    saveResult(selectedPerson.name, selectedPerson.birthdate, fortunes, luckyItems, warnings);
                }
            }

            function displayResult(elementId, text) {
                document.getElementById(elementId).innerHTML = `<h2>${text}</h2>`;
            }

            function getZodiacSign(birthdate) {
                const [month, day] = new Date(birthdate).toLocaleDateString('ja-JP').split('/').slice(1);
                const zodiacRanges = [
                    [[3, 21], [4, 19], "牡羊座"], [[4, 20], [5, 20], "牡牛座"], [[5, 21], [6, 20], "双子座"],
                    [[6, 21], [7, 22], "蟹座"], [[7, 23], [8, 22], "獅子座"], [[8, 23], [9, 22], "乙女座"],
                    [[9, 23], [10, 22], "天秤座"], [[10, 23], [11, 21], "蠍座"], [[11, 22], [12, 21], "射手座"],
                    [[12, 22], [1, 19], "山羊座"], [[1, 20], [2, 18], "水瓶座"], [[2, 19], [3, 20], "魚座"]
                ];
                return zodiacRanges.find(([start, end]) => (month, day) >= start && (month, day) <= end)[2];
            }

            function saveResult(name, birthdate, fortunes, luckyItems, warnings) {
                const fortune = fortunes[Math.floor(Math.random() * fortunes.length)];
                const luckyItem = luckyItems[Math.floor(Math.random() * luckyItems.length)];
                const warning = warnings[Math.floor(Math.random() * warnings.length)];
                const zodiacSign = getZodiacSign(birthdate);

                // AJAXリクエストでサーバーにデータを送信
                fetch('/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, birthdate, zodiacSign, fortune, luckyItem, warning }),
                });
            }
        </script>
    </body>
    </html>
    """

    return render_template_string(html_template, selected_people=selected_people, fortunes=fortunes, lucky_items=lucky_items, warnings=warnings)

# POSTリクエストで結果を保存
@app.route('/save', methods=['POST'])
def save_result():
    data = request.get_json()
    new_result = FortuneHistory(
        name=data['name'],
        birthdate=data['birthdate'],
        zodiac_sign=data['zodiacSign'],
        fortune=data['fortune'],
        lucky_item=data['luckyItem'],
        warning=data['warning']
    )
    db.session.add(new_result)
    db.session.commit()
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
