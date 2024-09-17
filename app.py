from flask import Flask, request, jsonify
import requests
import subprocess
import re
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Enable CORS for all routes
CORS(app)

# Vulners API key
API_KEY = os.getenv('API_KEY')


# Function to log messages and accumulate logs
def log(message, logs):
    print(message)
    logs.append(message)

def get_server_info(url, logs):
    log(f'Performing curl -I for {url}...', logs)
    try:
        result = subprocess.run(['curl', '-I', url], capture_output=True, text=True, check=True)
        headers = result.stdout
        log('Received headers:', logs)
        log(headers, logs)
        server_line = next((line for line in headers.splitlines() if line.lower().startswith('server:')), None)
        if server_line:
            server_info = server_line.split(':', 1)[1].strip()
            log(f'Server information: {server_info}', logs)
            return server_info
        else:
            log('No server information found.', logs)
            return None
    except subprocess.CalledProcessError as e:
        log(f'Failed to run curl: {e}', logs)
        return None
    except Exception as e:
        log(f'Exception occurred while getting server info: {e}', logs)
        return None

def search_vulnerabilities(server_info, logs):
    log(f'Searching for vulnerabilities related to {server_info}...', logs)
    try:
        query = server_info
        url = f'https://vulners.com/api/v3/search/lucene/?query={query}'
        response = requests.get(url, headers={'Authorization': f'Bearer {API_KEY}'})
        
        if response.status_code == 200:
            log('Request to Vulners API successful.', logs)
            data = response.json()
            log('Data retrieved from API:', logs)
            log(str(data), logs)  # Logging the raw response data
            return data
        else:
            log(f'Error: {response.status_code} - {response.text}', logs)
            return {'error': f'Error: {response.status_code} - {response.text}'}
    except Exception as e:
        log(f'Exception occurred while searching vulnerabilities: {e}', logs)
        return {'error': str(e)}

def extract_services_and_versions(text):
    # Revised regex pattern to accurately capture service names and versions
    pattern = re.compile(r'([a-zA-Z][\w\s\-\.]*[a-zA-Z])\s*(?:\[(\d+\.\d+\.\d+|\d+\.\d+|\d+)\]|(\d+\.\d+\.\d+|\d+\.\d+|\d+))', re.IGNORECASE)
    
    # Find all matches in the text
    matches = pattern.findall(text)
    
    # Create a list to store the services and their versions
    services = []
    
    for match in matches:
        service_name = match[0].strip()
        version_with_brackets = match[1]
        version_without_brackets = match[2]
        
        # Only add valid service names
        if version_with_brackets:
            services.append(f'{service_name}[{version_with_brackets}]')
        elif version_without_brackets:
            services.append(f'{service_name} {version_without_brackets}')
    
    return services

def run_searchSploit(service):
    try:
        if "HTML" in service:
            return
        command = ['searchsploit', service]
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Remove ANSI escape codes
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)

        # Extract lines with exploit titles
        # The exploit title lines are between 'Exploit Title' and 'Shellcodes: No Results'
        lines = clean_output.split('\n')
        start_index = 0
        end_index = len(lines)

        for i, line in enumerate(lines):
            if 'Exploit Title' in line:
                start_index = i + 1
            if 'Shellcodes: No Results' in line:
                end_index = i

        # Extract titles and clean up
        titles = []
        for line in lines[start_index:end_index]:
            # Filter out empty lines and trim whitespace
            line = line.strip()
            if line and '|' in line:
                title = line.split('|')[0].strip()
                if title:
                    titles.append(title)

        # Join the titles into a single string with newlines
        formatted_output = '\n'.join(titles)
        
        if 'Exploits: No Results' in clean_output:
            print (f"No exploits found for {service}")
            return {"service":service,"vulns":[]}
        
        return {"service":service,"vulns":formatted_output.replace('\x1b','').replace('[K','').split('\n')}
    except subprocess.CalledProcessError as e:
        return f"An error occurred with searchsploit: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
            

def run_whatweb(url):
    try:
        # Construct the command
        command = ['whatweb', url]
        
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Output the result
        print("WhatWeb Output:")
        res = result.stdout
        
        # Clean the output to remove unwanted characters and formatting
        res_clean = re.sub(r'\x1b\[[0-9;]*m', '', res)  # Remove ANSI escape codes
        print("Cleaned Output:")
        print(res_clean)
        
        # Extract services and versions
        services = extract_services_and_versions(res_clean)
        print("Extracted Services and Versions:")
        res=list(set([""+x.replace('[',' ').replace(']','') for x in services]))
        print(res)
        
        exploits=[]
        for i in res:
            if i and 'HTML' not in i:
                exploits.append(run_searchSploit(i)) 
        return {"services": res, "exploits": exploits}        
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
    except FileNotFoundError:
        return "Error: 'whatweb' command not found. Please make sure it is installed and accessible."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# API 1: /scanv2 (Vulners + Curl)
@app.route('/scanv2', methods=['POST'])
def scanv2():
    # url = request.form.get('url')
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'})

    # Initialize logs for this request
    logs = []

    # Get server information from the URL
    server_info = get_server_info(url, logs)
    if not server_info:
        return jsonify({'error': 'Unable to retrieve server information', 'logs': logs})

    # Search for vulnerabilities based on server information
    vulnerabilities = search_vulnerabilities(server_info, logs)

    # Include logs in the response
    response = {
        'server_info': server_info,
        'vulnerabilities': vulnerabilities,
        'logs': logs
    }

    return jsonify(response)

# API 2: /scan (WhatWeb + SearchSploit)
@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    result = run_whatweb(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
