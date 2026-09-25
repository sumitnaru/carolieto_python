import requests
import mysql.connector
from datetime import datetime, timedelta, timezone


host = 'localhost'
user = 'carolieto'
password = 'XpP68GY5MHCDZpAM'
database = 'carolieto'

apiKey = 'YNOVqgrBE7xvyZwALYhoNhVCBZKiDPIJ'

def signin_to_api(base_url, email, password):
    # Define the endpoint URL
    api_endpoint = f"{base_url}/api/signin"

    headers = {
      'Api_key': apiKey,
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'ci_session=4iumlk7nunsqhkbh22ub5spip51r7lr5'
    }

    data = {
        'email_id': email,
        'password': password
    }

    try:
        # Make the POST request
        response = requests.post(api_endpoint, data=data, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            status = response_data["status"]
            if status == 'error':
                print("Login Error")
                return {
                    "message": "Invalid credencials. Close the app and try again",
                    "status": "error"
                }
            else:
                email = response_data["data"]["email_id"]
                user_id = response_data["data"]["id"]
                api_response = {
                    "user": response_data,
                    "message": "",
                    "status": "success"
                }
                createUser(response_data)
                return api_response
        else:
            return {
                "message": f"Request failed with status code {response.status_code}",
                "status": "error"
            }
    except requests.exceptions.RequestException as e:
        return {
            "message": f"Request failed with exception: {str(e)}",
            "status": "error"
        }
        

def get_devices(base_url, user_id):
    api_endpoint = f"{base_url}/api/device/get_devices"

    headers = {
        'Api_key': apiKey,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ci_session=4iumlk7nunsqhkbh22ub5spip51r7lr5'
    }

    data = {
        'UserID': user_id
    }

    try:
        response = requests.post(api_endpoint, data=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            return response_data 
            
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed with exception: {str(e)}")
        return None



            
def createUser(data):

    user_id = data["data"]["id"]
    name = data["data"]["first_name"] + " " + data["data"]["last_name"]
    email = data["data"]["email_id"]
    activated = 1
    
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    # Create a cursor
    cursor = connection.cursor()
    
    select_query = "SELECT user_id FROM _iot_user WHERE user_id = %s"
    cursor.execute(select_query, (user_id,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        # User with the same user_id already exists
        print("User with the same user_id already exists")
        '''update_query = """
        UPDATE `_iot_user` SET `access_token`=null,`expires_in`=null,`refresh_token`=null WHERE `email` = %s
        """
        cursor.execute(update_query, (email))
        connection.commit()
        print("Data Updated")'''
    else:
        insert_query = """
        INSERT INTO `_iot_user` 
        (`id`, `user_id`, `name`, `email`, `activated`)
        VALUES (NULL, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, name, email, activated))
        connection.commit()

    cursor.close()
    connection.close()
    
def get_user_by_email(email):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor
        cursor = connection.cursor()
        
        select_query = "SELECT user_id FROM _iot_user WHERE email = %s AND activated = 1"
        cursor.execute(select_query, (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return existing_user[0]
        return None
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None

    finally:
        if connection:
            connection.close()
        if connection:
            connection.close()
            
def get_userid_by_token(access_token):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor
        cursor = connection.cursor()
        
        select_query = "SELECT user_id FROM _iot_user WHERE access_token = %s"
        cursor.execute(select_query, (access_token,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return existing_user[0]
        return None
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None

    finally:
        if connection:
            connection.close()
        if connection:
            connection.close()
            
def get_user_by_refreshToken(refreshToken):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor
        cursor = connection.cursor()
        
        select_query = "SELECT email FROM _iot_user WHERE refresh_token = %s"
        cursor.execute(select_query, (refreshToken,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return existing_user[0]
        return None
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None

    finally:
        if connection:
            connection.close()
        if connection:
            connection.close()

def get_user_by_token(access_token):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor
        cursor = connection.cursor()
        
        select_query = "SELECT email FROM _iot_user WHERE access_token = %s"
        cursor.execute(select_query, (access_token,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return existing_user[0]
        return None
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None

    finally:
        if connection:
            connection.close()
        if connection:
            connection.close()
            
            
def update_user_by_email(email, access_token, refresh_token, access_expires_in):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor
        cursor = connection.cursor()

        update_query = """
        UPDATE _iot_user
        SET access_token = %s, 
            expires_in = NOW() + INTERVAL %s SECOND, 
            refresh_token = %s, 
            activated = 1
        WHERE email = %s
        """

        cursor.execute(update_query, (access_token, access_expires_in, refresh_token, email))
        connection.commit()

        return True

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False  # Return False on error

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def getDevice(device_id):
    data = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor
        cursor = connection.cursor()
        
        cursor.callproc("GetDeviceStatus", (device_id,))
        
        results = cursor.stored_results()
        
        
        for result in results:
            for row in result:
                data = row
                
                    
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if connection:
            connection.close()
        if connection:
            connection.close()

        return data
            
def getDeviceStatus(device_id, component):
    
    data = 0
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor
        cursor = connection.cursor()
        
        cursor.callproc("GetDeviceStatus", (device_id,))
        
        results = cursor.stored_results()
        
        for result in results:
            for row in result:
                #print(row)
                if component == 'ON':
                    sh1 = row[0]
                    sh2 = row[1]
                    sh3 = row[2]
                    sh4 = row[3]
                    sh5 = row[4]
                    sh6 = row[5]
                    
                    if sh1 or sh2 or sh3 or sh4 or sh5 or sh6:
                        data = 1
                        
                if component == 'BR':
                    br = row[10]
                    print(f"BR:{br}")
                    data = br
                    
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if connection:
            connection.close()
        if connection:
            connection.close()

        return data
        

def updateDeviceStatus(query):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        print(f"Query: {query}")

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        print(f"DB Updated | Rows affected: {cursor.rowcount}")

        return True

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass




def putEmailCheckForAuth(email, user_id):
    name = "Customer"
    activated = 1
    authTime = datetime.now()
    
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    # Create a cursor
    cursor = connection.cursor()
    
    select_query = "SELECT user_id FROM _iot_user WHERE email = %s"
    cursor.execute(select_query, (email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        # User with the same user_id already exists
        print("User with the same email already exists---")
        sql_query = "UPDATE `_iot_user` SET `_authRec`=NOW() WHERE `email` = %s"
        cursor.execute(sql_query, (email,))
        connection.commit()
        print("Data Updated")
    else:
        insert_query = """
        INSERT INTO `_iot_user` 
        (`id`, `user_id`, `name`, `email`, `activated`, _authRec)
        VALUES (NULL, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, name, email, activated, authTime))
        connection.commit()
        print("Data Insirted")

    cursor.close()
    connection.close()
    

def matchforAuth():
    __email = None
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    cursor = connection.cursor()
    
    select_query = "SELECT email FROM _iot_user WHERE _authRec > NOW() - INTERVAL 60 SECOND ORDER BY _authRec LIMIT 1"
    cursor.execute(select_query, ())
    existing_user = cursor.fetchone()
    
    if existing_user:
        __email = existing_user[0]
        print("User Found")
        print(__email)
        print("--")
        sql_query = "UPDATE `_iot_user` SET `_authRec`=NULL WHERE `email` = %s"
        cursor.execute(sql_query, (__email,))
        connection.commit()
    else:
        print("User Not Found")
    
    cursor.close()
    connection.close()
    
    return __email

