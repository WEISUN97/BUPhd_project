import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator
from cnstpy.geo import (
    RectangleLH,
    Roundrect,
    RectSUshape,
    BendWaveguide,
    TextOutline,
    Circle,
    Points2Shape,
    Structure,
    Instance,
    AlignCustC1,
)


# cell logicgate
connector = Structure("logicgate")
# E-beam structure part in layer 10
gap_actuators_y_list = [2, 3]
for m in range(2):
    # gap between actuators and beams
    gap_actuators_y = gap_actuators_y_list[m]
    for k in range(3):
        # m = 0
        # k = 0
        r = 0.5  # round corner of beam
        w_cable = 5
        r_cable = 5
        w_support = 10
        L_support = 10
        w_beam = 0.2 + k * 0.2
        # L_beam = 15
        L_beam = 30
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_3 = 20  # gap between electrodes in x direction
        gap_cell_x = 740  # gap between cells in x direction
        gap_actuators_x = 2  # gap between actuators
        L_actuators = [
            [8, 8, 8],
            [8, 8, 8],
            [22 / 3, 22 / 3, 22 / 3],
            [22 / 3, 22 / 3, 22 / 3],
            [17, 11, 17],
            [17, 11, 17],
            [13, 13],
        ]
        h_actuators = 6
        L_electrode = 350
        cable_in = 10  # length enter the electrode
        x_beam = (
            -(w_support / 2 - L_electrode + gap_actuators_x + L_actuators[0][0])
            + k * 740
            + m * (3 * 740)
        )
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode + 850

        for j in range(7):
            y_beam -= 850
            connector.add("10 layer")
            # beams and supports
            gap_actuators_y = gap_actuators_y_list[m]

            if j != 2 and j != 3:
                p1 = [(x_beam + 2, y_beam)]
                p2 = [(p1[0][0] + 3, p1[0][1] + (w_support - w_beam) / 2)]
                p3 = [(p2[0][0], p2[0][1] + w_beam)]
                p4 = [(p1[0][0], p1[0][1] + L_support)]
                p5 = [(p3[0][0] - w_support, p4[0][1])]
                p6 = [(p5[0][0], p5[0][1] - L_support)]
                connector.add(
                    (
                        # def support
                        Points2Shape(p1 + p2 + p3 + p4 + p5 + p6),
                        # def round corner of beam
                        Circle(
                            x_beam + w_support / 2 + L_beam - w_beam / 2,
                            y_beam + L_support / 2,
                            w_beam / 2,
                        ),
                        # def beam
                        RectangleLH(
                            x_beam + w_support / 2,
                            y_beam + (L_support - w_beam) / 2,
                            L_beam - w_beam / 2,
                            w_beam,
                            0,
                        ),
                    ),
                )
            else:
                p1_1 = [(x_beam + 2, y_beam)]
                p2_1 = [(p1_1[0][0] + 3, p1_1[0][1] + (w_support - w_beam) / 2)]
                p3_1 = [(p2_1[0][0], p2_1[0][1] + w_beam)]
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
                        # def beam
                        RectangleLH(
                            x_beam + w_support / 2,
                            y_beam + (L_support - w_beam) / 2,
                            L_beam,
                            w_beam,
                            0,
                        ),
                    ),
                )

            # actuators
            L_actuators_j = L_actuators[j]
            if j < 4 or j == 6:
                gap_actuators_x_temp = gap_actuators_x
                for i in range(len(L_actuators_j)):
                    if i > 0:
                        gap_actuators_x_temp += L_actuators_j[i - 1] + gap_actuators_x
                    connector.add(
                        Roundrect(
                            x_beam + w_support / 2 + gap_actuators_x_temp,
                            y_beam
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - h_actuators,
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
                        Roundrect(
                            x_beam + w_support / 2 + gap_actuators_x,
                            y_beam
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - h_actuators,
                            L_actuators_j[0],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                        Roundrect(
                            x_beam + w_support / 2 + gap_actuators_x,
                            y_beam + (L_support + w_beam) / 2 + gap_actuators_y,
                            L_actuators_j[2],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                        RectSUshape(
                            x_beam
                            + w_support / 2
                            + gap_actuators_x
                            + L_actuators_j[0]
                            + gap_temp,
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            + h_actuators / 2,
                            L_actuators_j[1],
                            2 * gap_actuators_y + h_actuators + w_beam,
                            -L_actuators_j[1],
                            h_actuators,
                            -90,
                        ),
                    )
                )

            # cables
            # cables of beam
            center_start_x = p5[0][0] + w_cable / 2
            center_start_y = y_beam + L_support
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 + cable_in
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            L_actuators_j = L_actuators[j]
            gap_actuators_x_temp = gap_actuators_x
            for i in range(2):
                if i > 0:
                    gap_actuators_x_temp += +L_actuators_j[i - 1] + gap_actuators_x
                center_start_x = (
                    x_beam + w_support / 2 + gap_actuators_x_temp + L_actuators_j[i] / 2
                )
                center_start_y = (
                    y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
                )
                if i == 0:
                    p2_y = center_start_y - 15
                    p3_x = center_start_x - w_support - 15
                    electrode_y = y_beam + L_support / 2 - gap_2 / 2 - cable_in
                    electrode_x = p3_x

                if i > 0:
                    p2_y = center_start_y - 15
                    p3_x = (
                        x_beam
                        + w_support / 2
                        - L_electrode
                        + (L_electrode + gap_3)
                        + gap_actuators_x
                        + L_actuators[j][0]
                        + 10
                    )
                    electrode_y = y_beam + L_support / 2 - gap_2 / 2 - cable_in
                    electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable, 30),))

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
                )
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 + cable_in
                electrode_x = center_start_x + gap_3
                point = [
                    (center_start_x, center_start_y),
                    (electrode_x, center_start_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # third cable of 2/3 beam
            if j == 2 or j == 3:
                center_start_x = (
                    x_beam
                    + w_support / 2
                    + 1.5 * L_actuators_j[0]
                    + L_actuators_j[1]
                    + 3 * gap_actuators_x
                )
                center_start_y = (
                    y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
                )
                p2_y = center_start_y - 7.5
                p3_x = center_start_x + w_support + 15
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 + cable_in
                electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            if j == 4 or j == 5:
                center_start_x = (
                    x_beam + w_support / 2 + L_actuators_j[0] / 2 + gap_actuators_x
                )
                center_start_y = (
                    y_beam + (L_support + w_beam) / 2 + gap_actuators_y + h_actuators
                )
                p2_y = center_start_y + 10
                p3_x = center_start_x + gap_3 + 15
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 + cable_in
                electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable, 30),))

            # E-beam frame and text in layer 11
            connector.add("11 layer")
            L_actuators_j = L_actuators[j]
            center_start_x = (
                x_beam + w_support / 2 + gap_actuators_x + L_actuators_j[i] / 2
            )
            frame_x = center_start_x - w_support - 15 - w_cable / 2 - 10
            frame_height = gap_2 + 2 * cable_in
            frame_length = (
                w_cable
                + 20
                + (
                    -L_electrode
                    + (L_electrode + gap_3)
                    + gap_actuators_x
                    + L_actuators[j][0]
                    + 20
                )
                - (gap_actuators_x + L_actuators_j[i] / 2 - w_support - 15)
            )
            connector.add(
                RectangleLH(
                    frame_x,
                    y_beam + L_support / 2 - gap_2 / 2 - cable_in,
                    frame_length,
                    frame_height,
                    0,
                ),
            )
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - fontSize / 2
            text = f"{j+1}.{k+1}.{m+1} L{L_beam} t{w_beam:.2f} G{gap_actuators_y:.2f}"
            connector.add(
                (
                    TextOutline(
                        text, "Times New Roman", fontSize, x_text, y_text, spacing
                    )
                )
            )

            # cell electrode
            # electrode in layer 20
            connector.add("20 layer")
            # pads
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
                            - i * (gap_2 + L_electrode + 5),
                            L_electrode,
                            L_electrode,
                            0,
                        ),
                    )
            # mid frame
            L_actuators_j = L_actuators[j]
            center_start_x = (
                x_beam + w_support / 2 + gap_actuators_x + L_actuators_j[i] / 2
            )
            frame_x = center_start_x - w_support - 15 - w_cable / 2 - 10
            frame_height = gap_2 + 2 * cable_in + 5
            frame_length = (
                w_cable
                + 30
                + (
                    -L_electrode
                    + (L_electrode + gap_3)
                    + gap_actuators_x
                    + L_actuators[j][0]
                    + 10
                )
                - (gap_actuators_x + L_actuators_j[i] / 2 - w_support - 15)
            )
            connector.add(
                RectangleLH(
                    frame_x + 5,
                    y_beam + L_support / 2 - gap_2 / 2 - 5,
                    frame_length - 10,
                    frame_height - 2 * cable_in,
                    0,
                ),
            )
            # text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - fontSize / 2
            connector.add((RectangleLH(x_text - 5, y_text - 5, 240, 30, 0),))
