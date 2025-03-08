import signal
import sys

from main_system.components.BigWrapper import BigWrapper

from main_system.components.AltimeterReader import AltimeterReader
from main_system.components.GyroscopeReader import GyroscopeReader
from main_system.components.AccelReader import AccelReader

# An asynchronous signal handler.
# If the user hits CTRL+C, dump the logs to disk and exit regardless of our position in the BigWrapper loops.
def handle_sigint(signum, frame):
    print('Handling SIGINT. Dumping logs.')
    
    if (maincontroller != None):
        maincontroller.force_write_logs()
        sys.exit(0)

# All configs related to running the MainSoftwareSystem in its real launch configuration
# is contained in config.json.

# Note that BigWrapper reads its control and imaging configs from config.json in ./main_system/components/config.json
maincontroller = BigWrapper(AltimeterReader, GyroscopeReader, AccelReader)

# Install the signal handler.
signal.signal(signal.SIGINT, handle_sigint)

try:
    # Run the main loop.
    maincontroller.run()
except Exception as e:
    print(f'Exception caught: {e}.')
    print('Initializing emergency imaging sequence.')
    maincontroller.emergency_run()