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
            # Загружаем модель с оптимизациями
            self.tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
            self.model = MarianMTModel.from_pretrained(MODEL_NAME).to(device)

            # Включаем eval mode для ускорения
            self.model.eval()

            # Компилируем модель для MPS 
            if device.type == "mps":
                self.model = torch.compile(self.model, mode="reduce-overhead")

            print("Модель перевода успешно загружена и оптимизирована.")
        except Exception as e:
            print(f"Ошибка при загрузке модели перевода: {e}")
            raise e

    @torch.no_grad()  # Отключаем градиенты для ускорения
    def translate(self, text):
        try:
            # Токенизация с ограничением длины
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128  # Ограничиваем длину для скорости
            ).to(device)

            # Генерация с оптимизированными параметрами
            translated = self.model.generate(
                **inputs,
                max_length=128,
                num_beams=1,  # Отключаем beam search для скорости
                do_sample=False,
                early_stopping=True
            )

            translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            return translated_text
        except Exception as e:
            print(f"Ошибка при переводе: {e}")
            return text  # Возвращаем исходный текст при ошибке
