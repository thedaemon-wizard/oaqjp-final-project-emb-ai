import requests
import json

def emotion_detector(text_to_analyze):
    """
    Watson NLP Emotion Predict サービスを呼び出し、
    各感情スコアと支配的な感情を含む dict を返します。
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
    resp.raise_for_status()

    # 1. レスポンステキストを dict に変換
    result = json.loads(resp.text)

    # 2. 必要な感情スコアを抽出
    #    （レスポンス構造に合わせてパスを調整してください）
    #    例: result["emotionPredictions"]["emotion"] = {"anger": .., "disgust": .., ...}
    emotions = result["emotionPredictions"][0]["emotion"]
    anger_score   = emotions.get("anger",   0.0)
    disgust_score = emotions.get("disgust", 0.0)
    fear_score    = emotions.get("fear",    0.0)
    joy_score     = emotions.get("joy",     0.0)
    sadness_score = emotions.get("sadness", 0.0)

    # 3. 最高スコアの感情を決定
    dominant_emotion = max(
        ("anger", anger_score),
        ("disgust", disgust_score),
        ("fear", fear_score),
        ("joy", joy_score),
        ("sadness", sadness_score),
        key=lambda x: x[1]
    )[0]

    # 4. フォーマットして返却
    return {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
        "dominant_emotion": dominant_emotion
    }


if __name__ == "__main__":
    # テスト実行
    sample = "I am so happy I am doing this"
    formatted = emotion_detector(sample)
    print("Input :", sample)
    print("Output:", formatted)
