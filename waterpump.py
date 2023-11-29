# 워터펌프는 흰색 LED라고 가정한다
import time
import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def setInOut(pin, in_out):
    if in_out == "in":
        GPIO.setup(pin, GPIO.IN)
    if in_out == "out":
        GPIO.setup(pin, GPIO.OUT)

# pin에 연결된 워터펌프(white LED)에 0 or 1값을 출력하여 히터 끄고 킨다
def led_on_off(pin, value):
    GPIO.output(pin, value)

def watering(pump1, pump2, pump3):
    for i in range(3):
        led_on_off(pump1, 1)
        time.sleep(0.3)
        led_on_off(pump1, 0)
        time.sleep(0.3)
        led_on_off(pump2, 1)
        time.sleep(0.3)
        led_on_off(pump2, 0)
        time.sleep(0.3)
        led_on_off(pump3, 1)
        time.sleep(0.3)
        led_on_off(pump3, 0)
        time.sleep(0.3)

def watering_stop(pump1, pump2, pump3):
    led_on_off(pump1, 0)
    led_on_off(pump2, 0)
    led_on_off(pump3, 0)

if __name__ == "__main__":
    init()
    on_off = 1
    led_pin = int(input("GPIO PIN을 입력하세요 : "))
    setInOut(led_pin, "out")

    print("LED를 보세요.")

    # 5번 LED를 깜빡임
    for i in range(10):
        led_on_off(led_pin, on_off)
        time.sleep(1)
        print(i, end=' ', flush=True)
        on_off = 0 if on_off == 1 else 1 #0과 1의 토글링
        
    print()
    GPIO.clenup()