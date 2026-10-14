import uuid

def create_discovery_response(device_data):
    
    discovery_response = {
      "event": {
        "header": {
          "namespace": "Alexa.Discovery",
          "name": "Discover.Response",
          "payloadVersion": "3",
          "messageId": str(uuid.uuid4())
        },
        "payload": {
          "endpoints": []
        }
      }
    }
    
    print(device_data)
    print("_____________________________________")
    
    for data_item in device_data["data"]:
        device_id = data_item["deviceno"]
        dName = "Shower" #data_item["device"]
        noofshower = int(data_item["noofflow"])
        enable_steam = int(data_item["steamAvailable"])
        enable_light = int(data_item["rgb"])
        tempControl = int(data_item["tempController"])
        
        showerNames = [flow["name"] for flow in data_item["flows"]]
        
        print("deviceid:", device_id)
        print("device:", dName)
        print("noofshower:", noofshower)
        print("enable_steam:", enable_steam)
        print("enable_light:", enable_light)
        print("tempControl:", tempControl)
        print(showerNames)
        showerNames_length = len(showerNames)
        if showerNames_length < noofshower:
            noofshower = showerNames_length
            print("noofshower:", noofshower)
        
        if noofshower > 0:
            print("_____________________________________")
    
        
            discovery_response = create_device_data(discovery_response, noofshower, showerNames, device_id, enable_steam, enable_light, tempControl, dName)
    
    
    return discovery_response
    
  
    
