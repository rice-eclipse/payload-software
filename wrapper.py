from main_system.components import BigWrapper
from main_system.components import AltimeterReader
from main_system.components import GyroscopeReader
from main_system.components import AccelReader

from test_system.components import SimAltReader
from test_system.components import SimGyroReader
from test_system.components import SimAccelReader

maincontroller = BigWrapper(AltimeterReader, GyroscopeReader, AccelReader)

maincontroller.run()