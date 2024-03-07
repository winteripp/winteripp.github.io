# auto_update_ip.py

import requests
import re
import schedule
import time
from subprocess import run

# Function to get public IP address
def get_public_ip():
    response = requests.get('https://api64.ipify.org?format=json')
    ip_data = response.json()
    return ip_data['ip']

# Function to update index.html file
def update_index_html(new_ip):
    css_style = '''
        body {
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 20px;
        }

        #public-ip {
            font-size: 2em;
            color: #333;
            margin-bottom: 20px;
        }
    '''

    html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Public IP Display</title>
            <style>{css_style}</style>
        </head>
        <body>
            <h1>Your Public IP</h1>
            <p id="public-ip">{new_ip}</p>

            <script>
                // JavaScript code (if needed)
            </script>
        </body>
        </html>
    '''

    with open('index.html', 'w') as file:
        file.write(html_content)

# Function to check and update IP
def check_and_update_ip():
    current_ip = get_public_ip()
    print(f"Current Public IP: {current_ip}")
    update_index_html(current_ip)

    # Check if there are changes in the repository
    result = run(["git", "diff", "--quiet", "index.html"])
    if result.returncode == 1:
        # Commit changes
        run(["git", "add", "index.html"])
        run(["git", "commit", "-m", "Update public IP"])

        # Push changes with access token
        access_token = "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"
        username = "winteripp"
        repo_name = "your_repository_name"
        run(["git", "push", f"https://{access_token}@github.com/{username}/{repo_name}.git", "master"])
        print("Changes committed and pushed to GitHub.")
    else:
        print("No changes detected.")

# Schedule the task every 5 minutes
schedule.every(5).minutes.do(check_and_update_ip)

while True:
    schedule.run_pending()
    time.sleep(1)
