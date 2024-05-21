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

connector = Structure("beam")
for m in range(2):
    for k in range(4):
        r = 0.2  # round corner
        w_support = 2
        L_support = 2
        w_beam = 0.2
        L_beam = 10 + k * 5
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 30  # gap between electrodes in y direction
        gap_cell_x = 320  # gap between cells in x direction
        gap_actuators_x = 0.5  # gap between actuators
        gap_actuators_y = 0.2  # gap between actuators and beams
        L_actuators = [
            [3.5 + k * 2.5, 3.5 + k * 2.5, 1],
            [3.5 + k * 2.5, 3.5 + k * 2.5, 1],
            [3.5 + k * 2.5, 1, 3.5 + k * 2.5],
            [3.5 + k * 2.5, 1, 3.5 + k * 2.5],
            [5 + k * 5, 2, 5 + k * 5],
            [5 + k * 5, 2, 5 + k * 5],
            [6.5 + k * 5, 2],
        ]
        h_actuators = 0.2
        L_electrode = 250
        x_beam = (
            2 * k * gap_cell_x
            + gap_1
            + L_electrode
            + w_support / 2
            + 8 * m * gap_cell_x
        )
        y_beam = -L_support

        for i in range(7):
            # beams and supports
            if i != 2 and i != 3:
                connector.add(
                    (
                        tJunction(
                            x_beam,
                            y_beam - i * 850,
                            w_support,
                            w_beam,
                            L_support,
                            L_beam,
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
                            x_beam,
                            y_beam - i * 850,
                            w_support,
                            w_beam,
                            L_support,
                            L_beam,
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
                        y_beam + (L_support - w_beam) / 2 - r,
                        r,
                        90,
                    ),
                ),
            )
        # electrodes
        for j in range(7):
            for i in range(3):
                connector.add(
                    RectangleLH(
                        x_beam - w_support / 2 - gap_1 - L_electrode,
                        y_beam
                        + L_support
                        - L_electrode
                        - i * (gap_2 + L_electrode)
                        - j * 850,
                        L_electrode,
                        L_electrode,
                        0,
                    ),
                )
        if m == 1 and k == 3:
            for j in range(7):
                for i in range(3):
                    connector.add(
                        RectangleLH(
                            x_beam
                            - w_support / 2
                            - gap_1
                            - L_electrode
                            + gap_cell_x * 2,
                            y_beam
                            + L_support
                            - L_electrode
                            - i * (gap_2 + L_electrode)
                            - j * 850,
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
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            - j * 850,
                            L_actuators_j[2],
                            h_actuators,
                            0,
                        ),
                        rectSUshape(
                            x_beam
                            + w_support / 2
                            + L_beam
                            + gap_actuators_y
                            + h_actuators / 2
                            - L_actuators_j[1],
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            + h_actuators / 2
                            - j * 850,
                            2,
                            2 * gap_actuators_y + h_actuators + w_beam,
                            -2,
                            h_actuators,
                            -90,
                        ),
                    )
                )

        # cables
        for j in range(7):
            L_actuators_j = L_actuators[j]
            gap_actuators_x_temp = gap_actuators_x
            for i in range(len(L_actuators_j)):
                if (j == 4 or j == 5) and i == 2:
                    if j == 5:
                        continue
                    center_start_x = (
                        x_beam + w_support / 2 + gap_actuators_x + L_actuators_j[i] / 2
                    )
                    center_start_y = (
                        y_beam
                        + (L_support + w_beam) / 2
                        + gap_actuators_y
                        + h_actuators
                        - j * 850
                    )
                    up_distance = 15
                    electrode_y = y_beam + L_support - j * 850
                    electrode_x = x_beam - w_support / 2 - gap_1 - L_electrode / 2
                    point = [
                        (center_start_x, center_start_y),
                        (center_start_x, center_start_y + up_distance),
                        (electrode_x, center_start_y + up_distance),
                        (electrode_x, electrode_y),
                    ]
                    connector.add((BendWaveguide(point, r=10, w=1),))
                    continue
                if i > 0:
                    gap_actuators_x_temp += +L_actuators_j[i - 1] + gap_actuators_x
                center_start_x = (
                    x_beam + w_support / 2 + gap_actuators_x_temp + L_actuators_j[i] / 2
                )
                center_start_y = (
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators
                    - j * 850
                )
                electrode_y = (
                    y_beam
                    + L_support
                    - i * (gap_2 + L_electrode)
                    - j * 850
                    - L_electrode / 2
                )
                electrode_x = x_beam - w_support / 2 - gap_1
                if j == 4 or j == 5:
                    electrode_y -= L_electrode + gap_2
                    if i == 1:
                        center_start_x = (
                            x_beam
                            + w_support / 2
                            + L_beam
                            + gap_actuators_y
                            + h_actuators / 2
                            - L_actuators_j[1] / 2
                        )
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, electrode_y),
                    (electrode_x, electrode_y),
                ]

                connector.add((BendWaveguide(point, r=10, w=1),))
            if j == 1 or j == 3 or j == 6:
                center_start_x = x_beam
                center_start_y = y_beam + (L_support + w_beam) / 2 - j * 850
                temp_y = center_start_y + 15
                temp_x = x_beam + gap_cell_x - L_electrode - gap_1 - 15
                electrode_x = (
                    x_beam - w_support / 2 + 2 * gap_cell_x - L_electrode - gap_1
                )
                electrode_y = y_beam + L_support - j * 850 - L_electrode / 2
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, temp_y),
                    (temp_x, temp_y),
                    (temp_x, electrode_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r=10, w=1),))
            if j == 5:
                L_actuators_j = L_actuators[j]
                # top actuators
                center_start_x = (
                    x_beam + w_support / 2 + gap_actuators_x + L_actuators_j[i] / 2
                )
                center_start_y = (
                    y_beam
                    + (L_support + w_beam) / 2
                    + gap_actuators_y
                    + h_actuators
                    - j * 850
                )
                temp_y = center_start_y + 15
                temp_x = x_beam + gap_cell_x - L_electrode - gap_1 - 15
                electrode_x = (
                    x_beam - w_support / 2 + 2 * gap_cell_x - L_electrode - gap_1
                )
                electrode_y = y_beam + L_support - j * 850 - L_electrode / 2
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, temp_y),
                    (temp_x, temp_y),
                    (temp_x, electrode_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r=10, w=1),))
                # cable of beam
                center_start_x = x_beam
                center_start_y = y_beam + (L_support + w_beam) / 2 - j * 850
                up_distance = 15
                electrode_y = y_beam + L_support - j * 850
                electrode_x = x_beam - w_support / 2 - gap_1 - L_electrode / 2
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, center_start_y + up_distance),
                    (electrode_x, center_start_y + up_distance),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r=10, w=1),))

        # # Text
        for j in range(7):
            fontSize = 15
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 50
            y_text = y_beam - j * 850 - fontSize
            text = [
                f"No.{k+1}.{j+1}.{m+1}",
                f"L={L_beam}",
                f"t={w_beam}",
                f"L/t={L_beam/w_beam}",
            ]
            connector.add(
                (
                    multyTextOutline(
                        text, "Times New Roman", fontSize, spacing, x_text, y_text
                    )
                )
            )
gen = CNSTGenerator(shapeReso=0.1)
gen.add("2 layer")
gen.add(connector)
gen.generate("result_wei/XXX.cnst", "result_wei/XXX.gds", show=True)
