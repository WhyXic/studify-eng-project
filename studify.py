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
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

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

def play_emergency_alert():
    """Plays a continuous beeping sound if no object is detected."""
    print("No object detected! Stopping Pomodoro...")
    while True:
        speaker.start(90)
        sleep(0.1)
        speaker.stop()
        sleep(0.1)

# Function to run Pomodoro timer
def pomodoro_timer():
    start_time = monotonic()
    print("Pomodoro: Focus")
    
    while monotonic() - start_time < POMODORO_DURATION:
        remaining = POMODORO_DURATION - int(monotonic() - start_time)
        print(f"Focus: {remaining // 60:02}:{remaining % 60:02}")
        sleep(1)

        # Check temperature during Pomodoro
        temp = read_temperature()
        if temp and temp > 30:
            print(f"Temp: {temp:.1f}C!")
            play_alert()
            sleep(2)

        # Check if the ultrasonic sensor detects no object within 10 cm
        if not ultrasonic.is_object_detected(10):
            play_emergency_alert()
            break

    play_pomodoro_complete_sound()

# Break timer function
def break_timer():
    start_time = monotonic()
    print("Break: Relax")

    while monotonic() - start_time < BREAK_DURATION:
        remaining = BREAK_DURATION - int(monotonic() - start_time)
        print(f"Break: {remaining // 60:02}:{remaining % 60:02}")
        sleep(1)

# Main loop
try:
    while True:
        pomodoro_timer()
        break_timer()

except KeyboardInterrupt:
    print("Exiting...")
finally:
    speaker.stop()
    GPIO.cleanup()
    sys.exit()
