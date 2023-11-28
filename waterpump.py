import serial
import time

usb_port = '/dev/ttyAMAO' #라즈베리파이의 우측 하단 연결된 포트 넘버
ser = serial.Serial(usb_port, 9600, timeout=1)

def turn_on_pump():
    ser.write(b'TURN_ON')
    print("펌프 작동")

def turn_off_pump():
    ser.write(b'TURN_OFF')
    print("펌프 끔")

def turn_on_pump_5second():
    turn_on_pump()
    time.sleep(5)
    turn_off_pump()
