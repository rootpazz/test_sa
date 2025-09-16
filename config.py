import torch
import warnings

# Игнорировать предупреждения MPS для чистоты вывода (опционально)
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.functional")

# Настройка устройства (используем MPS для Mac с чипом M1/M2/M3, если доступно)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Модель перевода
MODEL_NAME = 'Helsinki-NLP/opus-mt-ru-en'
# MODEL_NAME = 'Helsinki-NLP/opus-mt-ru-es'

# API-ключ для ElevenLabsы
ELEVEN_LABS_API_KEY = " "

# Настройки голоса
VOICE_NAME = "Rachel"
