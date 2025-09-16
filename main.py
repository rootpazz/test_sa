from config import device
from translator import Translator
from audio_generator import AudioGenerator


def main():
    print(f"Используется устройство: {device}")

    # Инициализация компонентов
    try:
        translator = Translator()
        audio_generator = AudioGenerator()
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return

    # Настройка перевода
    translation_enabled = True
    print(f"Перевод: {'включен' if translation_enabled else 'отключен'}")

    # Интерактивный цикл
    print("\nКоманды:")
    print("- Введите текст для обработки")
    print("- 'перевод вкл' - включить перевод")
    print("- 'перевод выкл' - отключить перевод")
    print("- 'статус' - показать текущие настройки")
    print("- 'выход' - завершить программу")

    while True:
        text = input("\nВвод: ").strip()

        # Команды управления
        if text.lower() in ["выход", "exit", "quit"]:
            print("Программа завершена.")
            break
        elif text.lower() in ["перевод вкл", "translation on"]:
            translation_enabled = True
            print("Перевод включен.")
            continue
        elif text.lower() in ["перевод выкл", "translation off"]:
            translation_enabled = False
            print("Перевод отключен.")
            continue
        elif text.lower() in ["статус", "status"]:
            print(f"Перевод: {'включен' if translation_enabled else 'отключен'}")
            continue
        elif not text:
            print("Пожалуйста, введите текст или команду.")
            continue

        # Обработка текста
        try:
            if translation_enabled:
                translated_text = translator.translate(text)
                print("Перевод:", translated_text)
                final_text = translated_text
            else:
                print("Исходный текст:", text)
                final_text = text
        except Exception:
            continue

        # Генерация и воспроизведение аудио
        try:
            audio_generator.generate_and_play(final_text)
        except Exception:
            continue


if __name__ == "__main__":
    main()
