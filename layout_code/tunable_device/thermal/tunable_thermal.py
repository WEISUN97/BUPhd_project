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
    Instance,
)

connector = Structure("Tunable")
L_beam_list = [100, 500, 1000]
w_beam_list = [0.05, 0.1, 0.2, 0.1, 0.05, 0.1, 0.2, 0.1]
gap_actuators_y_list = [1, 3]  # gap between actuators and beams
for m in range(2):
    gap_actuators_y = gap_actuators_y_list[m]
    for k in range(3):
        y_beam = 1200
        r = 0.5  # round corner of beam
        r_cable = 10
        w_support = 20
        L_support = 20
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_actuators_x = 2  # gap between actuators
        h_actuators = 1
        L_electrode = 350
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        temp_x = 0 if k == 0 else L_beam_list[k - 1]
        x_beam = m * 6500 + k * 1000 + temp_x + 0
        L_1 = 150  # length of rectaper (rec part)
        L_2 = 50  # length of rectaper
        for j in range(8):
            y_beam -= 1200 if j != 4 else 3200
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
            # def beam
            connector.add(
                (
                    (
                        RectangleLH(
                            x_beam + w_support / 2,
                            y_beam + (L_support - w_beam) / 2,
                            L_beam,
                            w_beam,
                            0,
                        ),
                    )
                )
            )
            # supports
            temp = w_support / 4
            p1_1 = [(x_beam + temp, y_beam)]
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
            support_right = p5_2[0][0]
            connector.add(
                (
                    # def support
                    Points2Shape(p1_1 + p2_1 + p3_1 + p4_1 + p5_1 + p6_1),
                    Points2Shape(p1_2 + p2_2 + p3_2 + p4_2 + p5_2 + p6_2),
                ),
            )

            # actuators
            y_actuator = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
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
                        h_actuators,
                        h_actuators,
                        0,
                    ),
                    RectTaper(
                        x_actuator + L_actuator / 2,
                        y_actuator - L_2 - L_1,
                        w_cable,
                        L_1,
                        L_actuator - h_actuators,
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
                        h_actuators,
                        h_actuators,
                        0,
                    ),
                    RectTaper(
                        x_actuator + L_actuator / 2,
                        y_actuator + L_2 + h_actuators + L_1,
                        w_cable,
                        L_1,
                        L_actuator - h_actuators,
                        L_2,
                        -90,
                    ),
                )
            )
            connector.add("11 layer")
            # Text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam / 2 + L_electrode / 2 + 60
            y_text = y_beam + L_electrode / 2 + 60
            text = f"  {j+1}.{k+1} L={L_beam} t={w_beam} G={gap_actuators_y}"

            # L/t={int(L_beam/w_beam)}
            connector.add(
                (TextOutline(text, "Times New Roman", fontSize, x_text, y_text))
            )

            # frame of actuator in layer 11
            frame_x = x_beam - w_support / 2
            frame_y = y_beam + L_support / 2 - L_2 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = 1.5 * w_support + L_beam
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
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
                        y_actuator - L_2 - L_1,
                        L_1,
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
                        y_actuator + L_2 + h_actuators + L_1,
                        L_1,
                        w_cable + 20,
                        -90,
                    ),
                )
            )
            # pads
            connector.add("20 layer")
            # "left, right, top, bottom"
            x_start = [
                x_beam - w_support / 2 - L_electrode,
                x_beam + w_support / 2 * 3 + L_beam,
                x_beam + w_support / 2 + L_beam / 2 - L_electrode / 2,
                x_beam + w_support / 2 + L_beam / 2 - L_electrode / 2,
            ]
            y_start = [
                y_beam + L_support / 2 - L_electrode / 2,
                y_beam + L_support / 2 - L_electrode / 2,
                y_beam
                + (L_support + w_beam) / 2
                + gap_actuators_y
                + L_1
                + L_2
                + h_actuators,
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - L_1
                - L_2
                - h_actuators
                - L_electrode,
            ]
            if k == 0:
                temp_text = [x_start, y_start]
            for i in range(4):
                connector.add(
                    RectangleLH(
                        x_start[i],
                        y_start[i],
                        L_electrode,
                        L_electrode,
                        0,
                    ),
                )
            # frame of actuator in layer 20
            frame_x = x_beam - w_support / 2
            frame_y = y_beam + L_support / 2 - L_2 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = 1.5 * w_support + L_beam
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
            )
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
            x_text = x_beam + w_support / 2 + L_beam / 2 + L_electrode / 2 + 35
            y_text = y_beam + L_electrode / 2 + 55
            connector.add((RectangleLH(x_text - 2.5, y_text - 2.5, 350, 35, 0),))


# signature in layer 11
# connector.add("11 layer")
# text = "Zhou Lab 2024\nWei Sun"
# fontSize = 50
# spacing = 50
# text_x = temp_text[0][3] + L_electrode + 1500
# text_y = temp_text[1][3] + 100
# connector.add((TextOutline(text, "Times New Roman", fontSize, text_x, text_y, spacing)))
# frame of text
# connector.add("20 layer")
# connector.add(
#     RectangleLH(
#         text_x - 20,
#         text_y - 2 * fontSize,
#         500,
#         2 * fontSize + 20 + spacing,
#         0,
#     )
# )


connector.add("21 layer")
for i in range(2):
    for j in range(2):
        # connector.add(
        #     RectangleLH(
        #         -360 - 10,
        #         -10944.050 - 10,
        #         10380 + 360 + 20,
        #         562.025 + 10944.050 + 20,
        #         0,
        #     )
        # )
        connector.add(
            RectangleLH(
                -370 + 6500 * i,
                -4152.05 - 6800 * j,
                4260,
                4724.02,
                0,
            )
        )


# connector
# connector = Structure("connector")
# for i in range(3):
#     connector.add(Instance(connector, 10000 * i, 0, "N", 1, 0))

# alignment marks in layer 11
connector.add("11 layer")
connector.add(AlignCustC1(-510, -3600, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(10510, -3600, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(-510, -8600, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(10510, -8600, 100, 2, 100, 0, 120, 120, 0))
# alignment marks in layer 21
connector.add("21 layer")
connector.add(AlignCustC1(-510, -3600, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(10510, -3600, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(-510, -8600, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(10510, -8600, 100, 2, 100, 0, 120, 120, 0))


gen = CNSTGenerator(shapeReso=0.01)
# gen.add(connector)
gen.add(connector)
gen.generate(
    "result_wei/tunable_device/thermal/Tunable_thermal.cnst",
    "result_wei/tunable_device/thermal/Tunable_thermal.gds",
    show=True,
)
