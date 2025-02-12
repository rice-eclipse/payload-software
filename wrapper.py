from main_system.components import BigWrapper
from main_system.components import AltimeterReader
from main_system.components import GyroscopeReader
from main_system.components import AccelReader

from test_system.components import SimAltReader
from test_system.components import SimGyroReader
from test_system.components import SimAccelReader

# All configs related to running the MainSoftwareSystem in its real launch configuration
# is contained in config.json.

# Configurations and pathing for running the MainSoftwareSystem in the testing environment 
# are still primarily contained in config.json, but the paths for the data sources for the 
# simulated readers need to be configured in their respective files.

# Uncomment this line in order to run BigWrapper with the real sensor readers.
# Note that BigWrapper reads its control and imaging configs from config.json in ./main_system/components/config.json
maincontroller = BigWrapper(AltimeterReader, GyroscopeReader, AccelReader)

# Uncomment this line in order to run BigWrapper with the simulated readers.
# Note that the simulated readers need to have their paths reconfigured in their files to the desired data sources.
# maincontroller = BigWrapper(SimAltReader, SimGyroReader, SimAccelReader)

# Run the main loop.
maincontroller.run()