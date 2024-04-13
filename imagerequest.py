import requests
import time
from datetime import datetime
from processing import process_image
from temeprature_sensor import measure_mercury_length

def download_image():
    # Put IP adress here
    url = 'http://192.168.2.21:4747/cam/1/frame.jpg'

    response = requests.get(url)

    if response.status_code == 200:

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_with_timestamp = f'frame_{timestamp}.jpg'

        with open('frame.jpg', 'wb') as file:
            file.write(response.content)
        
        with open("failsafe"+filename_with_timestamp, 'wb') as file:
            file.write(response.content)
        
        print(f"Image saved successfully as {filename_with_timestamp}.")
    else:
        print("Failed to retrieve image. Status code:", response.status_code)

# Run download_image() every hour
def addNumbertoCsv(number):
    with open('number.csv', 'a') as file:
        file.write(f'{number}\n')
    print(f"Number {number} added to file.")

try:
    while True:
        download_image()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        process_image(timestamp)
        length = measure_mercury_length('thermometer.jpg')
        addNumbertoCsv(length)
        time.sleep(10800)  # Delay for 3 hour in seconds
except KeyboardInterrupt:
    print("Program stopped by user.")
