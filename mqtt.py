import time
import paho.mqtt.client as mqtt
import lumi
import temp_humid

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

# 병렬적으로 1초 단위로 초음파 센서로부터 거리를 읽어 전송하는 무한 루프 실행
while True:
	temp = temp_humid.getTemperature(temp_humid.sensor) #온도 읽기
	humid = temp_humid.getHumidity(temp_humid.sensor) #습도 읽기
	luminant = lumi.mcp.read_adc(0) #조도 읽기

	client.publish("luminant", luminant, qos=0) #조도 퍼블리시
	client.publish("temperature", temp, qos=0) #온도 퍼블리시
	client.publish("humidity", humid, qos=0) #습도 퍼블리시

	time.sleep(1)


client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
