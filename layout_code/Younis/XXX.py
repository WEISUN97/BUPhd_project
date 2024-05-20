import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnst_gen import CNSTGenerator
from geo import (
    tJunction,
    hJunction,
    RectangleLH,
    roundedCorners,
    rectSUshape,
    Structure,
)

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
gap_actuators_y = 0.2  # gap between actuators and beams
L_actuators = [
    [3.5, 3.5, 1],
    [3.5, 3.5, 1],
    [3.5, 1, 3.5],
    [3.5, 1, 3.5],
    [7, 7],
    [7, 7],
    [6.5, 2],
]
h_actuators = 0.2
L_electrode = 250

connector = Structure("Connector")
for i in range(7):
    # beams and supports
    if i != 2 and i != 3:
        connector.add(
            (
                tJunction(
                    x_beam, y_beam - i * 850, w_support, w_beam, L_support, L_beam
                ),
                roundedCorners(
                    x_beam + w_support / 2 + r,
                    y_beam + (L_support + w_beam) / 2 + r - i * 850,
                    r,
                    180,
                ),
                roundedCorners(
                    x_beam + w_support / 2 + r,
                    y_beam + (L_support - w_beam) / 2 - r - i * 850,
                    r,
                    90,
                ),
            ),
        )
    else:
        connector.add(
            (
                hJunction(
                    x_beam, y_beam - i * 850, w_support, w_beam, L_support, L_beam
                ),
                roundedCorners(
                    x_beam + w_support / 2 + r,
                    y_beam + (L_support + w_beam) / 2 + r - i * 850,
                    r,
                    180,
                ),
                roundedCorners(
                    x_beam + w_support / 2 + r,
                    y_beam + (L_support - w_beam) / 2 - r - i * 850,
                    r,
                    90,
                ),
                roundedCorners(
                    x_beam + w_support / 2 + L_beam - r,
                    y_beam + (L_support + w_beam) / 2 + r - i * 850,
                    r,
                    270,
                ),
                roundedCorners(
                    x_beam + w_support / 2 + L_beam - r,
                    y_beam + (L_support - w_beam) / 2 - r - i * 850,
                    r,
                    0,
                ),
            ),
        )
    connector.add(
        (
            tJunction(x_beam, y_beam - i * 850, w_support, w_beam, L_support, L_beam),
            roundedCorners(
                x_beam + w_support / 2 + r,
                y_beam + (L_support + w_beam) / 2 + r - i * 850,
                r,
                180,
            ),
            roundedCorners(
                x_beam + w_support / 2 + r, y_beam + (L_support - w_beam) / 2 - r, r, 90
            ),
        ),
    )
# electrodes
for j in range(7):
    for i in range(3):
        connector.add(
            RectangleLH(
                x_beam - w_support / 2 - gap_1 - L_electrode,
                y_beam + L_support - L_electrode - i * (gap_2 + L_electrode) - j * 850,
                L_electrode,
                L_electrode,
                0,
            ),
        )
# actuators
for j in range(7):
    L_actuators_j = L_actuators[j]
    if j < 4 or j == 6:
        gap_actuators_x_temp = gap_actuators_x
        for i in range(len(L_actuators_j)):
            if i > 0:
                gap_actuators_x_temp += L_actuators_j[i - 1] + gap_actuators_x
            connector.add(
                RectangleLH(
                    x_beam + w_support / 2 + gap_actuators_x_temp,
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators
                    - j * 850,
                    L_actuators_j[i],
                    h_actuators,
                    0,
                ),
            )
    elif j == 4 or j == 5:
        connector.add(
            (
                RectangleLH(
                    x_beam + w_support / 2 + gap_actuators_x,
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators
                    - j * 850,
                    L_actuators_j[0],
                    h_actuators,
                    0,
                ),
                RectangleLH(
                    x_beam + w_support / 2 + gap_actuators_x,
                    y_beam + (L_support + w_beam) / 2 + gap_actuators_y - j * 850,
                    L_actuators_j[1],
                    h_actuators,
                    0,
                ),
                rectSUshape(
                    x_beam
                    + w_support / 2
                    + 2 * gap_actuators_x
                    + L_actuators_j[0]
                    + gap_actuators_y
                    + h_actuators / 2,
                    y_beam
                    + (L_support + w_beam) / 2
                    + gap_actuators_y
                    + h_actuators
                    - j * 850,
                    2,
                    1,
                    -2,
                    h_actuators,
                    -90,
                ),
            )
        )

# cables
for j in range(7):
    L_actuators_j = L_actuators[j]
    if j != 4 and j != 5:
        for i in range(len(L_actuators_j)):
            gap_actuators_x_temp = gap_actuators_x
            if i > 0:
                gap_actuators_x_temp += L_actuators_j[i - 1] + gap_actuators_x
            center_start_x = (
                x_beam + w_support / 2 + gap_actuators_x_temp + L_actuators_j[i] / 2
            )
            center_start_y = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators / 2
                - j * 850
            )

    pass


gen = CNSTGenerator(shapeReso=0.1)
gen.add("2 layer")
gen.add(connector)
gen.generate("result_wei/XXX.cnst", "result_wei/XXX.gds", show=True)
