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
    BendWaveguide,
    Structure,
)

connector = Structure("Tunable")
for m in range(1):
    L_beam_list = [100, 500, 1000]
    for k in range(3):
        r = 0.5  # round corner of beam
        w_cable = 10
        r_cable = 10
        w_support = 20
        L_support = 20
        w_beam_list = [0.05, 0.1, 0.2, 0.1, 0.05, 0.1, 0.2, 0.1]
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_actuators_x = 2  # gap between actuators
        gap_actuators_y = 1  # gap between actuators and beams
        h_actuators = 1
        L_electrode = 350
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        # x_beam = (
        #     -(w_support / 2 - L_electrode + gap_actuators_x + L_actuator)
        #     + k * 1000
        #     + m * 3000
        # )
        x_beam = m * 3000 + k * 1500
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode
        L_1 = 0  # length of rectaper
        L_2 = 10  # length of rectaper
        for j in range(8):
            L_beam = L_beam_list[k]
            if k > 0 and j > 0:
                continue
            if k == 0 and (j == 3 or j == 7):
                L_beam = 3000
            gap_3 = L_beam  # gap between electrodes in x direction
            L_actuator = L_beam - 2 * gap_actuators_x
            w_beam = w_beam_list[j]
            # def beam
            connector.add(
                (
                    RectangleLH(
                        x_beam + w_support / 2,
                        y_beam - j * 800 + (L_support - w_beam) / 2,
                        L_beam,
                        w_beam,
                        0,
                    ),
                )
            )
            # beams and supports
            temp = w_support / 4
            p1_1 = [(x_beam + temp, y_beam - j * 800)]
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
            # electrodes
            for i in range(2):
                for p in range(2):
                    connector.add(
                        RectangleLH(
                            x_beam
                            - L_electrode
                            + p * (L_electrode + gap_3 - cable_offset + w_support / 2)
                            + cable_offset,
                            y_beam
                            + L_support / 2
                            + gap_2 / 2
                            - i * (gap_2 + L_electrode)
                            - j * 800,
                            L_electrode,
                            L_electrode,
                            0,
                        ),
                    )
            # actuators
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 800
            )
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
                        y_actuator - L_2,
                        w_cable,
                        L_1,
                        L_actuator - 1,
                        L_2,
                        90,
                    ),
                )
            )
            y_actuator += h_actuators + 2 * gap_actuators_y + w_beam
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
                        y_actuator + L_2 + h_actuators,
                        w_cable,
                        L_1,
                        L_actuator - 1,
                        L_2,
                        -90,
                    ),
                )
            )
            # cables
            # cables of beam
            # cable of left support
            center_start_x = x_beam
            center_start_y = y_beam + L_support - j * 800
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 800 + cable_in
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of right support
            center_start_x = x_beam + w_support + L_beam
            center_start_y = y_beam - j * 800
            electrode_y = (
                y_beam + L_support / 2 - gap_2 / 2 - j * 800 - w_cable / 2 - cable_in
            )
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of actuator below
            center_start_x = x_beam + w_support / 2 + gap_actuators_x + L_actuator / 2
            center_start_y = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - L_2
                - j * 800
            )
            electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 800 - cable_in
            electrode_x = x_beam - w_support
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
                (electrode_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of actuator up
            center_start_y += 2 * (L_2 + h_actuators + gap_actuators_y) + w_beam
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 800 + cable_in
            electrode_x = x_beam + 2 * w_support + L_beam
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
                (electrode_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))

            # Text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - j * 800 - fontSize / 2
            text = (
                f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} L/t={int(L_beam/w_beam)}"
            )
            connector.add(
                (
                    TextOutline(
                        text, "Times New Roman", fontSize, x_text, y_text, spacing
                    )
                )
            )
        # if k == 2 and m == 1:
        #     text = ["Zhou Lab", "Wei Sun 2024"]
        #     fontSize = 50
        #     spacing = 50
        #     text_x = x_beam
        #     text_y = (
        #         y_beam
        #         + L_support / 2
        #         - gap_2 / 2
        #         - j * 800
        #         - L_electrode
        #         - spacing * len(text)
        #     )
        #     connector.add(
        #         (
        #             multyTextOutline(
        #                 text, "Times New Roman", fontSize, spacing, text_x, text_y
        #             )
        #         )
        #     )
# Alignment Marks
connector.add(AlignCustC1(-350, -3150, 100, 2, 100, 0, 120, 120, 0))
connector.add(AlignCustC1(7000, -3150, 100, 2, 100, 0, 120, 120, 0))

gen = CNSTGenerator(shapeReso=0.01)
gen.add("2 layer")
gen.add(connector)
gen.generate(
    "result_wei/tunable_device/thermal/Tunable.cnst",
    "result_wei/tunable_device/thermal/Tunable.gds",
    show=True,
)
