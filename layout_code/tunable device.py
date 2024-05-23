import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnst_gen import CNSTGenerator
from geo import (
    tJunction,
    hJunction,
    RectangleLH,
    roundedCorners,
    rectSUshape,
    BendWaveguide,
    TextOutline,
    multyTextOutline,
    Boolean,
    Structure,
)

connector = Structure("Tunable")

r = 1
x_beam = 0
y_beam = 0
w_support = 5
L_support = 5
w_beam = 0.03  # thickness of beam
L_beam = 15
gap_1 = 10  # gap between electrodes and beams
gap_2 = 30  # gap between electrodes in y direction
gap_cell_x = 320  # gap between cells in x direction
L_electrode = 400

# Thermal
# beam
for i in range(4):
    L_beam_t = L_beam + i * 50
    connector.add(
        (
            hJunction(x_beam, y_beam - i * 860, w_support, w_beam, L_support, L_beam_t),
            roundedCorners(
                x_beam + w_support / 2 + r,
                y_beam + (L_support + w_beam) / 2 + r - i * 860,
                r,
                180,
            ),
            roundedCorners(
                x_beam + w_support / 2 + r,
                y_beam + (L_support - w_beam) / 2 - r - i * 860,
                r,
                90,
            ),
            roundedCorners(
                x_beam + w_support / 2 + L_beam_t - r,
                y_beam + (L_support + w_beam) / 2 + r - i * 860,
                r,
                270,
            ),
            roundedCorners(
                x_beam + w_support / 2 + L_beam_t - r,
                y_beam + (L_support - w_beam) / 2 - r - i * 860,
                r,
                0,
            ),
        )
    )

# elctrode
for j in range(4):
    for i in range(2):
        connector.add(
            RectangleLH(
                x_beam - w_support / 2 - gap_1 - L_electrode,
                y_beam + L_support - L_electrode - i * (gap_2 + L_electrode) - j * 860,
                L_electrode,
                L_electrode,
                0,
            )
        ),


gen = CNSTGenerator(shapeReso=0.1)
gen.add("2 layer")
gen.add(connector)
gen.generate("result_wei/Tunable.cnst", "result_wei/Tunable.gds", show=True)
