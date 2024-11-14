import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up TRIG and ECHO pins
TRIG = 20
ECHO = 21

# Set the TRIG pin as output and ECHO pin as input
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Ensure the TRIG pin is low initially
GPIO.output(TRIG, GPIO.LOW)

print("Waiting for sensor to settle...")
time.sleep(2)

try:
    while True:
        # Send a pulse to TRIG
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microseconds pulse
        GPIO.output(TRIG, GPIO.LOW)

        # Measure the time it takes for the pulse to return to ECHO
        while GPIO.input(ECHO) == GPIO.LOW:
            pulse_start = time.time()

        while GPIO.input(ECHO) == GPIO.HIGH:
            pulse_end = time.time()

        # Calculate the distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s, divided by 2 for the round trip
        distance = round(distance, 2)

        print(f"Distance: {distance} cm")

        # Wait for a short time before measuring again
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
