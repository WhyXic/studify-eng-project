import RPi.GPIO as GPIO
from time import sleep, time

# Ultrasonic Sensor Pins
TRIG_PIN = 23
ECHO_PIN = 24

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    """Measure the distance using the ultrasonic sensor."""
    # Send pulse
    GPIO.output(TRIG_PIN, GPIO.LOW)
    sleep(0.1)
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for echo response
    pulse_start = time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time()

    pulse_end = time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Calculate distance in cm
    return distance

def is_object_detected(threshold=10):
    """Check if an object is within the threshold distance."""
    distance = measure_distance()
    return distance < threshold
