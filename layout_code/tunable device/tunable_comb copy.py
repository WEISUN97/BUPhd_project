import sys
import math

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
    comb,
    Structure,
)

gen = CNSTGenerator(shapeReso=0.01)
connector = Structure("Tunable")
connector.add("10 layer")
for m in range(1):
    for k in range(3):
        r = 1  # round corner of beam
        w_cable = 2
        r_cable = 10
        w_support = 1
        L_support = 14.7
        w_support2 = 10
        L_support2 = 10
        L_beam = 100 + k * 50
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 100  # gap between electrodes in y direction
        gap_3 = L_beam  # gap between electrodes in x direction
        gap_cell_x = 140  # gap between cells in x direction
        gap_actuators_x = 2  # gap between actuators
        gap_actuators_y = 0.4  # gap between actuators and beams
        L_actuator = L_beam - 2 * gap_actuators_x
        h_actuators = 0.5
        L_electrode = 450
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        x_beam = k * 800 + 20
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode
        L_1 = 0  # length of rectaper
        L_2 = 5  # length of rectaper
        for j in range(3):
            w_beam = 0.04 + j * 0.01

            # beam
            connector.add(
                RectangleLH(
                    x_beam + w_support / 2,
                    y_beam + (L_support - w_beam) / 2 - j * 300,
                    L_beam,
                    w_beam,
                    0,
                ),
            )
            # right support
            x1 = x_beam + w_support / 2 + L_beam
            y1 = y_beam + (L_support - w_beam) / 2 - j * 300
            p1 = [(x1, y1)]
            p2 = [(x1, y1 + w_beam)]
            p3 = [(x1 + 3, y1 + (L_support2 + w_beam) / 2)]
            p4 = [(x1 + w_support2, y1 + (L_support2 + w_beam) / 2)]
            p5 = [(x1 + w_support2, y1 - (L_support2 - w_beam) / 2)]
            p6 = [(x1 + 3, y1 - (L_support2 - w_beam) / 2)]
            connector.add(
                (
                    # def support
                    Points2Shape(p1 + p2 + p3 + p4 + p5 + p6),
                ),
            )
            connector.add(
                (
                    roundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support + w_beam) / 2 + r - j * 300,
                        r,
                        180,
                    ),
                    roundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support - w_beam) / 2 - r - j * 300,
                        r,
                        90,
                    ),
                )
            )
        # pad
        # for j in range(3):
        #     for i in range(2):
        #         for p in range(2):
        #             connector.add(
        #                 RectangleLH(
        #                     x_beam
        #                     - L_electrode
        #                     + p * (L_electrode + gap_3 - cable_offset)
        #                     + cable_offset,
        #                     y_beam
        #                     + L_support / 2
        #                     + gap_2 / 2
        #                     - i * (gap_2 + L_electrode)
        #                     - j * 300,
        #                     L_electrode,
        #                     L_electrode,
        #                     0,
        #                 ),
        #             )
        # actuators
        for j in range(3):
            w_beam = 0.04 + j * 0.01

            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 300
            )

            connector.add(
                (
                    # roundcorner of actuator d = 1
                    roundrect(
                        x_actuator,
                        y_actuator,
                        L_actuator,
                        h_actuators,
                        h_actuators,
                        h_actuators,
                        0,
                    ),
                    rectTaper(
                        x_actuator + L_actuator / 2,
                        y_actuator - L_2,
                        w_cable,
                        L_1,
                        L_actuator - h_actuators,
                        L_2,
                        90,
                    ),
                )
            )
        # comb drive
        for j in range(3):
            w_beam = 0.04 + j * 0.01
            # beam side
            x_comb = x_beam + w_support / 2
            y_comb = y_beam - j * 300
            g_comb = 0.3
            b_comb = 0.3
            d_comb = 0.5
            L_overlapping = 1
            L_comb = d_comb + L_overlapping
            # N = math.floor(L_support / 2 / (b_comb + g_comb))
            N = 12
            d = (L_support - N * 2 * (b_comb + g_comb) - b_comb) / 2
            N += 1
            s = b_comb + 2 * g_comb
            x_comb_2 = x_beam + w_support / 2
            y_comb_2 = y_beam + L_support / 2 - gap_2 / 2 - j * 300

            connector.add(
                comb(x_comb, y_comb, L_support, w_support, L_comb, b_comb, d, s, N, 90)
            )
            # fixed side
            L_sub = N * 2 * (b_comb + g_comb) + b_comb
            w_sub = 10
            x_comb = x_beam - w_support / 2 - (d_comb + L_comb) - w_sub
            y_comb = y_beam + L_support - d + g_comb + b_comb - j * 300
            d = 0
            N += 1
            connector.add(
                comb(x_comb, y_comb, L_sub, w_sub, L_comb, b_comb, d, s, N, -90)
            )

        # cables
        for j in range(3):
            w_beam = 0.04 + j * 0.01

            # cables of beam
            # cable of right support
            center_start_x = x_beam + w_support / 2 + L_beam + w_support2 / 2
            center_start_y = y_beam + L_support / 2 + L_support2 / 2 - j * 300
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 300 + cable_in
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))
            # cable of left support
            center_start_x = x_beam - w_support / 2 - L_comb - d_comb - w_sub / 2
            center_start_y = y_beam + L_support + g_comb + b_comb - j * 300
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))
            # cable of electrode
            center_start_x = x_beam + w_support / 2 + gap_actuators_x + L_actuator / 2
            center_start_y = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - L_2
                - j * 300
            )
            electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 300 - cable_in
            electrode_x = x_beam - 20
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
                (electrode_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))

        # # Spring
        # for j in range(1):
        #     t_spring = 0.22
        #     L_spring = 20
        #     x_start = x_beam + w_support / 2
        #     y_start = y_beam + L_support - 8 - j * 300

        #     connector.add(
        #         RectangleLH(
        #             x_start,
        #             y_start,
        #             t_spring,
        #             L_spring,
        #             0,
        #         ),
        #     )

        # Text
        for j in range(3):
            w_beam = 0.04 + j * 0.01
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 10
            y_text = y_beam + L_support / 2 - j * 300 - fontSize / 2
            text = [
                f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} L/t={int(L_beam/w_beam)}",
            ]
            connector.add(
                (
                    multyTextOutline(
                        text, "Times New Roman", fontSize, spacing, x_text + 20, y_text
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
                - j * 300
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

connector.add("11 layer")

# frame for beam
for k in range(3):
    L_beam = 100 + k * 50
    x_beam = k * 800 + 20
    for j in range(3):
        w_beam = 0.04 + j * 0.01
        frame_x = x_beam - 20
        frame_y = y_beam + L_support / 2 - gap_2 / 2 - j * 300 - cable_in - 10
        frame_height = (
            y_beam + L_support / 2 + gap_2 / 2 - j * 300 + cable_in
        ) - frame_y
        frame_length = (
            (x_beam + w_support / 2 + L_beam + w_support2 / 2) + w_cable - frame_x
        )
        connector.add(
            RectangleLH(
                frame_x,
                frame_y,
                frame_length + 10,
                frame_height,
                0,
            ),
        )
        fontSize = 25
        spacing = 25
        x_text = x_beam + w_support / 2 + L_beam + 30
        y_text = y_beam + L_support / 2 - j * 300 - fontSize / 2
        connector.add((RectangleLH(x_text - 2.5, y_text - 2.5, 380, 25, 0),))

gen.add(connector)

# result = Structure("result")
# result.add(Boolean(11, 10, 2, "subtract"))
# gen.add(result)
gen.generate(
    "result_wei/tunable_device/comb/Tunable.cnst",
    "result_wei/tunable_device/comb/Tunable.gds",
    show=True,
)
