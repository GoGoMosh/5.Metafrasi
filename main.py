from ctypes import windll, Structure, c_long, byref
import cv2
import numpy as np
import easyocr
import mss
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

# Функция для поиска текста на фото с помощью OCR
def text_recognition(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0)

    return result


# Функция для захвата экрана и обработки через OpenCV
def capture_and_process_screen():
    with mss.mss() as sct:
        # Захват области экрана
        screenshot = sct.grab(monitor)

        # Преобразуем изображение в формат, который понимает OpenCV (numpy array)
        img = np.array(screenshot)

        # Преобразуем BGR изображение в RGB (опционально)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Показываем захваченный скриншот
        cv2.imshow('Screen Capture', img)

        # Сохраняем изображение (по желанию)
        cv2.imwrite(f'screenshot_{i}.png', img)


# Основной цикл программы
try:
    while True:
        i = 0
        if i == 3:
            i = 0
        else:
            i += 1
        # Захват экрана каждые 3 секунды, если захват запущен
        if is_running:
            capture_and_process_screen()
            img_for_read = cv2.imread(f'screenshot_{i}.png')
            img_resized = cv2.resize(img_for_read, (343, 40))
            try:
                print(text_recognition(img_resized)[0].translate(str.maketrans('', '', string.punctuation)))
            except IndexError:
                print('Empty')
                continue
            time.sleep(4)

        # Читаем клавиатуру с небольшой задержкой (100) для правильной обработки клавиш
        key = cv2.waitKey(100) & 0xFF

        # Если нажата клавиша 'p', ставим захват на паузу, иначе снимаем паузу
        if key == ord('p'):
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

finally:
    cv2.destroyAllWindows()
