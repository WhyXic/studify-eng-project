import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep, time
import sys

# Set up components
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# LCD Pin setup
LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11

# Grove Speaker Pin
SPEAKER_PIN = 18

# Constants for LCD
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

# Timer durations
POMODORO_DURATION = 25 * 60  # 25 minutes
BREAK_DURATION = 5 * 60      # 5 minutes

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# Speaker PWM setup
speaker = GPIO.PWM(SPEAKER_PIN, 1000)  # Set frequency to 1kHz

# LCD initialization
def lcd_init():
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    lcd_command(0x33) # Initialize
    lcd_command(0x32) # Set to 4-bit mode
    lcd_command(0x28) # 2 line, 5x7 matrix
    lcd_command(0x0C) # Turn cursor off
    lcd_command(0x06) # Shift cursor right
    lcd_command(0x01) # Clear display

def lcd_command(bits):
    GPIO.output(LCD_RS, LCD_CMD)
    send_to_lcd(bits)

def lcd_char(bits):
    GPIO.output(LCD_RS, LCD_CHR)
    send_to_lcd(bits)

def send_to_lcd(bits):
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    GPIO.output(LCD_E, True)
    sleep(0.001)
    GPIO.output(LCD_E, False)

    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    GPIO.output(LCD_E, True)
    sleep(0.001)
    GPIO.output(LCD_E, False)

def lcd_display(message):
    lcd_command(0x01)  # Clear display
    for char in message:
        lcd_char(ord(char))

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

# Function to run Pomodoro timer
def pomodoro_timer():
    start_time = time()
    lcd_display("Pomodoro: Focus")
    
    while time() - start_time < POMODORO_DURATION:
        remaining = POMODORO_DURATION - int(time() - start_time)
        lcd_display(f"Focus: {remaining // 60:02}:{remaining % 60:02}")
        sleep(1)
        
        # Check temperature during Pomodoro
        temp = read_temperature()
        if temp and temp > 30:
            lcd_display(f"Temp: {temp:.1f}C!")
            play_alert()
            sleep(2)
    
    play_pomodoro_complete_sound()

def break_timer():
    start_time = time()
    lcd_display("Break: Relax")

    while time() - start_time < BREAK_DURATION:
        remaining = BREAK_DURATION - int(time() - start_time)
        lcd_display(f"Break: {remaining // 60:02}:{remaining % 60:02}")
        sleep(1)

# Main loop
try:
    lcd_init()
    while True:
        pomodoro_timer()
        break_timer()

except KeyboardInterrupt:
    print("Exiting...")
finally:
    speaker.stop()
    GPIO.cleanup()
    sys.exit()
