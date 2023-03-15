# Import required modules and libraries.
import snow_api_module
import os

# Create a Flask app instance.
app = Flask(__name__)

# Define a function to retrieve the hostname of the server via user input.
def get_hostname():
    hostname = request.form['hostname']
    return hostname

# Define a function to retrieve the type of operating system user wants installed or upgraded via user input.
def get_os():
    os_type = request.form['os_type']
    return os_type

# Define a function to retrieve the hostname and IP address from SNOW.
def get_host_details(hostname):
    host_details = snow_api_module.get_host_details(hostname)
    return host_details

# Define a function to install or upgrade the operating system on the specified server.
def install_os(hostname, os_type):
    os.system(f'ssh {hostname} "sudo apt-get install {os_type}"')

# Define a route to the homepage of the app.
@app.route('/')
def home():
    return 'Welcome to the OS installer/upgrader app!'

# Define a route to the form for retrieving user input.
@app.route('/install', methods=['GET', 'POST'])
def install_form():
    if request.method == 'POST':
        # Get hostname and OS from form data
        hostname = get_hostname()
        os_type = get_os()
        # Get host details from SNOW
        host_details = get_host_details(hostname)
        # Install or upgrade OS on the specified server
        install_os(hostname, os_type)
        # Return success message
        return f'OS installation/upgradation on {hostname} successful!'
    else:
        # Render the install form template
        return render_template('install_form.html')

# Run the app.
if __name__ == '__main__':
    app.run()
