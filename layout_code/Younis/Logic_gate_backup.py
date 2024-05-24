import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnst_gen import CNSTGenerator
from geo import (
    tJunction,
    hJunction,
    RectangleLH,
    roundrect,
    roundedCorners,
    rectSUshape,
    BendWaveguide,
    TextOutline,
    multyTextOutline,
    sBend,
    slash,
    sBendLH,
    rectTaper,
    circlethree,
    Points2Shape,
    Boolean,
    Structure,
)

connector = Structure("beam")
for m in range(1):
    for k in range(1):
        # m = 0
        # k = 0
        r = 0.5  # round corner of beam
        w_cable = 2
        r_cable = 10
        w_support = 10
        L_support = 10
        w_beam = 0.2
        L_beam = 10 + k * 5
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_3 = 20  # gap between electrodes in x direction
        gap_cell_x = 740  # gap between cells in x direction
        gap_actuators_x = 0.25  # gap between actuators
        gap_actuators_y = 0.2  # gap between actuators and beams
        L_actuators = [
            [3 + k * 2.5, 3 + k * 3, 3],
            [3 + k * 2.5, 3 + k * 2.5, 3],
            [3 + k * 2.5, 3, 3 + k * 2.5],
            [3 + k * 2.5, 3, 3 + k * 2.5],
            [7 + k * 2.5, 4 + k * 2.5, 7 + k * 2.5],
            [7 + k * 2.5, 4 + k * 2.5, 7 + k * 2.5],
            [4.75 + k * 2.5, 4.75 + k * 2.5],
        ]
        h_actuators = 3
        L_electrode = 350
        x_beam = (
            -(w_support / 2 - L_electrode + gap_actuators_x + L_actuators[0][0])
            + k * 740
            + m * (3 * 740)
        )
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode

        for i in range(7):
            # beams and supports
            # def beam
            connector.add(
                (
                    RectangleLH(
                        x_beam + w_support / 2,
                        y_beam - i * 850 + (L_support - w_beam) / 2,
                        L_beam,
                        w_beam,
                        0,
                    ),
                )
            )
            if i != 2 and i != 3:
                x1 = x_beam + w_support / 2 + L_beam
                y1 = y_beam + (L_support - w_beam) / 2 - i * 740
                p1 = [(x_beam + 2, y_beam - i * 850)]
                p2 = [(p1[0][0] + 3, p1[0][1] + 4.9)]
                p3 = [(p2[0][0], p2[0][1] + 0.2)]
                p4 = [(p1[0][0], p1[0][1] + L_support)]
                p5 = [(p3[0][0] - w_support, p4[0][1])]
                p6 = [(p5[0][0], p5[0][1] - L_support)]
                connector.add(
                    (
                        # def support
                        Points2Shape(p1 + p2 + p3 + p4 + p5 + p6),
                        circlethree(
                            x1,
                            y1,
                            x1 + w_beam / 2,
                            y1 + w_beam / 2,
                            x1,
                            y1 + w_beam,
                            50,
                        ),
                    ),
                )
            else:
                x1 = x_beam + w_support / 2 + L_beam
                y1 = y_beam + (L_support - w_beam) / 2 - i * 740
                p1_1 = [(x_beam + 2, y_beam - i * 850)]
                p2_1 = [(p1_1[0][0] + 3, p1_1[0][1] + 4.9)]
                p3_1 = [(p2_1[0][0], p2_1[0][1] + 0.2)]
                p4_1 = [(p1_1[0][0], p1_1[0][1] + L_support)]
                p5_1 = [(p3_1[0][0] - w_support, p4_1[0][1])]
                p6_1 = [(p5_1[0][0], p5_1[0][1] - L_support)]
                p1_2 = [(x_beam + w_support / 2 + L_beam + 3, p1_1[0][1])]
                p2_2 = [(p1_2[0][0] - 3, p2_1[0][1])]
                p3_2 = [(p2_2[0][0], p3_1[0][1])]
                p4_2 = [(p1_2[0][0], p4_1[0][1])]
                p5_2 = [(p3_2[0][0] + w_support, p5_1[0][1])]
                p6_2 = [(p5_2[0][0], p6_1[0][1])]
                connector.add(
                    (
                        # def support
                        Points2Shape(p1_1 + p2_1 + p3_1 + p4_1 + p5_1 + p6_1),
                        Points2Shape(p1_2 + p2_2 + p3_2 + p4_2 + p5_2 + p6_2),
                    ),
                )
        # electrodes
        for j in range(7):
            for i in range(2):
                for p in range(2):
                    connector.add(
                        RectangleLH(
                            x_beam
                            + w_support / 2
                            - L_electrode
                            + p * (L_electrode + gap_3)
                            + gap_actuators_x
                            + L_actuators[j][0],
                            y_beam
                            + L_support / 2
                            + gap_2 / 2
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
                        roundrect(
                            x_beam + w_support / 2 + gap_actuators_x_temp,
                            y_beam
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - h_actuators
                            - j * 850,
                            L_actuators_j[i],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                    )
            elif j == 4 or j == 5:
                gap_temp = (
                    L_beam
                    + gap_actuators_y
                    + h_actuators / 2
                    - L_actuators_j[0]
                    - gap_actuators_x
                    - L_actuators_j[1],
                )[0]
                connector.add(
                    (
                        roundrect(
                            x_beam + w_support / 2 + gap_actuators_x,
                            y_beam
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - h_actuators
                            - j * 850,
                            L_actuators_j[0],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                        roundrect(
                            x_beam + w_support / 2 + gap_actuators_x,
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            - j * 850,
                            L_actuators_j[2],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                        rectSUshape(
                            x_beam
                            + w_support / 2
                            + gap_actuators_x
                            + L_actuators_j[0]
                            + gap_temp,
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            + h_actuators / 2
                            - j * 850,
                            L_actuators_j[1],
                            2 * gap_actuators_y + h_actuators + w_beam,
                            -L_actuators_j[1],
                            h_actuators,
                            -90,
                        ),
                    )
                )

        # cables
        for j in range(7):
            # cables of beam
            center_start_x = x_beam
            center_start_y = y_beam + L_support - j * 850
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))
            L_actuators_j = L_actuators[j]
            gap_actuators_x_temp = gap_actuators_x
            for i in range(2):
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
                electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, electrode_y),
                ]
                if i == 0:
                    if j == 2 or j == 3:
                        p2_y = center_start_y - 12
                        p3_x = center_start_x - w_support - 15
                        electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850
                        electrode_x = p3_x
                        point = [
                            (center_start_x, center_start_y),
                            (center_start_x, p2_y),
                            (p3_x, p2_y),
                            (electrode_x, electrode_y),
                        ]
                        connector.add((BendWaveguide(point, r_cable, w_cable),))
                    else:
                        connector.add((BendWaveguide(point, r_cable, w_cable),))

                if i > 0:
                    electrode_y = (
                        y_beam + L_support / 2 - gap_2 / 2 - j * 850 - w_cable / 2
                    )
                    electrode_x = (
                        x_beam
                        + w_support / 2
                        - L_electrode
                        + (L_electrode + gap_3)
                        + gap_actuators_x
                        + L_actuators[j][0],
                    )[0]
                    point = [
                        (center_start_x, center_start_y),
                        (center_start_x, electrode_y),
                        (electrode_x, electrode_y),
                    ]
                    electrode_x = center_start_x + gap_3
                    electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850
                    if j != 2 and j != 3:
                        x2 = center_start_x + (center_start_y - electrode_y)
                        y2 = center_start_y + (electrode_x - center_start_x)
                        connector.add(
                            (
                                sBend(
                                    center_start_x,
                                    center_start_y,
                                    x2,
                                    y2,
                                    w_cable,
                                    -90,
                                ),
                            )
                        )
                    else:
                        connector.add((BendWaveguide(point, r_cable, w_cable),))

            # third cable of 0/1 beam
            if j == 0 or j == 1:
                L_temp = (
                    gap_actuators_x * 3
                    + L_actuators_j[0]
                    + L_actuators_j[1]
                    + L_actuators_j[-1]
                )
                center_start_x = x_beam + w_support / 2 + L_temp
                center_start_y = (
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators / 2
                    - j * 850
                )
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
                electrode_x = center_start_x + gap_3
                point = [
                    (center_start_x, center_start_y),
                    (electrode_x, center_start_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable),))
            # third cable of 2/3 beam
            if j == 2 or j == 3:
                center_start_x = (
                    x_beam
                    + w_support / 2
                    + 2.5 * L_actuators_j[0]
                    + 3 * gap_actuators_x
                )
                center_start_y = (
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators
                    - j * 850
                )
                p2_y = center_start_y - 12
                p3_x = center_start_x + w_support + 30
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
                electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable),))
            if j == 4 or j == 5:
                center_start_x = (
                    x_beam + w_support / 2 + L_actuators_j[0] / 2 + gap_actuators_x
                )
                center_start_y = (
                    y_beam
                    + (L_support + w_beam) / 2
                    + gap_actuators_y
                    + h_actuators
                    - j * 850
                )
                p2_y = center_start_y + 10
                p3_x = center_start_x + gap_3 + 15
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
                electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable),))
        # # Text
        for j in range(7):
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - j * 850 - fontSize / 2
            text = [
                f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} L/t={L_beam/w_beam}",
            ]
            connector.add(
                (
                    multyTextOutline(
                        text, "Times New Roman", fontSize, spacing, x_text, y_text
                    )
                )
            )
        if k == 2 and m == 1:
            text = ["Zhou Lab", "Wei Sun 2024"]
            fontSize = 50
            spacing = 50
            text_x = x_beam
            text_y = (
                y_beam
                + L_support / 2
                - gap_2 / 2
                - j * 850
                - L_electrode
                - spacing * len(text)
            )
            connector.add(
                (
                    multyTextOutline(
                        text, "Times New Roman", fontSize, spacing, text_x, text_y
                    )
                )
            )

gen = CNSTGenerator(shapeReso=0.01)
gen.add("2 layer")
gen.add(connector)
gen.generate("result_wei/Younis.cnst", "result_wei/Younis.gds", show=True)
