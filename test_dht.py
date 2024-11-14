import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22  # Use DHT11 if that's your sensor type
DHT_PIN = 4  # Adjust this pin number if needed

print("Testing DHT Sensor...")
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if humidity is not None and temperature is not None:
    print(f"Temperature: {temperature:.2f}C, Humidity: {humidity:.2f}%")
else:
    print("Failed to retrieve data from the sensor")
