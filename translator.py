import torch
from transformers import MarianTokenizer, MarianMTModel
from config import device, MODEL_NAME


class Translator:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            self.tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
            self.model = MarianMTModel.from_pretrained(MODEL_NAME).to(device)
            print("Модель перевода успешно загружена.")
        except Exception as e:
            print(f"Ошибка при загрузке модели перевода: {e}")
            raise e

    def translate(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True).to(device)
            translated = self.model.generate(**inputs)
            translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            return translated_text
        except Exception as e:
            print(f"Ошибка при переводе: {e}")
            raise e
