import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sys

# Pin Definitions
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4           # Adjust if using a different GPIO pin
TRIG_PIN = 23         # Ultrasonic Sensor TRIG pin
ECHO_PIN = 24         # Ultrasonic Sensor ECHO pin
SPEAKER_PIN = 18      # Speaker Signal pin

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

def read_temperature():
    """Read temperature and humidity from DHT22 sensor."""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
    else:
        print("Failed to retrieve data from DHT22 sensor.")

def measure_distance():
    """Measure distance using HC-SR04 ultrasonic sensor."""
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    print(f"Distance: {distance:.2f} cm")

def test_speaker():
    """Test Grove speaker with 5 beeps."""
    print("Testing speaker...")
    for _ in range(5):
        GPIO.output(SPEAKER_PIN, True)
        time.sleep(0.2)
        GPIO.output(SPEAKER_PIN, False)
        time.sleep(0.2)

def main():
    """Main function to handle user input."""
    if len(sys.argv) < 2:
        print("Usage: python3 test_components.py [dht | ultrasonic | speaker]")
        sys.exit(1)

    test_type = sys.argv[1].lower()

    try:
        if test_type == "dht":
            print("Testing DHT22 Temperature Sensor...")
            read_temperature()
        elif test_type == "ultrasonic":
            print("Testing Ultrasonic Sensor...")
            measure_distance()
        elif test_type == "speaker":
            print("Testing Grove Speaker...")
            test_speaker()
        else:
            print("Invalid argument. Use: dht, ultrasonic, or speaker")
    except KeyboardInterrupt:
        print("Test interrupted.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
