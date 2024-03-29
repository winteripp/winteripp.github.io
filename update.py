import requests
import socket
import schedule
import time

def get_public_ip():
    # Use a public service to get the public IP address
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        public_ip = data['ip']
        return public_ip
    except Exception as e:
        print(f"Error getting public IP: {e}")
        return None

def update_public_ip():
    # Set the URL of your Flask server
    server_url = 'https://winterip.pythonanywhere.com/'

    # Get the public IP address
    public_ip = get_public_ip()

    if public_ip:
        try:
            # Make a GET request to the Flask server to get the current message
            response = requests.get(server_url)
            current_message = response.text

            # Compare the public IP with the current message
            if public_ip != current_message:
                # If different, send a POST request to update the message
                requests.post(server_url, data=public_ip)
                print(f"Public IP updated to: {public_ip}")
            else:
                print("Public IP is already up to date.")
        except Exception as e:
            print(f"Error communicating with the Flask server: {e}")
    else:
        print("Unable to retrieve public IP.")

# Schedule the task every 5 minutes
schedule.every(5).minutes.do(update_public_ip)

while True:
    # Run the scheduled tasks
    schedule.run_pending()

    # Sleep for a short interval to avoid high CPU usage
    time.sleep(1)
