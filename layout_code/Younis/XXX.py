import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnst_gen import CNSTGenerator
from geo import tJunction, RectangleC, RectangleLH, roundedCorners, Structure

r = 0.2  # round corner
x_beam = 0
y_beam = 0
w_support = 2
L_support = 2
w_beam = 0.2
L_beam = 10
gap_1 = 5  # gap between electrodes and beams
gap_2 = 30  # gap between electrodes in y direction
gap_actuators_x = 0.5  # gap between actuators
gap_actuators_y = 0.1
L_actuators = [3, 3, 2]
h_actuators = 0.2
L_electrode = 250

connector = Structure("Connector")
for i in range(1):
    # beams and supports
    connector.add(
        (
            tJunction(x_beam, y_beam, w_support, w_beam, L_support, L_beam),
            roundedCorners(
                x_beam + w_support / 2 + r,
                y_beam + (L_support + w_beam) / 2 + r,
                r,
                180,
            ),
            roundedCorners(
                x_beam + w_support / 2 + r, y_beam + (L_support - w_beam) / 2 - r, r, 90
            ),
        ),
    )
    # electrodes
    for i in range(3):
        connector.add(
            RectangleLH(
                x_beam - w_support / 2 - gap_1 - L_electrode,
                y_beam + L_support - L_electrode - i * (gap_2 + L_electrode),
                L_electrode,
                L_electrode,
                0,
            ),
        )
    # actuators
    for i in range(3):
        connector.add(
            RectangleLH(
                x_beam + w_support / 2 + (i + 1) * gap_actuators_x + i * L_actuators[0],
                y_beam + L_support / 2 - w_beam - gap_actuators_y - h_actuators,
                L_actuators[i],
                h_actuators,
                0,
            ),
        )

    # cables


gen = CNSTGenerator(shapeReso=0.1)
gen.add("2 layer")
gen.add(connector)
gen.generate("result_wei/XXX.cnst", "result_wei/XXX.gds", show=True)
