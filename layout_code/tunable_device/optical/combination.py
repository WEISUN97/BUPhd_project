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
position_1 = optical_thermal(gen, connector, 0, 0, "A", True)
# buttom left
position_3 = optical_thermal(gen, connector, 0, -3000, "B", False)
# top right
position_2 = optical_comb(gen, connector, 7500, 0, "C", True)
# buttom left
position_4 = optical_comb(gen, connector, 7500, -3000, "D", False)


gen.generate(
    "result_wei/tunable_device/combination/combination.cnst",
    "result_wei/tunable_device/combination/combination.gds",
    show=True,
)
