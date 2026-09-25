import uuid
import json
import paho.mqtt.client as mqtt

broker_address = "api.carolieto.it"
port = 1883
username = "carolieto"
password = "c545b80bada39a160759d24d758135ec"


topic = "my/topic"
payload = "Hello, MQTT!"



def on_connect(client, userdata, flags, rc):
    try:
        print("Connecting.....")
        if rc == 0:
            print("Connected to MQTT broker")
            print(f"Topic:{topic}")
            print(f"payload:{payload}")
            client.publish(topic, payload)

            client.disconnect()
        else:
            print(f"Connection failed with code {rc}")
                
    except Exception as e:
        print(e)

def dataPublish(device_id, data):
    try:
        global topic
        global payload
        payload = json.dumps(data)
        
        print(f"device_id:{device_id}")
        topic = f"/SUB/{device_id}"
        #topic = "/SUB/MCA0001"
        
        client = mqtt.Client(f"iot-backend-{str(uuid.uuid4())}")
        client.username_pw_set(username, password)
        client.on_connect = on_connect
    
        client.connect(broker_address, port, keepalive=60)
        print("dataPublish B")
    
        client.loop_start()
        #client.loop_forever()
        #input("Press Enter to exit...")
        #client.disconnect()
    except Exception as e:
        print(e)
