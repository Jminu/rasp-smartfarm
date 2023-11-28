let client = null; // MQTT 클라이언트의 역할을 하는 Client 객체를 가리키는 전역변수
let connectionFlag = false; // 연결 상태이면 true
const CLIENT_ID = "client-"+Math.floor((1+Math.random())*0x10000000000).toString(16) // 사용자 ID 랜덤 생성

function connect() { // 브로커에 접속하는 함수
	if(connectionFlag == true)
		return; // 현재 연결 상태이므로 다시 연결하지 않음

	// 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
	let broker = document.getElementById("broker").value; // 브로커의 IP 주소
	let port = 9001 // mosquitto를 웹소켓으로 접속할 포트 번호

	// id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
	document.getElementById("messages").innerHTML += '<span>접속 : ' + broker + ' 포트 ' + port + '</span><br/>';
	document.getElementById("messages").innerHTML += '<span>사용자 ID : ' + 	CLIENT_ID + '</span><br/>';

	// MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
	client = new Paho.MQTT.Client(broker, Number(port), CLIENT_ID);

	// client 객체에 콜백 함수 등록 및 연결
	client.onConnectionLost = onConnectionLost; // 접속 끊김 시 onConnectLost() 실행 
	client.onMessageArrived = onMessageArrived; // 메시지 도착 시 onMessageArrived() 실행

	// client 객체에게 브로커에 접속 지시
	client.connect({
		onSuccess:onConnect, // 브로커로부터 접속 응답 시 onConnect() 실행
	});
}

// 브로커로의 접속이 성공할 때 호출되는 함수
function onConnect() {
    document.getElementById("messages").innerHTML += '<span>connected' + '</span><br/>';
    connectionFlag = true; // 연결 상태로 설정
}

//각각의 열에 각자 출력
function handleSensorValue(sensorType, value) {
	var columnId = sensorType + "-column";
	var columnDiv = document.getElementById(columnId);
	var valueDiv = document.createElement("div");
	valueDiv.innerHTML = "<b>" + sensorType + ":</b> " + value;
	columnDiv.appendChild(valueDiv);

	document.getElementById("messages").scrollTop = 0;
 }

 function subscribeAndHandle(sensorType) {
    subscribe(sensorType);

    // 새로운 센서 데이터를 처리하는 콜백 함수 등록
	/*
    client.subscribe(sensorType);
    client.onMessageArrived = function (message) {
        if (message.destinationName === sensorType) {
            handleSensorValue(sensorType, message.payloadString);
        }
    };
	*/
	// 이미 등록된 콜백 함수가 없으면 등록
    if (!client.onMessageArrived) {
        client.onMessageArrived = function (message) {
            var currentSensorType = message.destinationName;
            var currentValue = message.payloadString;
            
            // 각 센서 타입에 따라 다른 열에 출력
            if (currentSensorType === "luminant") {
                handleSensorValue("luminant", currentValue);
            } else if (currentSensorType === "temperature") {
                handleSensorValue("temperature", currentValue);
            } else if (currentSensorType === "humidity") {
                handleSensorValue("humidity", currentValue);
            } else {
                // 다른 센서 타입에 대한 처리 추가
            }
        };
    }
}

function subscribe(topic) {
	if(connectionFlag != true) { // 연결되지 않은 경우
		alert("연결되지 않았음");
		return false;
	}

	// 구독 신청하였음을 <div> 영역에 출력
	document.getElementById("messages").innerHTML += '<span>구독신청: 토픽 ' + topic + '</span><br/>';
	client.subscribe(topic); // 브로커에 구독 신청
}

function publish(topic, msg) {
	if(connectionFlag != true) { // 연결되지 않은 경우
		alert("연결되지 않았음");
		return false;
	}
	client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
	if(connectionFlag != true) return; // 연결되지 않은 경우
	
	// 구독 신청 취소를 <div> 영역에 출력
	document.getElementById("messages").innerHTML += '<span>구독신청취소: 토픽 ' + topic + '</span><br/>';
	client.unsubscribe(topic, null); // 브로커에 구독 신청 취소
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // responseObject는 응답 패킷
	document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
	if (responseObject.errorCode !== 0) {
		document.getElementById("messages").innerHTML += '<span>오류 : ' + responseObject.errorMessage + '</span><br/>';
	}
	connectionFlag = false; // 연결 되지 않은 상태로 설정
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
	console.log("onMessageArrived: " + msg.payloadString);
	// 도착한 메시지 출력
	var sensorType = msg.destinationName;
	var value = msg.payloadString;
 
	// 각 센서 타입에 따라 다른 열에 출력
	if (sensorType === "luminant") {
	   handleSensorValue("luminant", value);
	} else if (sensorType === "temperature") {
	   handleSensorValue("temperature", value);
	} else if (sensorType === "humidity") {
	   handleSensorValue("humidity", value);
	} else {
	   // 다른 센서 타입에 대한 처리 추가
	}

	document.getElementById("messages").scrollTop = 0; //맨 위에서부터 출력되도록
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function disconnect() {
	if(connectionFlag == false) 
		return; // 연결 되지 않은 상태이면 그냥 리턴
	client.disconnect(); // 브로커와 접속 해제
	document.getElementById("messages").innerHTML += '<span>연결종료</span><br/>';
	connectionFlag = false; // 연결 되지 않은 상태로 설정
}