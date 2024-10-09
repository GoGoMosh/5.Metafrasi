#from ctypes import windll, Structure, c_long, byref
from function import *
import time
import string
import logging


# Чтобы не выводилась постоянно сообщение о CUDA от Easyocr
logging.getLogger('easyocr').setLevel(logging.ERROR)

# Определяем размеры и положение области экрана для скриншота
monitor = {
    "top": 100,  # Верхняя граница (координата Y)
    "left": 100,  # Левая граница (координата X)
    "width": 800,  # Ширина области
    "height": 120  # Высота области
}

# Флаг для запуска/паузы захвата экрана
is_running = True
i = 0

# Основной цикл программы
try:
    while True:

        # Изменение имени файла сохраняемого изображения с текстом от 0 до 2
        i = (i + 1) % 3

        # Захват экрана каждые 3 секунды, если захват запущен
        if is_running:
            capture_and_process_screen(monitor, i)
            img_for_read = cv2.imread(f'screenshot_{i}.png')
            img_resized = cv2.resize(img_for_read, (343, 40))
            try:
                print(text_recognition(img_resized)[0].translate(str.maketrans('', '', string.punctuation)))
            except IndexError:
                print('Empty')
                pass
            time.sleep(4)

        # Читаем клавиатуру с небольшой задержкой (100) для правильной обработки клавиш
        key = cv2.waitKey(100) & 0xFF

        # Если нажата клавиша 'p', ставим захват на паузу, иначе снимаем паузу
        if key in [80, 112]:
            if is_running:
                is_running = False
                print("Захват экрана поставлен на паузу")
            else:
                is_running = True
                print("Захват экрана паузы снят")

        # Выход из программы при нажатии ESC
        if key == 27:  # 27 - это код клавиши ESC
            print("Завершение программы")
            break

# Закрытие программы
finally:

    # Удаление окон openCV
    cv2.destroyAllWindows()

    # Удаление изображения
    deleting_img()