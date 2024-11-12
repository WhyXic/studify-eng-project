import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import pygame
import board
import busio
from adafruit_ht16k33.segments import Seg7x4

# Setup for Ultrasonic Sensor
TRIG = 17
ECHO = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Setup for DHT22 Temperature Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Setup for Display
i2c = busio.I2C(board.SCL, board.SDA)
display = Seg7x4(i2c)

# Setup for Speaker
pygame.mixer.init()
alert_sound = "alert.wav"

# Constants
TEMP_THRESHOLD = 30  # Temperature threshold in Celsius
DISTRACTION_THRESHOLD = 10  # Seconds to trigger alert if away from desk
WORK_DURATION = 25 * 60  # 25 minutes in seconds
BREAK_DURATION = 5 * 60   # 5 minutes in seconds

# Variables
distraction_start = None
pomodoro_running = True
timer_end = time.time() + WORK_DURATION

def measure_distance():
    """Get the distance using the ultrasonic sensor."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
    
    # Calculate distance
    elapsed = stop_time - start_time
    distance = (elapsed * 34300) / 2  # Speed of sound = 34300 cm/s
    return distance

def get_temperature():
    """Get the temperature reading from DHT22 sensor."""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature

def play_alert():
    """Play an alert sound."""
    pygame.mixer.music.load(alert_sound)
    pygame.mixer.music.play()

def display_status(temperature, time_left, session_type):
    """Display current status on the display."""
    display.fill(0)
    mins, secs = divmod(time_left, 60)
    display.print(f"{session_type[:4]} {mins:02}:{secs:02}")
    display.show()
    print(f"Temp: {temperature:.1f}°C, Timer: {mins:02}:{secs:02}, Session: {session_type}")

try:
    while True:
        # Measure temperature
        temperature = get_temperature()
        
        # Check for high temperature alert
        if temperature and temperature > TEMP_THRESHOLD:
            print("Warning: Temperature too high!")
            play_alert()

        # Check user presence
        distance = measure_distance()
        present = distance < 100  # Adjust this threshold if needed

        # Handle distraction alert
        if present:
            distraction_start = None
        else:
            if distraction_start is None:
                distraction_start = time.time()
            elif time.time() - distraction_start > DISTRACTION_THRESHOLD:
                print("You've been away for too long!")
                play_alert()

        # Handle Pomodoro Timer
        time_left = timer_end - time.time()
        if time_left <= 0:
            # Switch between work and break sessions
            if pomodoro_running:
                print("Time for a break!")
                play_alert()
                timer_end = time.time() + BREAK_DURATION
                pomodoro_running = False
            else:
                print("Back to work!")
                play_alert()
                timer_end = time.time() + WORK_DURATION
                pomodoro_running = True
        
        # Display status
        session_type = "Work" if pomodoro_running else "Break"
        display_status(temperature, time_left, session_type)
        
        # Sleep for a short interval before the next loop iteration
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    display.fill(0)
    display.show()
