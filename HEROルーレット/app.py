from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# SQLiteデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fortune.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースオブジェクトの初期化
db = SQLAlchemy(app)

# データベースモデルをインポート
from models import FortuneHistory

# 初回実行時にデータベースを作成
with app.app_context():
    db.create_all()

# 運勢、ラッキーアイテム、注意喚起のリストを定義
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

# ホームページのルート設定
@app.route('/')
def index():
    return render_template('index.html')

# POSTリクエストで結果を保存
@app.route('/save', methods=['POST'])
def save_result():
    data = request.get_json()  # リクエストからJSONデータを取得

    # データベースに新しい結果を保存
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

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
