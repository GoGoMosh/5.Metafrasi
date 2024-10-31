"""
Ядро программы Metafrasi
"""

from function import *
import time
import string
import logging
from threading import Thread

# Флаг для запуска/паузы захвата экрана
global is_running, stop_program
is_running = True
is_exit = True

# функция для обработки нажатий клавиш
def check_keys():

    global is_running, is_exit

    # Читаем клавиатуру с небольшой задержкой (100 мс) для правильной обработки к
    key = cv2.waitKey(100) & 0xFF

    # Если нажата клавиша 'p', ставим захват на паузу, иначе снимаем паузу
    if key in [80, 112]:
        is_running = not is_running
        print("Захват экрана поставлен на паузу" \
                    if not is_running else "Захват экрана паузы снят")
        return is_running

    # Выход из программы при нажатии ESC
    elif key == 27:  # 27 - это код клавиши ESC
        print("Завершение программы")
        is_exit = not is_exit
        return is_exit
    elif key == 75:
        print("Test parallel")

def main():

    global is_running, is_exit

    # Чтобы не выводилась постоянно сообщение о CUDA от Easyocr
    logging.getLogger('easyocr').setLevel(logging.ERROR)

    # Определяем размеры и положение области экрана для скриншота
    monitor = {
        "top": 100,  # Верхняя граница (координата Y)
        "left": 100,  # Левая граница (координата X)
        "width": 800,  # Ширина области
        "height": 120  # Высота области
    }


    i = 0

    # Основной цикл программы
    try:
        while True:
            # Изменение имени файла сохраняемого изображения с текстом от 0 до 2
            i = (i + 1) % 3
            check_keys()
            # Захват экрана каждые 3 секунды, если захват запущен
            if not is_exit:
                break
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



    # Закрытие программы
    finally:

        # Удаление окон openCV
        cv2.destroyAllWindows()

        # Удаление изображения
        deleting_img()



if __name__ == "__main__":
    t1 = Thread(target=check_keys)
    t2 = Thread(target=main, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()