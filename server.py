# server.py

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotionDetector():
    # JS からは GET パラメータ名 "textToAnalyze" で来る想定
    text = request.args.get('textToAnalyze', '').strip()

    # 入力チェック：空文字はエラー文だけ返す（ステータス 200）
    if not text:
        return "Invalid text! Please try again!"

    result = emotion_detector(text)

    # emotion_detector が全キー None を返す場合もエラー文だけ返す（ステータス 200）
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    # 正常時は narrative だけを返す（ステータス 200）
    narrative = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return narrative

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
