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

connector = Structure("Tunable")
for m in range(1):
    for k in range(1):
        r = 0.5  # round corner of beam
        w_cable = 2
        r_cable = 10
        w_support = 10
        L_support = 10
        w_beam = 0.2
        L_beam = 100 + k * 5
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_3 = 20  # gap between electrodes in x direction
        gap_cell_x = 740  # gap between cells in x direction
        gap_actuators_x = 5  # gap between actuators
        gap_actuators_y = 0.2  # gap between actuators and beams
        L_actuator = 20
        h_actuators = 3
        L_electrode = 350
        cable_in = 10  # length enter the electrode
        x_beam = (
            -(w_support / 2 - L_electrode + gap_actuators_x + L_actuator)
            + k * 740
            + m * (3 * 740)
        )
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode

        for i in range(7):
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
            # beams and supports
            x1 = x_beam + w_support / 2 + L_beam
            y1 = y_beam + (L_support - w_beam) / 2 - i * 740
            p1_1 = [(x_beam + 2, y_beam - i * 850)]
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
                            + L_actuator,
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
            connector.add(
                (
                    roundrect(
                        x_beam + (w_support + L_beam - L_actuator) / 2,
                        y_beam
                        + (L_support - w_beam) / 2
                        - gap_actuators_y
                        - h_actuators
                        - j * 850,
                        L_actuator,
                        h_actuators,
                        1,
                        1,
                        0,
                    ),
                    roundrect(
                        x_beam + (w_support + L_beam - L_actuator) / 2,
                        y_beam + (L_support + w_beam) / 2 + gap_actuators_y - j * 850,
                        L_actuator,
                        h_actuators,
                        1,
                        1,
                        0,
                    ),
                )
            )

        # cables
        for j in range(7):
            # cables of beam
            # cable of left support
            center_start_x = x_beam
            center_start_y = y_beam + L_support - j * 850
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850 + cable_in
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))
            # cable of right support
            center_start_x = x_beam + w_support + L_beam
            center_start_y = y_beam - j * 850
            p2_y = center_start_y - 10
            p3_x = (
                x_beam
                + w_support / 2
                + L_beam
                + gap_3
                + gap_actuators_x
                + L_actuator / 2
                + 10
            )
            electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850 - cable_in
            electrode_x = p3_x
            point = [
                (center_start_x, center_start_y),
                (center_start_x, p2_y),
                (p3_x, p2_y),
                (electrode_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))
            # cables of beam
            # cable of lower electrode
            center_start_x = x_beam + w_support / 2 + gap_actuators_x + L_actuator / 2
            center_start_y = (
                y_beam + (L_support - w_support) / 2 - gap_actuators_y - j * 850
            )

            # cable of upper electrode

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
gen.generate(
    "result_wei/tunable_device/Tunable.cnst",
    "result_wei/tunable_device/Tunable.gds",
    show=True,
)
