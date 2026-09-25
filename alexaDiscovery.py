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
                  "instance": "Shower.power",
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
                    "friendlyNames": [
                      {
                        "@type": "text",
                        "value": {
                          "text": capability_fName,
                          "locale": "en-US"
                        }
                      },
                      {
                        "@type": "text",
                        "value": {
                          "text": capability_fName,
                          "locale": "en-IN"
                        }
                      },
                      {
                        "@type": "text",
                        "value": {
                          "text": capability_fName,
                          "locale": "hi-IN"
                        }
                      }
                    ]
                  }
                }
        
        main_endpoint["capabilities"].append(capability)
        
        
    if tempControl:
        th_capability = {
            "type": "AlexaInterface",
            "interface": "Alexa.ThermostatController",
            "instance": "Shower.temp",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "targetSetpoint"
                    }
                ],
                "proactivelyReported": False,
                "retrievable": True
            }
        }
        main_endpoint["capabilities"].append(th_capability)
        
       
    discovery_response["event"]["payload"]["endpoints"].append(main_endpoint)
    
    
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
              "instance": "Colour.power",
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
              "instance": "Colour.color",
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
                "instance": "Colour.bright",
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
              "instance": "Steam.power",
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
                "instance": "Steam.temp",
                "version": "3",
                "properties": {
                    "supported": [
                        {
                            "name": "targetSetpoint"
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
