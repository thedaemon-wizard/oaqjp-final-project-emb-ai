import requests
import json

def emotion_detector(text_to_analyze):
    """
    Watson NLP Emotion Predict を呼び出し、
    各感情スコアと支配的な感情を含む dict を返します。

    ステータスコードが 400 の場合は全キーを None にして返す。
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    # POST リクエストを送信
    resp = requests.post(url, headers=headers, json=payload)

    # 1) 400 (Bad Request) → 全キー None
    if resp.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    # 2) それ以外は例外を投げる
    resp.raise_for_status()

    # 3) レスポンスを dict に変換
    result = resp.json()

    # 4) 感情スコア抽出（レスポンス構造に合わせて）
    emotions = result["emotionPredictions"][0]["emotion"]
    anger_score   = emotions.get("anger",   0.0)
    disgust_score = emotions.get("disgust", 0.0)
    fear_score    = emotions.get("fear",    0.0)
    joy_score     = emotions.get("joy",     0.0)
    sadness_score = emotions.get("sadness", 0.0)

    # 5) 最高スコアの感情を決定
    dominant_emotion = max(
        ("anger", anger_score),
        ("disgust", disgust_score),
        ("fear", fear_score),
        ("joy", joy_score),
        ("sadness", sadness_score),
        key=lambda x: x[1]
    )[0]

    # 6) 結果を返却
    return {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
        "dominant_emotion": dominant_emotion
    }
