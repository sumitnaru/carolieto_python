import uuid
from datetime import datetime, timezone
from userdata import getDevice

def alexaReport(correlation_token, token, endpoint_id, responseType):
    
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    parts = endpoint_id.split('-')
    device_id = parts[0]
    component_id = parts[1]
    
    print("Device ID:", device_id)
    print("Component ID:", component_id)
    
    discoverData = {
        "context": {
            "properties": [
                {
                    "namespace": "Alexa.EndpointHealth",
                    "name": "connectivity",
                    "value": {
                        "value": "OK"
                    },
                    "timeOfSample": str(current_time),
                    "uncertaintyInMilliseconds": 200
                }
            ]
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": responseType,
                "payloadVersion": "3",
                "messageId": str(uuid.uuid4()),
                "correlationToken": correlation_token
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": token
                },
                "endpointId": endpoint_id
            },
            "payload": {}
        }
    }
    
    data = getDevice(device_id)
    print(data)
    sh = 0
    
    sh1 = data[0]
    sh2 = data[1]
    sh3 = data[2]
    sh4 = data[3]
    sh5 = data[4]
    sh6 = data[5]
    ShTemp = data[6]
    STTemp = data[7]
    STTimer = data[8]
    HueH = data[9]
    br = data[10]
    
    st = 0;
    if STTimer > 0:
        st = 1
    
    
    if sh1 or sh2 or sh3 or sh4 or sh5 or sh6:
        sh = 1
    
    
    if component_id == "shower":# and responseType == 'StateReport':
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": "ON" if sh == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ThermostatController",
                "name": "targetSetpoint",
                "value": {
                    "scale": "CELSIUS",
                    "value": ShTemp
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        '''
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ColorController",
                "name": "color",
                "value": {
                    "hue": HueH,
                    "saturation": 1,
                    "brightness": 1
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.BrightnessController",
                "name": "brightness",
                "value": br,
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        '''
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d1",
                "name": "toggleState",
                "value": "ON" if sh1 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d2",
                "name": "toggleState",
                "value": "ON" if sh2 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d3",
                "name": "toggleState",
                "value": "ON" if sh3 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d4",
                "name": "toggleState",
                "value": "ON" if sh4 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d5",
                "name": "toggleState",
                "value": "ON" if sh5 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d6",
                "name": "toggleState",
                "value": "ON" if sh6 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200,
                "retrievable": True
            }
        )
        
    
    elif component_id == "colour":# and responseType == 'StateReport':
        
        discoverData["context"]["properties"].append(
            {
                    "namespace": "Alexa.PowerController",
                    "name": "powerState",
                    "value": "ON" if br > 0 else "OFF",
                    "timeOfSample": str(current_time),
                    "uncertaintyInMilliseconds": 200,
                    "retrievable": True
                }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ColorController",
                "name": "color",
                "value": {
                    "hue": HueH,
                    "saturation": 1,
                    "brightness": 1
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.BrightnessController",
                "name": "brightness",
                "value": br,
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
    
    
    elif component_id == "steam":# and responseType == 'StateReport':
        
        discoverData["context"]["properties"].append(
            {
                    "namespace": "Alexa.PowerController",
                    "name": "powerState",
                    "value": "ON" if st == 1 else "OFF",
                    "timeOfSample": str(current_time),
                    "uncertaintyInMilliseconds": 200,
                    "retrievable": True
                }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ThermostatController",
                "name": "targetSetpoint",
                "value": {
                    "scale": "CELSIUS",
                    "value": STTemp
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
    

    return discoverData
