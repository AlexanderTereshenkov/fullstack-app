import easyocr
import requests
import numpy as np
from PIL import Image
import io


reader = easyocr.Reader(['ru', 'en'], gpu=False)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen3.5:9b"


def extract_event_data_from_image(image_bytes: bytes) -> dict:
    try:
        pil_image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}")
  
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')

    image_np = np.array(pil_image)

    result = reader.readtext(image_np, detail=0)
    ocr_text = " ".join(result)

    system_prompt = f"""
        Ты — ассистент для парсинга афиш мероприятий.
        Проанализируй текст и верни ТОЛЬКО JSON без лишнего текста.
        Следуй строго этой схеме:
            {{
                "title": "Название события",
                "date": "Дата в формате DD.MM.YYYY",
                "time": "Время в формате HH:MM",
                "location": "Место проведения",
                "description": "Краткое описание. Придумай пару литературных предложений."
            }}
        Если какое-то поле не удалось определить, оставь его пустой строкой.
        Вот текст:
        {ocr_text}
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": system_prompt,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 1.0,           # случайность ответа (0–2)
            "top_p": 1.00,                # nucleus sampling (0–1)
            "top_k": 20,                  # ограничение на k самых вероятных токенов
            "min_p": 0.0,                 # минимальная вероятность для отсечения
            "presence_penalty": 2.0,      # штраф за появление новых токенов
            "repetition_penalty": 1.0     # штраф за повторения
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code != 200:
        raise Exception(f"LLM ошибка: {response.text}")

    llm_output = response.json().get("response", "")
  
    import json
    try:
        return json.loads(llm_output)
    except:
        return {"title": "", "date": "", "time": "", "location": "", "description": ""}
    
