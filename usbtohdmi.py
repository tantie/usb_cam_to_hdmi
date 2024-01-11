"""
for old rasp (32bit)
pip3 install opencv-python==3.4.6.27
pip3 install "numpy<1.20" or pip3 install numpy==1.19.5
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqt4-test libqt4-dev

sudo apt-get install unclutter убираем курсор

старт скрипта
DISPLAY=:0 python3 usbtohdmi.py

автозагрузка и постоянная работа
xset s off
xset -dpms

crontab -e
@reboot DISPLAY=:0 python3 /home/pi/usbtohdmi.py
@reboot unclutter -idle 0.1 or @reboot sleep 30; DISPLAY=:0 unclutter -idle 0.1

"""

import cv2
import numpy as np

cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

desired_size = (1280, 720)  # желаемый размер изображения

# Функция для показа сообщения на полноэкранном окне
def show_message(msg, delay):
    # Задаем параметры шрифта
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2 # размер шрифта
    line_type = 2

    for i in range(0, 255, 5):  # Плавное появление текста
        # Создаем черное изображение
        img = np.zeros([desired_size[1], desired_size[0], 3], dtype=np.uint8)

        # Наносим текст на изображение с изменением цвета
        cv2.putText(img, msg, (int(desired_size[0]/4), int(desired_size[1]/2)), 
                    font, font_scale, (i, i, i), line_type)
        
        cv2.imshow('Camera', img)
        if cv2.waitKey(delay) & 0xFF == ord('q'):  # Пауза для плавного появления текста
            return False

    for i in range(255, 0, -5):  # Плавное исчезновение текста
        # Создаем черное изображение
        img = np.zeros([desired_size[1], desired_size[0], 3], dtype=np.uint8)

        # Наносим текст на изображение с изменением цвета
        cv2.putText(img, msg, (int(desired_size[0]/4), int(desired_size[1]/2)), 
                    font, font_scale, (i, i, i), line_type)

        cv2.imshow('Camera', img)
        if cv2.waitKey(delay) & 0xFF == ord('q'):  # Пауза для плавного исчезновения текста
            return False
    return True

while True:
    cap = None
    for i in range(5):  # Попытка подключиться к камере
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', i)
            if not show_message('Trying to connect to cam ' + str(i), 5):
                cap = None
                continue
        else:
            print('Success: opened video source: ', i)
            break  # если удалось открыть камеру, прервать цикл

    if cap is None or not cap.isOpened():
        if not show_message('Failed to connect to camera.', 10):
            cap.release()
            cv2.destroyAllWindows()
            exit(0)
    else:
        # Чтение изображений с камеры и их отображение
        while True:
            ret, frame = cap.read()

            # Если изображение было успешно прочитано, изменить его размер и отобразить
            if ret:
                frame = cv2.resize(frame, desired_size)
                cv2.imshow('Camera', frame)
            else:
                break

            # Если нажата клавиша 'q', выйти из цикла
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit(0)

        # Если изображение не было прочитано, освободить камеру и попытаться снова подключиться
        cap.release()
