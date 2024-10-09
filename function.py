import numpy as np
import easyocr
import mss
import pathlib
import cv2

# Функция для поиска текста на фото с помощью OCR
def text_recognition(file_path):
    reader = easyocr.Reader(['ru'])
    result = reader.readtext(file_path, detail=0)

    return result

# Функция для захвата экрана и обработки через OpenCV
def capture_and_process_screen(monitor, i):
    with mss.mss() as sct:
        # Захват области экрана
        screenshot = sct.grab(monitor)

        # Преобразуем изображение в формат, который понимает OpenCV (numpy array)
        img = np.array(screenshot)

        # Преобразуем BGR изображение в RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Показываем захваченный скриншот
        cv2.imshow('Screen Capture', img)

        # Сохраняем изображение
        cv2.imwrite(f'screenshot_{i}.png', img)

# Функция для удаления фоток
def deleting_img():
    j = 0
    for j in range(3):
        try:
            file = pathlib.Path(f"screenshot_{j}.png")
            file.unlink()

        # Если не будет нужного изображения
        except FileNotFoundError:
            continue