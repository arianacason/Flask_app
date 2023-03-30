# Import required libraries
from flask import Flask, render_template, request, jsonify
import os
import paramiko
import time
from asset_utils import asset_to_hostname

# Initialize Flask app
app = Flask(__name__)

# Define a function to interact with ServiceNow CLI and retrieve hostname and IP address
def get_snow_info(hostname, os_type):
    # Retrieve hostname and IP address from ServiceNow using SNOW CLI
    snow_cli_command = f"snow find {hostname}"
    snow_output = os.popen(snow_cli_command).read()

    # Parse the output to extract hostname and IP address
    # This depends on the output format of your SNOW CLI command
    # (use regex or string manipulation to extract the required data)

    return hostname, ip_address

# Function to establish SSH connection, copy ISO image, and disconnect
def copy_iso_image(hostname, root_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username='root', password=root_password)
        # Execute commands here to copy the ISO image from the repository
        # Example: ssh.exec_command("cp /path/to/repo/iso_image /destination/path")

        # Simulate installation progress
        for progress in range(0, 101, 10):
            time.sleep(1)
            print(f"Installation progress: {progress}%")

    except paramiko.AuthenticationException:
        return False
    finally:
        ssh.close()

    return True

# Define the route for the main page (index) with a form for user input
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user inputs from the form
        asset_number = request.form['asset_number']
        os_type = request.form['os_type']
        root_password = request.form['root_password']

        # Convert asset number to hostname
        hostname = asset_to_hostname(asset_number)

        # Call get_snow_info function to retrieve the hostname and IP address
        hostname, ip_address = get_snow_info(hostname, os_type)

        # Attempt to copy the ISO image
        success = copy_iso_image(hostname, root_password)

        if success:
            # Redirect to the result page with the retrieved information
            return render_template('result.html', hostname=hostname, ip_address=ip_address)
        else:
            return render_template('index.html', error="Failed to copy ISO image. Check your root password.")
    else:
        # Render the main page with the form for user input
        return render_template('index.html')

# Define the route for the result page to display the retrieved information
@app.route('/result')
def result():
    # Render the result page with the retrieved hostname and IP address
    return render_template('result.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

