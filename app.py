# 1. Import required libraries
from flask import Flask, render_template, request
import os
from asset_utils import asset_to_hostname

# 2. Initialize Flask app
app = Flask(__name__)

# 3. Define a function to interact with ServiceNow CLI and retrieve hostname and IP address
def get_snow_info(hostname, os_type):
    # Retrieve hostname and IP address from ServiceNow using SNOW CLI
    # Adapt this command to your specific use case
    # Use the appropriate command for your environment
    snow_cli_command = f"snow find {hostname}"
    snow_output = os.popen(snow_cli_command).read()
    
    # Parse the output to extract hostname and IP address
    # This depends on the output format of your SNOW CLI command
    # (use regex or string manipulation to extract the required data)
    
    return hostname, ip_address

# 4. Define the route for the main page (index) with a form for user input
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user inputs from the form
        asset_number = request.form['asset_number']
        os_type = request.form['os_type']
        
        # Convert asset number to hostname
        hostname = asset_to_hostname(asset_number)
        
        # Call get_snow_info function to retrieve the hostname and IP address
        hostname, ip_address = get_snow_info(hostname, os_type)
        
        # Redirect to the result page with the retrieved information
        return render_template('result.html', hostname=hostname, ip_address=ip_address)
    else:
        # Render the main page with the form for user input
        return render_template('index.html')

# 5. Define the route for the result page to display the retrieved information
@app.route('/result')
def result():
    # Render the result page with the retrieved hostname and IP address
    return render_template('result.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
