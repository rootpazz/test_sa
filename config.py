import torch
import warnings
import os

# Игнорировать предупреждения MPS
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.functional")

# Настройка устройства
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Оптимизации для MPS
if device.type == "mps":
    # Включаем оптимизации памяти
    os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

# Модель перевода 
MODEL_NAME = 'Helsinki-NLP/opus-mt-ru-en'

# API-ключ для ElevenLabs
ELEVEN_LABS_API_KEY = ""  # Вставьте ваш API ключ

# Голос для ElevenLabs - теперь нужен voice_id, а не имя
VOICE_NAME = "pNInz6obpgDQGcFmaJgB"  # Adam voice ID, замените при желании
