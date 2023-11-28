import time
import paho.mqtt.client as mqtt
import lumi #구현 완료
import temp_humid #구현 완료
import hitter #구현 완료
import plantled #구현 완료
import camera #구현 완료
import waterpump #모터 작동 안됨

def on_connect(client, userdata, flag, rc): #브로커에 연결시
	print("connected to broker")
def on_message(client, userdata, msg) : #브로커 연결되고 
	print("on_message connected to broker")

ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

hitter.init()
hitter.setInOut(5, "out") #히터LED는 red색이다

plantled.init()
plantled.setInOut(6, "out") #생장용LED는 green색이다


count = 0

# 병렬적으로 1초 단위로 초음파 센서로부터 거리를 읽어 전송하는 무한 루프 실행
while True:
	temp = temp_humid.getTemperature(temp_humid.sensor) #온도 읽기
	humid = temp_humid.getHumidity(temp_humid.sensor) #습도 읽기
	luminant = lumi.mcp.read_adc(0) #조도 읽기

	#10초마다 촬영
	
	if (count % 10) == 0:
		camera.init_camera()
		camera.shot_camera(count)
	else:
		pass

	#조도
	if(luminant < 10):
		#조도가 10 미만으로 나오면, 경고메세지 나오고 생장용 LED킨다
		plantled.led_on_off(6, 1)
		client.publish("luminant", "너무 어둡습니다. LED를 킵니다.", qos=0)
	else: #아니면 현재 조도 출력하고 생장용 LED 끈다
		plantled.led_on_off(6, 0)
		client.publish("luminant", "현재 조도 : "+str(luminant), qos=0)

	#습도
	if(humid < 10):
		#건조하면 경고메세지 나오고 물 펌프 작동
		client.publish("humidity", "수분이 부족합니다. 물 펌프 작동합니다", qos=0)
	else: #아니면 현재 습도 출력
		client.publish("humidity", "현재 습도 : "+str(humid), qos=0)

	#온도
	if temp < 20:
		#온도가 20도미만이면 LED히터 키고, 경고메세지 출력
		hitter.led_on_off(5, 1)
		client.publish("temperature", "온도가 너무 높습니다. 히터 작동.", qos=0)
	else: #아니면 현재 온도 출력하고, 히터 끈다
		hitter.led_on_off(5, 0)
		client.publish("temperature", "현재 온도 : "+str(temp), qos=0) #온도 퍼블리시

	count += 1
	time.sleep(1)


client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
