import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator
from cnstpy.geo import (
    RectangleLH,
    Roundrect,
    TextOutline,
    RectTaper,
    Points2Shape,
    AlignCustC1,
    Structure,
)

connector = Structure("Tunable")
L_beam_list = [100, 500, 1000]
w_beam_list = [0.05, 0.1, 0.2, 0.1, 0.05, 0.1, 0.2, 0.1]
y_beam = -562.025

for m in range(2):
    for k in range(3):
        r = 0.5  # round corner of beam
        r_cable = 10
        w_support = 20
        L_support = 20
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_actuators_x = 2  # gap between actuators
        gap_actuators_y_list = [
            1,
            1,
            1,
            1,
            3,
            3,
            3,
            3,
        ]  # gap between actuators and beams
        h_actuators = 1
        L_electrode_1 = 250
        L_electrode_2 = 350
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        temp_x = 0 if k == 0 else L_beam_list[k - 1]
        x_beam = m * 4500 + k * 1000 + temp_x + 360
        L_1 = 150  # length of rectaper (rec part)
        L_2 = 50  # length of rectaper
        for j in range(8):
            connector.add("10 layer")
            L_beam = L_beam_list[k]
            w_cable = 50 + (150 / 900) * (L_beam - 100)
            if k > 0 and (j == 3 or j == 7):
                continue
            if k == 0 and (j == 3 or j == 7):
                L_beam = 3000
                w_cable = 200
            gap_3 = L_beam  # gap between electrodes in x direction
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            L_actuator = L_beam - 2 * gap_actuators_x
            w_beam = w_beam_list[j]
            gap_actuators_y = gap_actuators_y_list[j]
            # def beam
            connector.add(
                (
                    (
                        RectangleLH(
                            x_beam + w_support / 2,
                            y_beam - j * 1200 + (L_support - w_beam) / 2,
                            L_beam,
                            w_beam,
                            0,
                        ),
                    )
                )
            )
            # beams and supports
            temp = w_support / 4
            p1_1 = [(x_beam + temp, y_beam - j * 1200)]
            p2_1 = [(p1_1[0][0] + temp, p1_1[0][1] + (w_support - w_beam) / 2)]
            p3_1 = [(p2_1[0][0], p2_1[0][1] + w_beam)]
            p4_1 = [(p1_1[0][0], p1_1[0][1] + L_support)]
            p5_1 = [(p3_1[0][0] - w_support, p4_1[0][1])]
            p6_1 = [(p5_1[0][0], p5_1[0][1] - L_support)]
            p1_2 = [(x_beam + w_support / 2 + L_beam + temp, p1_1[0][1])]
            p2_2 = [(p1_2[0][0] - temp, p2_1[0][1])]
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

            # actuators
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 1200
            )
            # down
            connector.add(
                (
                    # roundcorner of actuator d = 1
                    Roundrect(
                        x_actuator,
                        y_actuator,
                        L_actuator,
                        h_actuators,
                        1,
                        1,
                        0,
                    ),
                    RectTaper(
                        x_actuator + L_actuator / 2,
                        y_actuator - L_2 - L_1 - 10,
                        w_cable,
                        L_1 + 10,
                        L_actuator - 1,
                        L_2,
                        90,
                    ),
                )
            )
            y_actuator += h_actuators + 2 * gap_actuators_y + w_beam
            # up
            connector.add(
                (
                    # roundcorner of actuator d = 1
                    Roundrect(
                        x_actuator,
                        y_actuator,
                        L_actuator,
                        h_actuators,
                        1,
                        1,
                        0,
                    ),
                    RectTaper(
                        x_actuator + L_actuator / 2,
                        y_actuator + L_2 + h_actuators + L_1 + 10,
                        w_cable,
                        L_1 + 10,
                        L_actuator - 1,
                        L_2,
                        -90,
                    ),
                )
            )
            connector.add("11 layer")
            # Text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam / 2 + L_electrode_2 / 2 + 60
            y_text = y_beam - j * 1200 + L_electrode_2 / 2 + 60
            text = f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} G={gap_actuators_y}"

            # L/t={int(L_beam/w_beam)}
            connector.add(
                (TextOutline(text, "Times New Roman", fontSize, x_text, y_text))
            )
            # frame of actuator
            frame_x = x_beam - w_support / 2
            frame_y = y_beam + L_support / 2 - L_2 - j * 1200 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = 1.5 * w_support + L_beam
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 1200
            )
            connector.add(
                (
                    # center
                    RectangleLH(
                        frame_x,
                        frame_y,
                        frame_length + 10,
                        frame_height,
                        0,
                    ),
                    # down
                    RectangleLH(
                        x_beam + w_support / 2 + L_beam / 2 + w_cable / 2 + 10,
                        y_actuator - L_2 - L_1 - 10,
                        L_1 + 10,
                        w_cable + 20,
                        90,
                    ),
                )
            )
            y_actuator += h_actuators + 2 * gap_actuators_y + w_beam
            connector.add(
                (
                    # up
                    RectangleLH(
                        x_beam + w_support / 2 + L_beam / 2 - w_cable / 2 - 10,
                        y_actuator + L_2 + h_actuators + L_1 + 10,
                        L_1 + 10,
                        w_cable + 20,
                        -90,
                    ),
                )
            )
            # pads
            connector.add("20 layer")
            frame_x = x_beam - w_support / 2
            frame_y = y_beam + L_support / 2 - L_2 - j * 1200 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = 1.5 * w_support + L_beam
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 1200
            )
            for i in range(2):
                connector.add(
                    (
                        # left
                        RectangleLH(
                            x_beam - w_support / 2 - L_electrode_2,
                            y_beam + L_support / 2 - j * 1200 - L_electrode_2 / 2,
                            L_electrode_2,
                            L_electrode_2,
                            0,
                        ),
                        # right
                        RectangleLH(
                            x_beam + w_support / 2 * 3 + L_beam,
                            y_beam + L_support / 2 - j * 1200 - L_electrode_2 / 2,
                            L_electrode_2,
                            L_electrode_2,
                            0,
                        ),
                        # top
                        RectangleLH(
                            x_beam + w_support / 2 + L_beam / 2 - L_electrode_2 / 2,
                            y_beam
                            - j * 1200
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            + L_1
                            + L_2
                            + h_actuators,
                            L_electrode_2,
                            L_electrode_2,
                            0,
                        ),
                        # bottom
                        RectangleLH(
                            x_beam + w_support / 2 + L_beam / 2 - L_electrode_2 / 2,
                            y_beam
                            - j * 1200
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - L_1
                            - L_2
                            - h_actuators
                            - L_electrode_2,
                            L_electrode_2,
                            L_electrode_2,
                            0,
                        ),
                    )
                )
            # frame of actuator in layer 20
            connector.add(
                (
                    RectangleLH(
                        frame_x,
                        frame_y + 5,
                        frame_length + 10,
                        frame_height - 10,
                        0,
                    ),
                    # down
                    RectangleLH(
                        x_beam + w_support / 2 + L_beam / 2 + w_cable / 2 + 5,
                        y_actuator - L_2 - L_1 - 10,
                        L_1 + 10,
                        w_cable + 10,
                        90,
                    ),
                )
            )
            y_actuator += h_actuators + 2 * gap_actuators_y + w_beam
            connector.add(
                (
                    # up
                    RectangleLH(
                        x_beam + w_support / 2 + L_beam / 2 - w_cable / 2 - 5,
                        y_actuator + L_2 + h_actuators + L_1 + 10,
                        L_1 + 10,
                        w_cable + 10,
                        -90,
                    ),
                )
            )
            # frame of text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam / 2 + L_electrode_2 / 2 + 35
            y_text = y_beam - j * 1200 + L_electrode_2 / 2 + 55
            connector.add((RectangleLH(x_text - 2.5, y_text - 2.5, 360, 35, 0),))

        # if k == 2 and m == 1:
        #     text = ["Zhou Lab", "Wei Sun 2024"]
        #     fontSize = 50
        #     spacing = 50
        #     text_x = x_beam
        #     text_y = (
        #         y_beam
        #         + L_support / 2
        #         - gap_2 / 2
        #         - j * 1200
        #         - L_electrode
        #         - spacing * len(text)
        #     )
        #     connector.add(
        #         (
        #             M(
        #                 text, "Times New Roman", fontSize, spacing, text_x, text_y
        #             )
        #         )
        #     )

# alignment marks in layer 11
connector.add("11 layer")
connector.add(AlignCustC1(-200, -5000, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(8940, -5000, 100, 2, 100, 0, 120, 120, 0))

# connector.add("21 layer")
connector.add("21 layer")
connector.add(
    RectangleLH(
        -10,
        -9506.075 - 10,
        8740 + 20,
        9506.075 + 20,
        0,
    )
)
# alignment marks in layer 21
connector.add(AlignCustC1(-200, -5000, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(8940, -5000, 100, 2, 100, 0, 120, 120, 0))


gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.generate(
    "result_wei/tunable_device/thermal/Tunable_thermal.cnst",
    "result_wei/tunable_device/thermal/Tunable_thermal.gds",
    show=True,
)
