import hashlib
import uuid
import requests
import secrets
import json
import pytz
from datetime import time
from time import time
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, redirect, session, render_template, jsonify
from bcrypt import checkpw
from authlib.integrations.flask_client import OAuth
from bcrypt import hashpw, gensalt
from authlib.integrations.flask_client import OAuth, OAuthError
from flask import request
from pprint import pprint
from bcrypt import checkpw
from datetime import datetime, timedelta, timezone
#from alexa_response import AlexaResponse  # Import the AlexaResponse class
#from alexa_utils import generate_access_token
#from validation import validate_message

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
app.secret_key = '131313dasdad'

# A dictionary to store authorization codes temporarily
authorization_codes = {}


base_url = "https://api.carolieto.it"  # API's base URL
#hostingURL = "backclouds.xyz" # Hosted URL

OAUTH_CLIENT_ID = 'abcdef'
OAUTH_CLIENT_SECRET = '987654321'
OAUTH_SCOPE = 'profile postal_code'


#my_redirect_uri = "https://layla.amazon.com/api/skill/link/MPUHHIP30KBZU"
#scope = profile



from userdata import signin_to_api, get_user_by_email, get_devices, update_user_by_email, get_user_by_refreshToken, get_userid_by_token, get_user_by_token, putEmailCheckForAuth, matchforAuth, getDevice
from alexaResponseClass import alexaReport
from alexaDiscovery import create_discovery_response
from triggerDevice import trigger


def generate_access_token(authorization_code):
    print("I'm generating access token")
    print(authorization_codes)
    print("----")
    
    if not authorization_codes:
        print("Fresh Array")
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32) 

        expires_in = int(time()) + 3600

        return access_token, refresh_token, expires_in
        
    
    try:
        print("try A1: ")
        for key, value in authorization_codes.copy().items():
            print("Check: ", key)
            if value == authorization_code:
                print("Auth Array updated")
                access_token = secrets.token_urlsafe(32)
                refresh_token = secrets.token_urlsafe(32) 
    
                expires_in = int(time()) + 3600
    
                return access_token, refresh_token, expires_in
        
        
        print("Re-Fresh Array")
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32) 

        expires_in = int(time()) + 3600

        return access_token, refresh_token, expires_in
        
        
    except KeyError as e:
        return None, None, None
    

@app.route('/')
def home():
    if 'access_token' in session:
        return 'Welcome to Your App. You are linked!'
    
    #get_devices(base_url, 25)
    #usr = get_userid_by_token('SXVaz8kKe9alHGYSwqI-Bl_anmzb9j6jkZC-lngsVe4')
    
    #device_data = get_devices(base_url, 25)
    #print(create_discovery_response(device_data))
    return 'Welcome to Your App. Please link your account...'

        
@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'POST':
            print("im in post")
            # Retrieve user credentials and authenticate the user
            email = request.form.get('email')
            password = request.form.get('password')
            
            state_param = request.form.get('state')
            client_id = request.form.get('client_id')
            response_type = request.form.get('response_type')
            scope = request.form.get('scope')
            redirect_uri = request.form.get('redirect_uri')
    
            print("email: ", email)
            print("password: ", password)
            
            print("state_param: ", state_param)
            print("client_id: ", client_id)
            print("response_type: ", response_type)
            print("scope: ", scope)
            print("redirect_uri: ", redirect_uri)
            #redirect_uri = my_redirect_uri
            
            try:
                print("B4 Checking authorization_codes--------")
                for key, value in authorization_codes.copy().items():
                    if key == email:
                        authorization_codes.pop(email)
                        print("authorization_codes removed--------")
            except KeyError as e:
                print(f"login exception:",str(e))
                    
    
            response = signin_to_api(base_url, email, password)
            print(f"login response:",response)
            status = response.get('status')
            if status == 'success':
                user_data = response.get('user')
                session['user'] = user_data
                email = user_data["data"]["email_id"]
                #session['user'] = email
                
                
                authorization_code = authorization_codes.get(email)
                
                print(f"authorization_code res:",authorization_code)
    
                if not authorization_code:
                    print(f"authorised Success:")
                    authorization_code = secrets.token_urlsafe(32)
                    authorization_codes[email] = authorization_code
                    
                    update_user_by_email(email, authorization_code, "", "0")
    
                    redirect_url = f'/authorize?state={state_param}&client_id={client_id}&response_type={response_type}&scope={scope}&redirect_uri={redirect_uri}&code={authorization_code}'
    
                    return redirect(redirect_url)
    
                else:
                    print(f"authorised Failed:")
                    uri = f'login.html?state_param={state_param}&client_id={client_id}&response_type={response_type}&scope={scope}&redirect_uri={redirect_uri}'
                    return render_template(uri, error='Invalid credentials, Close the app and try again')      
                
            else:
                session.clear()
                
                #uri = f'login.html?state_param={state_param}&client_id={client_id}&response_type={response_type}&scope={scope}&redirect_uri={redirect_uri}'
                return render_template('login.html', error=response.get('message'))
                
            return response
            
        else:
            return render_template('login.html', error=None)
    except TemplateNotFound:
        app.logger.error('TemplateNotFound error for login.html')
        return jsonify({"error": "Template not found"}), 500


