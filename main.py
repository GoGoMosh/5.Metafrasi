"""
# Функция для захвата экрана и обработки через OpenCV
def capture_and_process_screen():
    with mss.mss() as sct:
        # Захват области экрана
        screenshot = sct.grab({
        "top": 100,  # Верхняя граница (координата Y)
        "left": 100,  # Левая граница (координата X)
        "width": 800,  # Ширина области
        "height": 600  # Высота области
        })

        # Преобразуем изображение в формат, который понимает OpenCV (numpy array)
        img = np.array(screenshot)

        # Преобразуем BGR изображение в RGB (опционально)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Показываем захваченный скриншот
        cv2.imshow('Screen Capture', img)

        # Сохраняем изображение (по желанию)
        cv2.imwrite(f'screenshot_{time.time()}.png', img)

        img_for_read = cv2.imread(img)
        img_resized = cv2.resize(img_for_read, (343, 40))
        print(text_recognition(img_resized)[0].translate(str.maketrans('', '', string.punctuation)))

def text_recognition(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0)

    return result

def main():

    # Основной цикл программы
    try:
        while True:

            # Флаг для запуска/паузы захвата экрана
            is_running = False

            # Читаем клавиатуру
            key = cv2.waitKey(1) & 0xFF

            # Если нажата клавиша 's', запускаем или возобновляем захват
            if key == ord('s'):
                is_running = True
                print("Захват экрана запущен")

            # Если нажата клавиша 'p', ставим захват на паузу
            if key == ord('p'):
                is_running = False
                print("Захват экрана поставлен на паузу")

            # Захват экрана каждые 3 секунды, если захват запущен
            if is_running:
                capture_and_process_screen()
                time.sleep(3)

            # Выход из программы при нажатии ESC
            if key == 27:  # 27 - это код клавиши ESC
                break

    finally:
        cv2.destroyAllWindows()
"""
import cv2
import numpy as np
import easyocr
import mss
import time

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
        cv2.imwrite(f'screenshot_{++i}.png', img)


# Основной цикл программы
try:
    while True:
        # Захват экрана каждые 3 секунды, если захват запущен
        if is_running:
            capture_and_process_screen()
            time.sleep(3)

        # Читаем клавиатуру с небольшой задержкой для правильной обработки клавиш
        key = cv2.waitKey(100) & 0xFF

        # Если нажата клавиша 's', запускаем или возобновляем захват

        # Если нажата клавиша 'p', ставим захват на паузу
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
