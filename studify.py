import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep, time
import sys

# Set up DHT11 sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# Grove Speaker Pin
SPEAKER_PIN = 18

# Ultrasonic Sensor Pins
TRIG_PIN = 23
ECHO_PIN = 24

# Constants for timers
POMODORO_DURATION = 25 * 60  # 25 minutes
BREAK_DURATION = 5 * 60      # 5 minutes

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# Ultrasonic sensor setup
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Speaker PWM setup
speaker = GPIO.PWM(SPEAKER_PIN, 1000)  # Set frequency to 1kHz

# Function to read temperature
def read_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature

# Function to play speaker alert
def play_alert():
    speaker.start(50)
    sleep(0.5)
    speaker.stop()

def play_pomodoro_complete_sound():
    for _ in range(3):
        speaker.start(50)
        sleep(0.3)
        speaker.stop()
        sleep(0.2)

# Function to measure distance using ultrasonic sensor
def measure_distance():
    # Send pulse
    GPIO.output(TRIG_PIN, GPIO.LOW)
    sleep(0.1)
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for response
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time()
    
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Calculate distance in cm
    return distance

# Function to run Pomodoro timer
def pomodoro_timer():
    start_time = time()
    print("Pomodoro: Focus")
    
    while time() - start_time < POMODORO_DURATION:
        remaining = POMODORO_DURATION - int(time() - start_time)
        print(f"Focus: {remaining // 60:02}:{remaining % 60:02}")
        sleep(1)
        
        # Check temperature during Pomodoro
        temp = read_temperature()
        if temp and temp > 30:
            print(f"Temp: {temp:.1f}C!")
            play_alert()
            sleep(2)
    
    play_pomodoro_complete_sound()

# Break timer function
def break_timer():
    start_time = time()
    print("Break: Relax")

    while time() - start_time < BREAK_DURATION:
        remaining = BREAK_DURATION - int(time() - start_time)
        print(f"Break: {remaining // 60:02}:{remaining % 60:02}")
        sleep(1)

# Main loop
try:
    while True:
        pomodoro_timer()
        break_timer()

        # Check for ultrasonic sensor proximity (example use case)
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        if distance < 10:
            print("Object detected close by!")
            play_alert()
            sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    speaker.stop()
    GPIO.cleanup()
    sys.exit()
