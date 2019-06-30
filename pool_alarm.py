import sys
import time 

from mpu9250.mpu9250 import mpu9250
from pushetta import Pushetta 


# Constants used in program - change these to change things like thresholds.
Z_THRESHOLD = 0.08

# Global variable because lazy - value that threshold is relative to.
start_value = 0.98
data_max = 0.0

# Infinite loop to constantly send distress call
# every 2 seconds.
#
# Resume program by pressing physical button on
# breadboard.
def alert(p, CHANNEL_NAME, sensor):
    global start_value
    global data_max

    # Shake device hard to reset after alarm trigger.
    Z_RESET = 2.0

    next_msg = time.time()
    print('Alert!')

    time.sleep(0.1)

    # Push message until button press.
    while (sensor.accel[2] < Z_RESET):
        time.sleep(0.01)
        if (time.time() > next_msg):
            next_msg = time.time() + 7.0
            print('Notification')
            #p.pushMessage(CHANNEL_NAME, "CHECK POOL!!!!")

    # Turn off alarm and reset threshold starting value.
    print('Resetting...')
    sys.stdout.flush()
    time.sleep(15)
    data_max = 0.0
    start_value = sensor.accel[2]


def main():
    global start_value
    global data_max

    # Initialize sensor with external library class.
    sensor = mpu9250()

    # Key taken from account.
    API_KEY = "fb2dc4530995b2fe3d3f823a0fa35a5e8d635716"

    # Name of channel.
    CHANNEL_NAME = "JuicySeniorDesign"

    # Create pushetta object.
    p = Pushetta(API_KEY)
    
    print('entering main loop...')
    sys.stdout.flush()
    while True:

        # Get sensor data.
        data = sensor.accel[2]

        # Look at new max value.
        if data > data_max:
            print('New Maximum... {}'.format(data_max))
            data_max = data

        # Thresholding for alarm detection. Adjust magnitude for each axis.           
        if (data_max >= (start_value + Z_THRESHOLD)):
            print('Sending out alert... {} {} {}'.format(data_max, start_value, Z_THRESHOLD))
            sys.stdout.flush()
            alert(p, CHANNEL_NAME, sensor)
            print('Done... {} {} {}'.format(data_max, start_value, Z_THRESHOLD))
            sys.stdout.flush()



if __name__ == "__main__": main()
