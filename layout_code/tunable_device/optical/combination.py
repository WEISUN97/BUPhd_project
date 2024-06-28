import sys
import math

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator
from layout_code.tunable_device.optical.optical_comb import optical_comb
from layout_code.tunable_device.optical.optical_thermal import optical_thermal

from cnstpy.geo import (
    Structure,
    AlignCustC1,
)

gen = CNSTGenerator(shapeReso=0.01)
connector = Structure("Tunable")
# top left
position_1 = optical_thermal(connector, 0, 0, "A", True)
# buttom left
position_3 = optical_thermal(connector, 0, -3150, "B", False)
# top right
position_2 = optical_comb(connector, 7500, -4, "C", True)
# buttom left
position_4 = optical_comb(connector, 7500, -3154, "D", False)
gen.add(connector)

print("position_1:", position_1)
print("position_2:", position_2)
print("position_3:", position_3)
print("position_4:", position_4)

gen.generate(
    "result_wei/tunable_device/combination/combination.cnst",
    "result_wei/tunable_device/combination/combination.gds",
    show=True,
)
