import json
from userdata import getDeviceStatus, updateDeviceStatus
from mqttAction import dataPublish

def trigger(endpoint_id, status, instance, namespace):
    parts = endpoint_id.split('-')
    device_id = parts[0]
    component_type = parts[1]
    
    component_id = instance[-1]

    
    if component_type == 'shower' and ( namespace == 'Alexa.PowerController' or namespace == 'Alexa.ToggleController'):
        if status == 'TurnOn':
            showerOnOff(device_id, component_id, 1)
        else:
            showerOnOff(device_id, component_id, 0)
    
    elif component_type == 'steam' and namespace == 'Alexa.PowerController':
        if status == 'TurnOn':
            steamOnOff(device_id, 1)
        else:
            steamOnOff(device_id, 0)
    
    elif component_type == 'colour' and namespace == 'Alexa.PowerController':
        if status == 'TurnOn':
            setBrightness(device_id, 100)
        else:
            setBrightness(device_id, 0)
    
    elif component_type == 'colour' and namespace == 'Alexa.BrightnessController':
        setBrightness(device_id, status)
    
    elif component_type == 'colour' and namespace == 'Alexa.ColorController':
        setColour(device_id, status)
        
    elif component_type == 'shower' and namespace == 'Alexa.ThermostatController':
        
        #isOn = getDeviceStatus(device_id, "ON")
        #print(f"isOn:{isOn}")
        
        data = {
            "ShTemp": status
        }
        
        #if isOn != 1:
        #    data = {
        #        "shTemp": status,
        #        "sh1": 1
        #    }
            
        sendData(device_id, data)
    
    elif component_type == 'steam' and namespace == 'Alexa.ThermostatController':
        data = {
            "STTemp": status
            #"STTimer" : 1
        }
        sendData(device_id, data)
    


def showerOnOff(device_id, component_id, val):
    data = {}
    
    query = ""
    
    if component_id == '0' and val == 0:
        data = {
            "sh1" : val,
            "sh2" : val,
            "sh3" : val,
            "sh4" : val,
            "sh5" : val,
            "sh6" : val,
        }
        query = f"UPDATE tbl_device_status SET sh1=0, sh2=0, sh3=0, sh4=0, sh5=0, sh6=0 WHERE deviceid='{device_id}'"
    else:
        if component_id == '0':
            isOn = getDeviceStatus(device_id, "ON")
            if isOn == 1:
                return
            
            component_id = '1'
            
        data = {
            f"sh{component_id}" : val
        }
        query = f"UPDATE tbl_device_status SET sh{component_id}={val} WHERE deviceid='{device_id}'"
    
    sendData(device_id, data)
    
    updateDeviceStatus(query)
    
def steamOnOff(device_id, val):
    data = {
        "STTimer" : val
    }
    sendData(device_id, data)
    
    query = f"UPDATE tbl_device_status SET STTimer={val} WHERE deviceid='{device_id}'"
    updateDeviceStatus(query)
    


def setBrightness(device_id, status):
    
    data = {
        "br": status
    }
    
    sendData(device_id, data)
    
    query = f"UPDATE tbl_device_status SET br={status} WHERE deviceid='{device_id}'"
    updateDeviceStatus(query)
    
    
def setColour(device_id, status):
    br = getDeviceStatus(device_id, "BR")
        
    data = {
        "HueH": status
    }
        
    if br == 0:
        data = {
            "HueH": status,
            "br": 100
        }
        br = 100
    
    sendData(device_id, data)
    
    query = f"UPDATE tbl_device_status SET br={br}, HueH={status} WHERE deviceid={device_id}"  
    updateDeviceStatus(query)

    
    
def sendData(device_id, data):
    try:
        print("publish:"+json.dumps(data))
        if device_id:
            dataPublish(device_id, data)
    
    except Exception as e:
        print(e)
    
    