@app.route('/authorize')
def authorize():
    # Extract parameters from the query string
    state_param = request.args.get('state')
    client_id = request.args.get('client_id')
    response_type = request.args.get('response_type')
    scope = request.args.get('scope')
    redirect_uri = request.args.get('redirect_uri')
    print("state_param", state_param)
    print("response_type", response_type)
    print("scope", scope)
    print("redirect_uri", redirect_uri)
    print("client_id", client_id)
    #redirect_uri = my_redirect_uri

    # Check if the user is already logged in
    if 'user' in session:
        user_data = session['user']
        email = session['user']["data"]["email_id"]
        user = get_user_by_email(email)
        authorization_code = authorization_codes.get(email)
        print("authorization_code: ", authorization_code)
        

        if user and authorization_code:
            # Construct the URL with parameters in the URL fragment
            redirect_url = f'{redirect_uri}?state={state_param}&code={authorization_code}&scope={OAUTH_SCOPE}'
            print("Redirect user in Autorize", redirect_url)
            return redirect(redirect_url)

    # User is not logged in or does not have an authorization code, redirect to the login page with the received GET variables
    login_url = f'/login?state={state_param}&client_id={client_id}&response_type={response_type}&scope={scope}&redirect_uri={redirect_uri}'

    # Redirect to the login URL with GET parameters
    return redirect(login_url)


@app.route('/token_exchange', methods=['POST'])
def token_exchange():
    print("In token_exchange")
    # Retrieve the parameters from the POST request
    
    grant_type = request.form.get('grant_type')
    authorization_code = request.form.get('code')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    redirect_uri = request.form.get('redirect_uri')


    print("grant_type", grant_type)
    print("authorization_code", authorization_code)
    print("client_id", client_id)
    print("client_secret", client_secret)
    print("redirect_uri", redirect_uri)
    #redirect_uri = my_redirect_uri
    

    if grant_type == "authorization_code":
        # Generate or retrieve the access token and its expiration time
        access_token, refresh_token, access_expires_in = generate_access_token(authorization_code)
        print("access_token", access_token)
        print("access_expires_in", access_expires_in)
        print("refresh_token", refresh_token)

        if access_token:
            session['access_token'] = access_token

            user_data = session.get('user', None)
            print("user session in token exchange")
            print(user_data)
            if authorization_code:
                print("in authorization_code")
                email = None
                print("authorization_codes arr count:", len(authorization_codes))
                for stored_email, stored_code in authorization_codes.items():
                    if stored_code == authorization_code:
                        email = stored_email
                        print("email Found in data", email)
                        break
                
                if not email:
                    print("Check DB for Email")
                    email = get_user_by_token(authorization_code)
                    print("Email Found:",email)
                
                if not email:
                    print("Check DB Auth for Email")
                    email = matchforAuth()
                    print("Email Found:",email)

                if email:
                    print("Updating DB")
                    access_expires = datetime.now() + timedelta(seconds=access_expires_in)
                    res = update_user_by_email(email, access_token, refresh_token, access_expires)
                    print("User update: ", res)
                    
                    response = {
                        'access_token': access_token,
                        'token_type': 'bearer',  # Include the token type here
                        'expires_in': access_expires_in,
                        'refresh_token': refresh_token,  # Include the refresh token if needed
                    }
                    print("we sending response in authorization_code", response)
                    return jsonify(response)
                
                
        return ""
                

    elif grant_type == "refresh_token":
        # Retrieve the refresh_token from the request
        refresh_token = request.form.get('refresh_token')

        if refresh_token:
            # Match the refresh_token with a user in the collection
            _email = get_user_by_refreshToken(refresh_token)

            if _email:
                # Generate a new access token and expiration time
                access_token, refresh_token_notUse, access_expires_in = generate_access_token(refresh_token)

                if access_token:
                    session['access_token'] = access_token

                    access_expires = datetime.now() + timedelta(seconds=access_expires_in)
                    res = update_user_by_email(_email, access_token, refresh_token, access_expires)
                    print("User update: ", res)

                    response = {
                        'access_token': access_token,
                        'token_type': 'bearer',
                        'expires_in': access_expires_in,
                    }
                    print("we sending response in refresh_token", response)

                    return jsonify(response)

            return jsonify({'error': 'Invalid refresh_token'}), 400

        return jsonify({'error': 'Refresh token is missing'}), 400

    return jsonify({'error': 'Invalid grant_type'}), 400


