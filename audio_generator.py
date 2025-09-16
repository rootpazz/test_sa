import os
import tempfile
from elevenlabs.client import ElevenLabs
from config import ELEVEN_LABS_API_KEY, VOICE_NAME


class AudioGenerator:
    def __init__(self):
        self.client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

    def generate_and_play(self, text):
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
                output_file = temp_file.name
                # Генерация аудио с помощью ElevenLabs
                audio = self.client.generate(
                    text=text,
                    voice=VOICE_NAME
                )
                # Сохранение аудио во временный файл
                with open(output_file, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)
                print(f"Аудио временно сохранено как {output_file}")
                # Воспроизведение
                os.system(f"afplay {output_file}")
                print("Воспроизведение завершено.")
            # Файл автоматически удаляется после закрытия контекста tempfile
        except Exception as e:
            print(f"Ошибка при создании или воспроизведении аудиофайла через ElevenLabs: {e}")
            raise e