def create_device_data(discovery_response, noofshower, showerNames, device_id, enable_steam, enable_light, tempControl, dName):
    display_categories = "OTHER"
    if tempControl:
        display_categories = "SWITCH"
    
    main_endpoint = {
                  "endpointId": f"{device_id}-shower",
                  "manufacturerName": "Carolieto",
                  "description": "Smart Shower Appliance By Carolieto",
                  "friendlyName": dName,
                  "displayCategories": [
                    display_categories
                  ],
                  "cookie": {},
                  "capabilities": [
                      {
                  "type": "AlexaInterface",
                  "interface": "Alexa.PowerController",
                  "version": "3",
                  "properties": {
                    "supported": [
                      {
                        "name": "powerState"
                      }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                  }
                },
                {
                  "type": "AlexaInterface",
                  "interface": "Alexa.EndpointHealth",
                  "version": "3",
                  "properties": {
                    "supported": [
                      {
                        "name": "connectivity"
                      }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True
                  }
                },
                {
                  "type": "AlexaInterface",
                  "interface": "Alexa",
                  "version": "3"
                }
              ]
            }
    
    
    for i in range(1, noofshower + 1):
        capability_inst_id = f"Shower.d{i}"
        capability_fName = showerNames[i-1] #f"Shower {str(i)}"
        names_to_add = [capability_fName]
        if "shower" not in capability_fName.lower():
            names_to_add.append(f"{capability_fName} Shower")
            names_to_add.append(f"Shower {capability_fName}")

        fnames_list = []
        for name_val in names_to_add:
            for loc in ["en-US", "en-IN", "hi-IN"]:
                fnames_list.append({
                    "@type": "text",
                    "value": {
                        "text": name_val,
                        "locale": loc
                    }
                })

        capability = {
                  "type": "AlexaInterface",
                  "interface": "Alexa.ToggleController",
                  "instance": capability_inst_id,
                  "version": "3",
                  "properties": {
                    "supported": [
                      {
                        "name": "toggleState"
                      }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True,
                    "nonControllable": False
                  },
                  "capabilityResources": {
                    "friendlyNames": fnames_list
                  }
                }
        
        main_endpoint["capabilities"].append(capability)
        
        
    if tempControl:
        th_capability = {
            "type": "AlexaInterface",
            "interface": "Alexa.ThermostatController",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "targetSetpoint"
                    },
                    {
                        "name": "thermostatMode"
                    }
                ],
                "proactivelyReported": False,
                "retrievable": True
            },
            "configuration": {
                "supportedModes": [
                    "OFF",
                    "HEAT"
                ]
            }
        }
        main_endpoint["capabilities"].append(th_capability)

        temp_sensor_capability = {
            "type": "AlexaInterface",
            "interface": "Alexa.TemperatureSensor",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "temperature"
                    }
                ],
                "proactivelyReported": False,
                "retrievable": True
            }
        }
        main_endpoint["capabilities"].append(temp_sensor_capability)
        
       
    discovery_response["event"]["payload"]["endpoints"].append(main_endpoint)
    
    for i in range(1, noofshower + 1):
        flow_name = showerNames[i-1]
        friendly_flow_name = f"{flow_name} Shower" if "shower" not in flow_name.lower() else flow_name
        flow_endpoint = {
            "endpointId": f"{device_id}-sh{i}",
            "manufacturerName": "Carolieto",
            "friendlyName": friendly_flow_name,
            "description": f"Carolieto Smart Shower {flow_name}",
            "displayCategories": [
                "SWITCH"
            ],
            "cookie": {},
            "capabilities": [
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa",
                    "version": "3"
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.PowerController",
                    "version": "3",
                    "properties": {
                        "supported": [
                            {
                                "name": "powerState"
                            }
                        ],
                        "proactivelyReported": False,
                        "retrievable": True
                    }
                },
                {
                    "type": "AlexaInterface",
                    "interface": "Alexa.EndpointHealth",
                    "version": "3",
                    "properties": {
                        "supported": [
                            {
                                "name": "connectivity"
                            }
                        ],
                        "proactivelyReported": True,
                        "retrievable": True
                    }
                }
            ]
        }
        discovery_response["event"]["payload"]["endpoints"].append(flow_endpoint)
    if enable_light:
        st_endpoint = {
          "endpointId": f"{device_id}-colour",
          "manufacturerName": "Carolieto",
          "friendlyName": "Colour",
          "description": "Smart Colour",
          "displayCategories": [
            "LIGHT"
          ],
          "capabilities": [
            {
              "type": "AlexaInterface",
              "interface": "Alexa",
              "version": "3"
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.PowerController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "powerState"
                  }
                ],
                "proactivelyReported": False,
                "retrievable": True
              }
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.ColorController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "color"
                  }
                ],
                "proactivelyReported": False,
                "retrievable": True
              }
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.BrightnessController",
                "version": "3",
                "properties": {
                    "supported": [
                        {
                            "name": "brightness"
                        }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                }
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.EndpointHealth",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "connectivity"
                  }
                ],
                "proactivelyReported": True,
                "retrievable": True
              }
            }
          ]
        }
        
        discovery_response["event"]["payload"]["endpoints"].append(st_endpoint)
    
    if enable_steam:
        st_endpoint = {
          "endpointId": f"{device_id}-steam",
          "manufacturerName": "Carolieto",
          "friendlyName": "Steam",
          "description": "Smart Steam",
          "displayCategories": [
            "SWITCH"
          ],
          "capabilities": [
            {
              "type": "AlexaInterface",
              "interface": "Alexa",
              "version": "3"
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.PowerController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "powerState"
                  }
                ],
                "proactivelyReported": False,
                "retrievable": True
              }
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.ThermostatController",
                "version": "3",
                "properties": {
                    "supported": [
                        {
                            "name": "targetSetpoint"
                        },
                        {
                            "name": "thermostatMode"
                        }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                },
                "configuration": {
                    "supportedModes": [
                        "OFF",
                        "HEAT"
                    ]
                }
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.TemperatureSensor",
                "version": "3",
                "properties": {
                    "supported": [
                        {
                            "name": "temperature"
                        }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                }
            },
            {
              "type": "AlexaInterface",
              "interface": "Alexa.EndpointHealth",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "connectivity"
                  }
                ],
                "proactivelyReported": True,
                "retrievable": True
              }
            }
          ]
        }
        
        discovery_response["event"]["payload"]["endpoints"].append(st_endpoint)
        
    return discovery_response
