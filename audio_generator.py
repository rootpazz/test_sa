import os
import tempfile
from elevenlabs import ElevenLabs, stream as elevenlabs_stream
from config import ELEVEN_LABS_API_KEY, VOICE_NAME
import threading
import queue
import io
import subprocess


class AudioGenerator:
    def __init__(self):
        self.client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)
        self.mpv_available = self._check_mpv()
        self.pyaudio_available = self._check_pyaudio()

    def _check_mpv(self):
        """Проверяет доступность mpv"""
        try:
            result = subprocess.run(['which', 'mpv'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def _check_pyaudio(self):
        """Проверяет доступность pyaudio"""
        try:
            import pyaudio
            return True
        except ImportError:
            return False

    def generate_and_play_stream(self, text):
        """Стриминг аудио для максимальной скорости"""
        try:
            # Генерируем аудио со стримингом - НОВЫЙ API
            audio_stream = self.client.text_to_speech.convert_as_stream(
                voice_id=VOICE_NAME,
                text=text,
                model_id="eleven_turbo_v2_5",  # Обновленная модель
                optimize_streaming_latency=5,  # Максимальная оптимизация (1-5)
                output_format="mp3_44100_128"
            )

            if self.pyaudio_available:
                # САМЫЙ БЫСТРЫЙ метод - прямой стриминг через PyAudio
                self._stream_with_pyaudio(audio_stream)
            elif self.mpv_available:
                # Второй по скорости - через mpv
                elevenlabs_stream(audio_stream)
            else:
                # Третий вариант - через afplay со стримингом
                self._stream_with_afplay(audio_stream)

        except Exception as e:
            # print(f"Ошибка при стриминге аудио: {e}")
            # Fallback на метод через файл
            self.generate_and_play_file(text)

    def _stream_with_pyaudio(self, audio_stream):
        """Прямой стриминг через PyAudio - максимальная скорость"""
        import pyaudio
        from pydub import AudioSegment
        from pydub.playback import play
        import threading

        # Создаем очередь для буферизации
        audio_queue = queue.Queue(maxsize=5)

        def producer():
            """Поток для получения аудио чанков"""
            try:
                for chunk in audio_stream:
                    if chunk:
                        audio_queue.put(chunk)
                audio_queue.put(None)  # Сигнал окончания
            except Exception as e:
                print(f"Ошибка в producer: {e}")
                audio_queue.put(None)

        def consumer():
            """Поток для воспроизведения аудио"""
            p = pyaudio.PyAudio()
            stream = None

            try:
                first_chunk = True
                buffer = io.BytesIO()

                while True:
                    chunk = audio_queue.get()
                    if chunk is None:
                        break

                    buffer.write(chunk)

                    # Начинаем воспроизведение после первого чанка
                    if first_chunk and buffer.tell() > 512:
                        first_chunk = False
                        buffer.seek(0)

                        # Определяем формат аудио
                        audio = AudioSegment.from_mp3(buffer)

                        # Открываем поток PyAudio
                        stream = p.open(
                            format=p.get_format_from_width(audio.sample_width),
                            channels=audio.channels,
                            rate=audio.frame_rate,
                            output=True,
                            frames_per_buffer=512  # Маленький буфер для низкой латентности
                        )

                        # Воспроизводим первый чанк
                        stream.write(audio.raw_data)
                        buffer = io.BytesIO()

                    elif not first_chunk and buffer.tell() > 512:
                        buffer.seek(0)
                        audio_chunk = AudioSegment.from_mp3(buffer)
                        stream.write(audio_chunk.raw_data)
                        buffer = io.BytesIO()

                # Воспроизводим остатки
                if buffer.tell() > 0:
                    buffer.seek(0)
                    audio_chunk = AudioSegment.from_mp3(buffer)
                    if stream:
                        stream.write(audio_chunk.raw_data)

            except Exception as e:
                print(f"Ошибка в consumer: {e}")
            finally:
                if stream:
                    stream.stop_stream()
                    stream.close()
                p.terminate()

        # Запускаем потоки
        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        # Ждем завершения
        producer_thread.join()
        consumer_thread.join()

    def _stream_with_afplay(self, audio_stream):
        """Стриминг через afplay (без mpv)"""
        # Собираем поток в память
        audio_data = io.BytesIO()
        for chunk in audio_stream:
            audio_data.write(chunk)

        # Воспроизводим через pipe
        audio_data.seek(0)
        process = subprocess.Popen(['afplay', '-'], stdin=subprocess.PIPE)
        process.communicate(input=audio_data.read())

    def generate_and_play_file(self, text):
        """Резервный метод через файл"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
                output_file = temp_file.name

         
                audio_generator = self.client.text_to_speech.convert(
                    voice_id=VOICE_NAME,
                    text=text,
                    model_id="eleven_turbo_v2",
                    output_format="mp3_44100_128"
                )

                with open(output_file, "wb") as f:
                    for chunk in audio_generator:
                        f.write(chunk)
                os.system(f"afplay {output_file}")
        except Exception as e:
            print(f"Ошибка при создании аудиофайла: {e}")
            raise e

    def generate_and_play(self, text):
        """Основной метод для обратной совместимости"""
        self.generate_and_play_stream(text)
