# test_connect.py

import requests

host = "gabshost"
connector = "user1"
base_url = "http://127.0.0.1:5000"

try:
    # 1. Connect the user
    response = requests.post(
        f"{base_url}/connect",
        json={"host": host, "connector": connector},
        timeout=5
    )
    print("Connect:", response.status_code, response.text)

    # 2. Send a key
    response = requests.post(
        f"{base_url}/send",
        json={"host": host, "connector": connector, "key": "right"},
        timeout=5
    )
    print("Send key:", response.status_code, response.text)

    # 3. Check host status
    response = requests.get(
        f"{base_url}/status/{host}",
        timeout=5
    )
    print("Status:", response.status_code, response.text)

except requests.exceptions.RequestException as e:
    print("❌ Network or server error:", e)
except Exception as e:
    print("❌ Unexpected error:", e)
