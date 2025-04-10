import requests
def ask_model(prompt):
    res = requests.post('http://localhost:11434/api/generate', json={
        'model': 'deepseek-coder:6.7b',
        'prompt': prompt,
        'stream': False
    })
    # Check if the response status code is 200 (OK)
    if res.status_code != 200:
        raise Exception(f"Error: {res.status_code} - {res.text}")
    # Check if the response contains JSON data  
    try:
        res.json()
    except ValueError:
        raise Exception("Error: Response is not in JSON format")
    # Check if the response contains the expected keys
    if 'response' not in res.json():
        raise Exception("Error: 'response' key not found in JSON response")
    # Return the 'response' key from the JSON response
    # Check if the 'response' key is empty
    if not res.json()['response']:
        raise Exception("Error: 'response' key is empty")
    return res.json()['response']
prompt = "hello !!"
response = ask_model(prompt)
print(response)