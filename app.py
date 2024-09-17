from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)

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
        if 'Exploits: No Results' in result.stdout:
            return f"No exploits found for {service}"
        return result.stdout
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
            if i:
                exploits.append(run_searchSploit(i)) 
        return {"services": res, "exploits": exploits}        
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
    except FileNotFoundError:
        return "Error: 'whatweb' command not found. Please make sure it is installed and accessible."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    result = run_whatweb(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