def generate_change_report(endpoint_id, device_state, correlation_token, bearer_token, component_type):
    # Define the current timestamp in ISO 8601 format
    timestamp = datetime.utcnow().isoformat()

    # Extract the device state for the specified component from the JSON
    # component_state = device_state.get(component_type, {})

    # Prepare the ChangeReport event
    if component_type == 'Light' or component_type == 'LIGHT':
        # Extract the power state from the component state
        for key, value in device_state.items():
            if 'ONOFF' in value:
                onoff_value = value['ONOFF']
                break

        # Print the extracted value
        print("ONOFF Value:", onoff_value)
        power_state = onoff_value  # component_state.get('ONOFF', 'OFF')

        change_report = {
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "StateReport",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": correlation_token,
                    "payloadVersion": "3"
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": bearer_token
                    },
                    "endpointId": endpoint_id
                },
                "payload": {}
            },
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.PowerController",
                        "name": "powerState",
                        "value": power_state,
                        "timeOfSample": timestamp,
                        "uncertaintyInMilliseconds": 6000,
                        "retrievable": True  # Set to retrievable
                    },
                    {
                        "namespace": "Alexa.EndpointHealth",
                        "name": "connectivity",
                        "value": {
                            "value": "OK"
                        },
                        "timeOfSample": timestamp,
                        "uncertaintyInMilliseconds": 6000,
                        "retrievable": True  # Set to retrievable
                    }
                ]
            }
        }

    return change_report


def generate_power_controller_response(correlation_token, endpoint_id, power_state_value):
    # Define the current timestamp in ISO 8601 format
    timestamp = datetime.utcnow().isoformat()

    # Prepare the Response event
    response = {
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "Response",
                "messageId": str(uuid.uuid4()),
                "correlationToken": correlation_token,
                "payloadVersion": "3"
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": "OAuth2.0 bearer token"
                },
                "endpointId": endpoint_id
            },
            "payload": {}
        },
        "context": {
            "properties": [
                {
                    "namespace": "Alexa.PowerController",
                    "name": "powerState",
                    "value": power_state_value,
                    "timeOfSample": timestamp,
                    "uncertaintyInMilliseconds": 500
                }
            ]
        }
    }

    return response


