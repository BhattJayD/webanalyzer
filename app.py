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
