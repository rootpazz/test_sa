from config import device
from translator import Translator
from audio_generator import AudioGenerator
import threading
import queue
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")


def main():
    print(f"Используется устройство: {device}")

    # Инициализация компонентов
    try:
        translator = Translator()
        audio_generator = AudioGenerator()
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return

    # Настройка
    translation_enabled = True
    use_streaming = True  # Использовать стриминг для скорости

    print(f"Перевод: {'включен' if translation_enabled else 'отключен'}")
    print(f"Стриминг: {'включен' if use_streaming else 'отключен'}")

    # Интерактивный цикл
    print("\nКоманды:")
    print("- Введите текст для обработки")
    print("- 'перевод вкл/выкл' - управление переводом")
    print("- 'стриминг вкл/выкл' - управление стримингом")
    print("- 'статус' - показать настройки")
    print("- 'выход' - завершить программу")

    # Очередь для параллельной обработки
    audio_queue = queue.Queue()

    def audio_worker():
        """Воркер для асинхронного воспроизведения аудио"""
        while True:
            item = audio_queue.get()
            if item is None:
                break
            text, use_stream = item
            if use_stream:
                audio_generator.generate_and_play_stream(text)
            else:
                audio_generator.generate_and_play_file(text)
            audio_queue.task_done()

    # Запускаем воркер в отдельном потоке
    audio_thread = threading.Thread(target=audio_worker, daemon=True)
    audio_thread.start()

    while True:
        text = input("\nВвод: ").strip()

        # Команды управления
        if text.lower() in ["выход", "exit", "quit"]:
            audio_queue.put(None)  # Сигнал для завершения воркера
            print("Программа завершена.")
            break
        elif text.lower() == "перевод вкл":
            translation_enabled = True
            print("Перевод включен.")
            continue
        elif text.lower() == "перевод выкл":
            translation_enabled = False
            print("Перевод отключен.")
            continue
        elif text.lower() == "стриминг вкл":
            use_streaming = True
            print("Стриминг включен.")
            continue
        elif text.lower() == "стриминг выкл":
            use_streaming = False
            print("Стриминг отключен.")
            continue
        elif text.lower() == "статус":
            print(f"Перевод: {'включен' if translation_enabled else 'отключен'}")
            print(f"Стриминг: {'включен' if use_streaming else 'отключен'}")
            continue
        elif not text:
            print("Пожалуйста, введите текст или команду.")
            continue

        # Обработка текста
        try:
            if translation_enabled:
                # Начинаем перевод
                translated_text = translator.translate(text)
                print("Перевод:", translated_text)
                final_text = translated_text
            else:
                print("Исходный текст:", text)
                final_text = text

            # Отправляем в очередь для параллельного воспроизведения
            audio_queue.put((final_text, use_streaming))

        except Exception as e:
            print(f"Ошибка обработки: {e}")
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n ступай! 👋")