@app.route('/api/alexa/smart_home', methods=['POST'])
def alexa_smart_home():
    try:
        # Get the request JSON data sent by Alexa
        alexa_request = request.json
        print("Received Alexa Request:")
        
        if "directive" in alexa_request:
            directive = alexa_request["directive"]
            print("Directive:", json.dumps(directive))
            
            if "payload" in directive and "scope" in directive["payload"]:
                token = directive["payload"]["scope"]["token"]
                print("get Token", token)
                user_id = get_userid_by_token(token)
                print("user_id", user_id)
                if user_id:
                    if "directive" in alexa_request and "header" in alexa_request["directive"] and "namespace" in directive["header"] and "name" in directive["header"]:
                        
                        namespace = alexa_request["directive"]["header"]["namespace"]
                        name = alexa_request["directive"]["header"]["name"]
    
                        if namespace == 'Alexa.Authorization':
                            if name == 'AcceptGrant':
                                # Note: This sample accepts any grant request
                                # In your implementation, you would use the code and token to get and store access tokens
                                grant_code = alexa_request['directive']['payload']['grant']['code']
                                grantee_token = alexa_request['directive']['payload']['grantee']['token']
    
                                # Prepare AcceptGrant.Response
                                response = {
                                    "event": {
                                        "header": {
                                            "namespace": "Alexa.Authorization",
                                            "name": "AcceptGrant.Response",
                                            "messageId": str(uuid.uuid4()),
                                            "payloadVersion": "3"
                                        },
                                        "payload": {}
                                    }
                                }
                                print("AcceptGrant.Response:")
                                print(response)
                                return jsonify(response)
    
                        elif namespace == 'Alexa.Discovery':
                            device_data = get_devices(base_url, user_id)
                            print('Alexa.Discovery namespace')
                            alexa_response = create_discovery_response(device_data)
    
                            print(alexa_response)
                            print('Alexa.Discovery submit')
                            return jsonify(alexa_response)
    
                        elif namespace == 'Alexa.PowerController':
                            # Get the endpoint ID, requested state, and correlation token
                            endpoint_id = directive['endpoint']['endpointId']
                            name = directive['header']['name']
                            print("Get Request for ", name)
                            power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
                            correlation_token = directive['header']['correlationToken']
                            # Check for an error when setting the state
                            response = generate_power_controller_response(correlation_token, endpoint_id, power_state_value)
                            print("response", response)
                            #print("Validate:", validate_message(alexa_request, response))
                            return jsonify(response)
            
            elif "header" in directive and "namespace" in directive["header"] and "name" in directive["header"]:
                    
                namespace = directive["header"]["namespace"]
                name = directive["header"]["name"]
                
                if namespace == 'Alexa' and name == 'ReportState':
                    try:
                        print("I'm in Report State")
                        endpoint_id = directive['endpoint']['endpointId']
                        print("endpoint_id", endpoint_id)
                        correlation_token = directive['header']['correlationToken']
                        print("correlation_token", correlation_token)
                        token = directive['endpoint']['scope']['token']
                        print("token", token)
                        
                        
                        change_report = alexaReport(correlation_token, token, endpoint_id, "StateReport")
                        
                        
                        print("ChangeReport:")
                        print(change_report)
                        #print("Validate:", validate_message(alexa_request, change_report))
    
                        return jsonify(change_report)
                    except (KeyError, Exception) as e:
                        # Handle missing or incorrect keys in the request
                        error_response = {
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "ErrorResponse",
                                    "messageId": str(uuid.uuid4()),
                                    "payloadVersion": "3"
                                },
                                "payload": {
                                    "type": "INVALID_DIRECTIVE",
                                    "message": f"Missing or incorrect key in the request: {str(e)}"
                                }
                            }
                        }
                        print("Error Response:")
                        print(error_response)
                        return jsonify(error_response)
                
                elif namespace == 'Alexa.PowerController':
                    try:
                        print("I'm in Trigger Power")
                        endpoint_id = directive['endpoint']['endpointId']
                        print("endpoint_id: ", endpoint_id)
                        correlation_token = directive['header']['correlationToken']
                        print("correlation_token: ", correlation_token)
                        token = directive['endpoint']['scope']['token']
                        print("token: ", token)
                        
                        status = directive['header']['name']
                        print("status: ", status)
                        
                        trigger(endpoint_id, status, "Shower.d0", namespace)
                        #time.sleep(1)
                        response_report = alexaReport(correlation_token, token, endpoint_id, "Response")
                        
                        
                        print("Response:")
                        print(response_report)
                        #print("Validate:", validate_message(alexa_request, change_report))
    
                        return jsonify(response_report)
                    
                    except (KeyError, Exception) as e:
                        # Handle missing or incorrect keys in the request
                        error_response = {
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "ErrorResponse",
                                    "messageId": str(uuid.uuid4()),
                                    "payloadVersion": "3"
                                },
                                "payload": {
                                    "type": "INVALID_DIRECTIVE",
                                    "message": f"Missing or incorrect key in the request: {str(e)}"
                                }
                            }
                        }
                        print("Error Response:")
                        print(error_response)
                        return jsonify(error_response)
                
                elif namespace == 'Alexa.ToggleController':
                    try:
                        print("I'm in Trigger Toggle")
                        endpoint_id = directive['endpoint']['endpointId']
                        print("endpoint_id: ", endpoint_id)
                        correlation_token = directive['header']['correlationToken']
                        print("correlation_token: ", correlation_token)
                        token = directive['endpoint']['scope']['token']
                        print("token: ", token)
                        
                        status = directive['header']['name']
                        print("status: ", status)
                        
                        instance = directive['header']['instance']
                        print("instance: ", instance)
                        
                        trigger(endpoint_id, status, instance, namespace)
                        
                        response_report = alexaReport(correlation_token, token, endpoint_id, "Response")
                        
                        
                        print("Response:")
                        print(response_report)
                        #print("Validate:", validate_message(alexa_request, change_report))
    
                        return jsonify(response_report)
                    
                    except (KeyError, Exception) as e:
                        # Handle missing or incorrect keys in the request
                        error_response = {
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "ErrorResponse",
                                    "messageId": str(uuid.uuid4()),
                                    "payloadVersion": "3"
                                },
                                "payload": {
                                    "type": "INVALID_DIRECTIVE",
                                    "message": f"Missing or incorrect key in the request: {str(e)}"
                                }
                            }
                        }
                        print("Error Response:")
                        print(error_response)
                        return jsonify(error_response)
                        
                elif namespace == 'Alexa.BrightnessController':
                    try:
                        print("I'm in Trigger Brightness")
                        endpoint_id = directive['endpoint']['endpointId']
                        print("endpoint_id: ", endpoint_id)
                        correlation_token = directive['header']['correlationToken']
                        print("correlation_token: ", correlation_token)
                        token = directive['endpoint']['scope']['token']
                        print("token: ", token)
                        
                        payload = directive.get('payload', {})
                        if 'brightness' in payload:
                            status = payload['brightness']
                        elif 'brightnessDelta' in payload:
                            delta = payload['brightnessDelta']
                            parts = endpoint_id.split('-')
                            dev_id = parts[0]
                            dev_data = getDevice(dev_id)
                            current_br = dev_data[10] if dev_data and len(dev_data) > 10 else 100
                            status = max(0, min(100, (current_br or 0) + delta))
                        else:
                            status = 100
                        print("status: ", status)
                        
                        trigger(endpoint_id, status, "light-d1", namespace)
                        
                        response_report = alexaReport(correlation_token, token, endpoint_id, "Response")
                        
                        print("Response:")
                        print(response_report)
    
                        return jsonify(response_report)
                    
                    except (KeyError, Exception) as e:
                        # Handle missing or incorrect keys in the request
                        error_response = {
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "ErrorResponse",
                                    "messageId": str(uuid.uuid4()),
                                    "payloadVersion": "3"
                                },
                                "payload": {
                                    "type": "INVALID_DIRECTIVE",
                                    "message": f"Missing or incorrect key in the request: {str(e)}"
                                }
                            }
                        }
                        print("Error Response:")
                        print(error_response)
                        return jsonify(error_response)
                        
                elif namespace == 'Alexa.ColorController':
                    try:
                        print("I'm in Color Controller")
                        endpoint_id = directive['endpoint']['endpointId']
                        print("endpoint_id", endpoint_id)
                        correlation_token = directive['header']['correlationToken']
                        print("correlation_token", correlation_token)
                        token = directive['endpoint']['scope']['token']
                        print("token", token)
        
                        color_data = directive['payload']['color']
                        #brightness = color_data['brightness']
                        hue = color_data['hue']
                        #saturation = color_data['saturation']
                        status = hue
                        print("status: ", status)
                        
                        
                        trigger(endpoint_id, status, "light-d1", namespace)
        
                        response_report = alexaReport(correlation_token, token, endpoint_id, "Response")
        
                        print("Response:")
                        print(response_report)
        
                        return jsonify(response_report)
                    except KeyError as e:
                        # Handle missing or incorrect keys in the request
                        error_response = {
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "ErrorResponse",
                                    "messageId": str(uuid.uuid4()),
                                    "payloadVersion": "3"
                                },
                                "payload": {
                                    "type": "INVALID_DIRECTIVE",
                                    "message": f"Missing or incorrect key in the request: {str(e)}"
                                }
                            }
                        }
                        print("Error Response:")
                        print(error_response)
                        return jsonify(error_response)
                
                elif namespace == 'Alexa.ThermostatController':
                    try:
                        print("I'm in Thermostat Controller")
                        endpoint_id = directive['endpoint']['endpointId']
                        print("endpoint_id", endpoint_id)
                        correlation_token = directive['header']['correlationToken']
                        print("correlation_token", correlation_token)
                        token = directive['endpoint']['scope']['token']
                        print("token", token)
        
                        directive_name = directive['header']['name']
                        payload = directive.get('payload', {})
                        print("directive_name: ", directive_name)
                        print("payload: ", payload)

                        parts = endpoint_id.split('-')
                        device_id = parts[0]
                        component_type = parts[1]

                        if directive_name == 'SetThermostatMode':
                            mode_val = payload.get('mode', {}).get('value', 'OFF')
                            power_status = 'TurnOff' if mode_val == 'OFF' else 'TurnOn'
                            trigger(endpoint_id, power_status, "Shower.d0", "Alexa.PowerController")
                            response_report = alexaReport(correlation_token, token, endpoint_id, "Response")
                            return jsonify(response_report)
                        elif directive_name == 'SetTargetTemperature':
                            target_obj = payload.get('targetSetpoint', {})
                            temp_val = float(target_obj.get('value', 38))
                            scale = target_obj.get('scale', 'CELSIUS')
                            if str(scale).upper() == 'FAHRENHEIT':
                                status = round((temp_val - 32) * 5 / 9)
                            else:
                                status = round(temp_val)
                            trigger(endpoint_id, status, "showerSteam-d1", namespace)
                        elif directive_name == 'AdjustTargetTemperature':
                            delta_obj = payload.get('targetSetpointDelta', {})
                            delta_val = float(delta_obj.get('value', 0))
                            scale = delta_obj.get('scale', 'CELSIUS')
                            if str(scale).upper() == 'FAHRENHEIT':
                                delta = delta_val * 5 / 9
                            else:
                                delta = delta_val
                            dev_data = getDevice(device_id)
                            current_temp = (dev_data[6] if component_type == 'shower' else dev_data[7]) if dev_data else 38
                            status = round((current_temp or 38) + delta)
                            trigger(endpoint_id, status, "showerSteam-d1", namespace)
                        else:
                            status = 38
                            trigger(endpoint_id, status, "showerSteam-d1", namespace)

                        response_report = alexaReport(correlation_token, token, endpoint_id, "Response")
        
                        print("Response:")
                        print(response_report)
        
                        return jsonify(response_report)
                    except (KeyError, Exception) as e:
                        # Handle missing or incorrect keys in the request
                        error_response = {
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "ErrorResponse",
                                    "messageId": str(uuid.uuid4()),
                                    "payloadVersion": "3"
                                },
                                "payload": {
                                    "type": "INVALID_DIRECTIVE",
                                    "message": f"Missing or incorrect key in the request: {str(e)}"
                                }
                            }
                        }
                        print("Error Response:")
                        print(error_response)
                        return jsonify(error_response)
            
            else:
                    # Return an appropriate error response
                    response = {
                        "event": {
                            "header": {
                                "namespace": "Alexa",
                                "name": "ErrorResponse",
                                "messageId": str(uuid.uuid4()),
                                "payloadVersion": "3"
                            },
                            "payload": {
                                "type": "INTERNAL_ERROR",
                                "message": "Unsupported Alexa namespace directive received"
                            }
                        }
                    }
                    print("ErrorResponse:")
                    print(response)
                    return jsonify(response)
    
    except Exception as e:
        # Handle any exceptions or errors
        error_response = {
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "ErrorResponse",
                    "messageId": str(uuid.uuid4()),
                    "payloadVersion": "3"
                },
                "payload": {
                    "type": "INTERNAL_ERROR",
                    "message": str(e)
                }
            }
        }
        print("Error Response:")
        print(error_response)
        return jsonify(error_response)


@app.route('/link', methods=['GET'])
def link():
    _email = request.args.get('email')
    
    if len(_email) > 8:
        _uid = request.args.get('uid')
        print("email: ", _email)
        print("uid: ", _uid)
        putEmailCheckForAuth(_email, _uid)
    
        #print(matchforAuth())
    return "success"
    

#@app.route('/unlink', methods=['GET'])
#def unlink():
#    print(request)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)