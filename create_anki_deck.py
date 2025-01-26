import os
import base64
import re
import requests

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def natural_sort_key(filename):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]

def create_deck(deck_name):
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    print(f"Create Deck Response for {deck_name}: {response.json()}")
    return response.json()

def store_media_file(filename, filepath):
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": filename,
            "data": data,
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    print(f"Uploading {filename}: {response.json()}")
    return response.json()

def add_note(deck_name, model_name, front_html, back_html):
    payload = {
        "action": "addNotes",
        "version": 6,
        "params": {
            "notes": [
                {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {
                        "表面": front_html,
                        "裏面": back_html,
                    },
                    "tags": ["auto-generated"],
                }
            ]
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    print(f"Add Note Response for {deck_name}: {response.json()}")
    return response.json()

def create_anki_deck(deck_name, image_dir, model_name="基本"):
    create_deck(deck_name)

    files = sorted(os.listdir(image_dir), key=natural_sort_key)  # 自然順でソート
    question_files = [f for f in files if f.startswith("Q_") and f.endswith(".png")]
    answer_files = [f for f in files if f.startswith("A_") and f.endswith(".png")]

    for q_file, a_file in zip(question_files, answer_files):
        q_path = os.path.join(image_dir, q_file)
        a_path = os.path.join(image_dir, a_file)

        store_media_file(q_file, q_path)
        store_media_file(a_file, a_path)

        front_html = f"<img src='{q_file}'>"
        back_html = f"<img src='{a_file}'>"

        add_note(deck_name, model_name, front_html, back_html)

if __name__ == "__main__":
    # A～X に対応するフォルダとデッキ名を指定
    DECK_NAMES = ["消化器", "肝胆膵", "循環器", "代謝・内分泌", "腎臓", "免疫・膠原病", "血液", "感染症", "呼吸器", "神経", "救急・中毒", "輸液", "麻酔", "老年", "小児科", "産婦人科", "乳腺", "眼科", "耳鼻咽喉科", "整形外科", "精神科", "皮膚科", "泌尿器", "放射線科"]
    LETTERS = [chr(c) for c in range(ord('A'), ord('X') + 1)]
    BASE_IMG_DIR = "img"

    for letter, deck_name in zip(LETTERS, DECK_NAMES):
        image_dir = os.path.join(BASE_IMG_DIR, letter)  # 各アルファベットに対応するフォルダ

        if not os.path.exists(image_dir):
            print(f"Warning: {image_dir} does not exist. Skipping.")
            continue

        create_anki_deck(deck_name, image_dir)
        print(f"Deck {deck_name} ({letter}) creation complete.")