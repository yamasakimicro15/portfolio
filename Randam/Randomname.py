from flask import Flask, render_template_string
import random

app = Flask(__name__)


# 人の名前のリストを定義します
names = ["山崎", "山田", "山内", "木内", "とおる", "馬木", "どん兵衛", "竹内", "東川", "ケンイチ","mori富士"]

@app.route('/')
def index():
    # ランダムに選択する名前の数を指定します
    num_to_select = 11

    # namesリストから指定した数(num_to_select)の名前をランダムに選びます
    selected_names = random.sample(names, num_to_select)

    # HTMLテンプレート
    html_template = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>ルーレット - 世界の命運をジャッジする者は</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                text-align: center;
                background: url('https://example.com/background.jpg') no-repeat center center fixed;
                background-size: cover;
                color: white;
                margin: 0;
                padding: 0;
                overflow: hidden;
                transition: background-color 0.5s;
            }
            body.flash {
                animation: flash 0.5s alternate infinite;
            }
            @keyframes flash {
                0% { background-color: rgba(255, 0, 0, 0.5); }
                100% { background-color: rgba(0, 0, 255, 0.5); }
            }
            #roulette-container {
                margin-top: 100px;
            }
            #roulette {
                font-size: 3em;
                margin: 20px auto;
                height: 100px;
                line-height: 100px;
                border: 5px solid #fff;
                display: inline-block;
                padding: 0 40px;
                border-radius: 10px;
                background-color: rgba(0, 0, 0, 0.7);
                box-shadow: 0 0 10px #000;
                animation: pulse 1s infinite;
                transition: transform 0.5s, font-size 0.5s;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            button {
                font-size: 1.5em;
                padding: 15px 30px;
                margin: 20px;
                border: none;
                border-radius: 10px;
                background-color: #28a745;
                color: white;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #218838;
            }
            #selected-names, #all-names {
                margin-top: 40px;
                font-size: 1.2em;
                background-color: rgba(0, 0, 0, 0.7);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px #000;
                display: inline-block;
                text-align: left;
            }
            h1 {
                font-size: 4em;
                margin-top: 50px;
                text-shadow: 0 0 10px #000;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                padding: 5px 0;
            }
        </style>
    </head>
    <body>
        <div id="roulette-container">
            <h1>世界の命運をジャッジするルーレット</h1>
            <div id="roulette">---</div>
            <br>
            <button onclick="startRoulette()">スタート</button>
            <button onclick="stopRoulette()">ストップ</button>
        </div>
        <div id="selected-names"></div>
        <div id="all-names"></div>

        <script>
            const names = {{ selected_names | tojson }};
            let rouletteInterval;
            let selectedOrder = [];
            let isRouletteRunning = false;
            let speed = 50;

            function startRoulette() {
                if (rouletteInterval) {
                    clearInterval(rouletteInterval);
                }
                document.body.classList.add('flash');
                let index = 0;
                isRouletteRunning = true;
                speed = 50;
                rouletteInterval = setInterval(() => {
                    document.getElementById('roulette').innerText = names[index];
                    index = (index + 1) % names.length;
                }, speed); // ルーレットのスピードを初期設定
            }

            function stopRoulette() {
                if (rouletteInterval) {
                    clearInterval(rouletteInterval);
                    rouletteInterval = null;
                    const selectedName = document.getElementById('roulette').innerText;
                    if (isRouletteRunning && !selectedOrder.includes(selectedName)) {
                        selectedOrder.push(selectedName);
                    }
                    isRouletteRunning = false;
                    document.body.classList.remove('flash');
                    displaySelectedNames();
                    // アニメーションで名前を強調表示
                    const rouletteDiv = document.getElementById('roulette');
                    rouletteDiv.style.transform = 'scale(1.5)';
                    rouletteDiv.style.fontSize = '4em';
                    setTimeout(() => {
                        rouletteDiv.style.transform = '';
                        rouletteDiv.style.fontSize = '';
                    }, 1000);
                }
            }

            function displaySelectedNames() {
                const selectedNamesDiv = document.getElementById('selected-names');
                selectedNamesDiv.innerHTML = '<h2>選択された順番</h2><ul>' +
                    selectedOrder.map(name => '<li>' + name + '</li>').join('') +
                    '</ul>';

                const remainingNames = names.filter(name => !selectedOrder.includes(name));
                const allNamesDiv = document.getElementById('all-names');
                allNamesDiv.innerHTML = '<h2>全ての名前</h2><ul>' +
                    selectedOrder.concat(remainingNames).map(name => '<li>' + name + '</li>').join('') +
                    '</ul>';
            }
        </script>
    </body>
    </html>
    """

    # テンプレートに選ばれた名前を渡してレンダリングします
    return render_template_string(html_template, selected_names=selected_names)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)