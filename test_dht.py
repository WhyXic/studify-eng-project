import adafruit_dht
import board
import time

# Change DHT22 to DHT11 if you're using that model
DHT_SENSOR = adafruit_dht.DHT22(board.D4)  # Change board.D4 if you're using a different GPIO pin

print("Testing DHT Sensor...")

while True:
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity

        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        else:
            print("Sensor read failed, retrying...")

        # Sleep for 2 seconds before the next read
        time.sleep(2)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep trying
        print(f"RuntimeError: {error.args[0]}")
        time.sleep(2.0)
        continue
    except Exception as error:
        DHT_SENSOR.exit()
        raise error