# electrode frame in layer 21
connector.add("21 layer")
connector.add(
    RectangleLH(
        -10,
        -5865,
        4445,
        5875,
        0,
    )
)


# Array
x_gap = 4800
y_gap = -6200
array = Structure("Array")
for i in range(3):
    for j in range(2):
        array.add(Instance(connector, x_gap * i, y_gap * j, "N", 1, 0))
        # marker
        array.add("11 layer")
        array.add(AlignCustC1(-200, -2925 + y_gap * j, 100, 2, 100, 0, 120, 120, 0))
        print(AlignCustC1(-200, -2925 + y_gap * j, 100, 2, 100, 0, 120, 120, 0))
        array.add(
            AlignCustC1(
                4620 + 2 * x_gap, -2925 + y_gap * j, 100, 2, 100, 0, 120, 120, 0
            )
        )
        print(
            AlignCustC1(
                4620 + 2 * x_gap, -2925 + y_gap * j, 100, 2, 100, 0, 120, 120, 0
            )
        )

        array.add("21 layer")
        array.add(AlignCustC1(-200, -2925 + y_gap * j, 100, 2, 100, 0, 120, 120, 0))
        array.add(
            AlignCustC1(
                4620 + 2 * x_gap, -2925 + y_gap * j, 100, 2, 100, 0, 120, 120, 0
            )
        )

# Signature
array.add("11 layer")
text = "Zhou Lab\n 2024 Wei Sun"
fontSize = 50
spacing = 50
text_x = 13700
text_y = -12100
array.add((TextOutline(text, "Times New Roman", fontSize, text_x, text_y)))


gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.add(array)
gen.generate(
    "result_wei/logicgate/logicgate.cnst",
    "result_wei/logicgate/logicgate.gds",
    show=True,
)
