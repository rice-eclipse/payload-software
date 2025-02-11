from main_system.components import BigWrapper
from main_system.components import AltimeterReader
from main_system.components import GyroscopeReader
from main_system.components import AccelReader

maincontroller = BigWrapper(AltimeterReader, GyroscopeReader, AccelReader)

maincontroller.run()