import cv2
import time

camera = None

def init_camera():
    global camera
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)

def shot_camera(count):
    image_folder = '/home/pi/smartplanter/rasp-smartfarm/image'
    image_name = f'image_{count}.jpg'
    image_path = image_folder + image_name

    ret, image = camera.read()
    if(ret == True):
        cv2.imwrite(image_folder, image) # OpenCV 함수로 이미지를 파일에 저장
    else:
        print("camera error!")

if __name__ == "__main__":
    init_camera()
