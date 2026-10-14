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
    
    endpoint_data = {
        "endpointId": endpoint_id
    }
    if responseType == "StateReport" and token:
        endpoint_data["scope"] = {
            "type": "BearerToken",
            "token": token
        }

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
            "endpoint": endpoint_data,
            "payload": {}
        }
    }
    
    data = getDevice(device_id)
    print(data)
    if not data:
        data = (0, 0, 0, 0, 0, 0, 38, 42, 0, 0, 0)
    sh = 0
    
    sh1 = data[0]
    sh2 = data[1]
    sh3 = data[2]
    sh4 = data[3]
    sh5 = data[4]
    sh6 = data[5]
    ShTemp = data[6] if data[6] is not None else 38
    STTemp = data[7] if data[7] is not None else 42
    STTimer = data[8] if data[8] is not None else 0
    HueH = data[9] if data[9] is not None else 0
    br = data[10] if data[10] is not None else 0
    
    st = 0
    if STTimer > 0:
        st = 1
    
    if sh1 or sh2 or sh3 or sh4 or sh5 or sh6:
        sh = 1
    
    if component_id == "shower":
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": "ON" if sh == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ThermostatController",
                "name": "thermostatMode",
                "value": "HEAT" if sh == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ThermostatController",
                "name": "targetSetpoint",
                "value": {
                    "scale": "CELSIUS",
                    "value": float(ShTemp)
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.TemperatureSensor",
                "name": "temperature",
                "value": {
                    "scale": "CELSIUS",
                    "value": float(ShTemp)
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d1",
                "name": "toggleState",
                "value": "ON" if sh1 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d2",
                "name": "toggleState",
                "value": "ON" if sh2 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d3",
                "name": "toggleState",
                "value": "ON" if sh3 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d4",
                "name": "toggleState",
                "value": "ON" if sh4 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d5",
                "name": "toggleState",
                "value": "ON" if sh5 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ToggleController",
                "instance": "Shower.d6",
                "name": "toggleState",
                "value": "ON" if sh6 == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
    elif component_id == "colour":
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": "ON" if br > 0 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
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
        
    elif component_id == "steam":
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": "ON" if st == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ThermostatController",
                "name": "thermostatMode",
                "value": "HEAT" if st == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )
        
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.ThermostatController",
                "name": "targetSetpoint",
                "value": {
                    "scale": "CELSIUS",
                    "value": float(STTemp)
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.TemperatureSensor",
                "name": "temperature",
                "value": {
                    "scale": "CELSIUS",
                    "value": float(STTemp)
                },
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

    elif component_id in ['sh1', 'sh2', 'sh3', 'sh4', 'sh5', 'sh6']:
        try:
            flow_num = int(component_id[2:])
            flow_val = data[flow_num - 1] if data and len(data) >= flow_num else 0
        except (ValueError, IndexError):
            flow_val = 0
        discoverData["context"]["properties"].append(
            {
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": "ON" if flow_val == 1 else "OFF",
                "timeOfSample": str(current_time),
                "uncertaintyInMilliseconds": 200
            }
        )

    return discoverData
