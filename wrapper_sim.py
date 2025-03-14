import signal
import sys

from main_system.components.BigWrapper import BigWrapper

from test_system.components.SimAltReader import SimAltReader
from test_system.components.SimGyroReader import SimGyroReader
from test_system.components.SimAccelReader import SimAccelReader
from test_system.components.SimTempReader import SimTempReader

# An asynchronous signal handler.
# If the user hits CTRL+C, dump the logs to disk and exit regardless of our position in the BigWrapper loops.
def handle_sigint(signum, frame):
    print('Handling SIGINT. Dumping logs.')
    
    if (maincontroller != None):
        maincontroller.force_write_logs()
        sys.exit(0)

# All configs related to running the MainSoftwareSystem in its real launch configuration
# is contained in config.json.

# Configurations and pathing for running the MainSoftwareSystem in the testing environment 
# are still primarily contained in config.json, but the paths for the data sources for the 
# simulated readers need to be configured in their respective files.

# Note that the simulated readers need to have their paths reconfigured in their files to the desired data sources.
maincontroller = BigWrapper(SimAltReader, SimGyroReader, SimAccelReader, SimTempReader)

# Install the signal handler.
signal.signal(signal.SIGINT, handle_sigint)

try:
    # Run the main loop.
    maincontroller.run()
except Exception as e:
    print(f'Exception caught: {e}.')
    print('Initializing emergency imaging sequence.')
    maincontroller.emergency_run()