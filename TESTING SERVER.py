import requests

# Replace with the ESP32's IP address
esp32_ip = "http://192.168.45.245/read"

def get_data():
    response = requests.get(esp32_ip)
    if response.status_code == 200:
        print("Data from SD Card:\n", response.text)
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    get_data()
