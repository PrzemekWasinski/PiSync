import RPi.GPIO as GPIO
import subprocess
import time

#GPIO Pins
LED_IDLE = 17 #Green LED
LED_BUSY = 27 #Red LED
BUTTON = 22 #Button input

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_IDLE, GPIO.OUT)
GPIO.setup(LED_BUSY, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Turn on Idle LED 
GPIO.output(LED_IDLE, GPIO.HIGH)
GPIO.output(LED_BUSY, GPIO.LOW)

#Path to sync script
SYNC_SCRIPT = '/home/przemek/sync/sync.sh'

#Track last hourly sync
last_hourly_run = time.time()

is_running = False

def run_sync():
    global is_running
    if is_running:
        return  

    is_running = True
    GPIO.output(LED_IDLE, GPIO.LOW)
    GPIO.output(LED_BUSY, GPIO.HIGH)

    #Run bash script
    try:
        subprocess.run([SYNC_SCRIPT])
    except Exception as e:
        print(f"Error running sync: {e}")

    GPIO.output(LED_BUSY, GPIO.LOW)
    GPIO.output(LED_IDLE, GPIO.HIGH)
    is_running = False

try:
    while True:
        #On buton press
        if GPIO.input(BUTTON) == GPIO.LOW:  
            print("Button press")
            run_sync()
            time.sleep(0.5) 

        #Hourly sync
        current_time = time.time()
        if current_time - last_hourly_run >= 3600:  #Sync every 1h (3600s)
            run_sync()
            last_hourly_run = current_time

        time.sleep(1)

finally:
    GPIO.cleanup()
