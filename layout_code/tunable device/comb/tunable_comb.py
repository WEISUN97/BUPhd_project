import sys
import math

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator

from cnstpy.geo import (
    RectangleLH,
    Roundrect,
    RoundedCorners,
    BendWaveguide,
    TextOutline,
    RectTaper,
    Points2Shape,
    Comb,
    RotateRec,
    RotateRoundrect,
    HollowUnit,
    Circle,
    Structure,
    AlignCustC1,
)


connector = Structure("Tunable")
L_electrode_2 = 350
for m in range(1):
    for k in range(1):
        r = 0.1  # round corner of beam
        w_cable = 27.45
        r_cable = 10
        w_support = 1
        L_support = 28
        w_support2 = 40
        L_support2 = 40
        w_beam_list = [0.05, 0.075, 0.1, 0.05, 0.075, 0.1]
        L_beam = 100 + k * 50
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 100  # gap between electrodes in y direction
        gap_3 = L_beam  # gap between electrodes in x direction
        gap_actuators_x = 2  # gap between actuators
        # gap_actuators_y = 1  # gap between actuators and beams
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
        L_actuator = L_beam - 30
        h_actuators = 0.5
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        x_beam = 0
        x_beam_2 = x_beam + w_support
        y_beam = 0
        L_1 = 150  # length of rectaper
        L_2 = 50  # length of rectaper
        for j in range(1):
            connector.add("10 layer")
            gap_actuators_y = gap_actuators_y_list[j]
            w_beam = w_beam_list[j] * 2
            # beam
            connector.add(
                RectangleLH(
                    x_beam_2 + w_support / 2,
                    y_beam + (L_support - w_beam) / 2 - j * 100,
                    L_beam,
                    w_beam,
                    0,
                ),
            )
            # right support
            x1 = x_beam_2 + w_support / 2 + L_beam
            y1 = y_beam + (L_support - w_beam) / 2 - j * 100
            p1 = [(x1, y1)]
            p2 = [(x1, y1 + w_beam)]
            p3 = [(x1 + L_support2 - w_cable, y1 + (L_support2 - w_beam) / 2)]
            p4 = [(x1 + w_support2, y1 + (L_support2 - w_beam) / 2)]
            p5 = [(x1 + w_support2, y1 - (L_support2 + w_beam) / 2)]
            p6 = [(x1 + L_support2 - w_cable, y1 - (L_support2 + w_beam) / 2)]
            connector.add(
                (
                    # def support
                    Points2Shape(p1 + p2 + p3 + p4 + p5 + p6),
                ),
            )
            connector.add(
                (
                    RoundedCorners(
                        x_beam_2 + w_support / 2 + r,
                        y_beam + (L_support + w_beam) / 2 + r - j * 100,
                        r,
                        180,
                    ),
                    RoundedCorners(
                        x_beam_2 + w_support / 2 + r,
                        y_beam + (L_support - w_beam) / 2 - r - j * 100,
                        r,
                        90,
                    ),
                )
            )

            # actuators
            x_actuator = x_beam_2 + L_beam / 2 - L_actuator / 2
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 1050
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
            # comb drive
            # beam side
            x_comb = x_beam + w_support / 2
            y_comb = y_beam - j * 100
            hollow_support_x = x_comb - w_support / 2
            hollow_support_y = y_comb + 0.5
            g_comb = 0.5
            b_comb = 0.15
            d_comb = 0.5
            L_overlapping = 1
            L_comb = d_comb + L_overlapping
            # N = math.floor(L_support / 2 / (b_comb + g_comb))
            N = 20
            d = (L_support - N * 2 * (b_comb + g_comb) - b_comb) / 2
            N += 1
            s = b_comb + 2 * g_comb
            connector.add(
                Comb(x_comb, y_comb, L_support, w_support, L_comb, b_comb, d, s, N, 90)
            )
            # def left support
            connector.add(
                RectangleLH(
                    x_beam + w_support / 2,
                    y_comb,
                    w_support,
                    L_support,
                    0,
                ),
            )
            # fixed side
            L_sub = N * 2 * (b_comb + g_comb) + b_comb
            w_sub = 36
            x_comb = x_beam - w_support / 2 - (d_comb + L_comb) - w_sub
            y_comb = y_beam + L_support - d + g_comb + b_comb - j * 100
            d = 0
            N += 1
            connector.add(
                Comb(x_comb, y_comb, L_sub, w_sub, L_comb, b_comb, d, s, N, -90)
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
            # Spring
            t_spring = 0.1
            L_spring = 20
            t_side = 0.9
            L_anchor = w_anchor = 5
            gap_anchor = 2
            gap_anchor_buttom = 1
            L_top = 9
            w_top = 1.1
            L_side = 1 + gap_anchor_buttom + L_anchor
            for n in range(2):
                # top spring
                if n == 0:
                    theta = 0
                    x_start = x_beam + w_support / 2
                    y_start = y_beam + L_support - 7 - j * 100
                    hollow_side_x_1 = x_start + 0.5
                    hollow_side_y_1 = y_start + 0.5 + 0.05
                # buttom spring
                else:
                    theta = 180
                    x_start = x_start + L_top + 2 * (t_side + t_spring)
                    d_gap = (L_support / 2 - 3) * 2
                    y_start = y_beam + L_support + 1 - j * 100 - d_gap
                    hollow_side_x_2 = x_start - 0.5 - L_top - (t_side + t_spring)
                    hollow_side_y_2 = y_start - 0.5 - 0.05
                connector.add(
                    (
                        # left side
                        RotateRec(
                            x_start,
                            y_start,
                            x_start,
                            y_start,
                            t_spring + t_side,
                            L_side,
                            theta,
                        ),
                        # right side
                        RotateRec(
                            x_start,
                            y_start,
                            x_start + L_top + t_spring + t_side,
                            y_start,
                            t_spring + t_side,
                            L_side,
                            theta,
                        ),
                        # bottom
                        RotateRec(
                            x_start,
                            y_start,
                            x_start + t_spring + t_side,
                            y_start,
                            L_top,
                            w_top,
                            theta,
                        ),
                        # top side
                        RotateRec(
                            x_start,
                            y_start,
                            x_start + t_side,
                            y_start + L_side + L_spring,
                            L_top + 2 * t_spring,
                            w_top,
                            theta,
                        ),
                        # anchor
                        RotateRoundrect(
                            x_start,
                            y_start,
                            x_start + t_spring + t_side + gap_anchor,
                            y_start + gap_anchor_buttom + w_top - 0.1,
                            L_anchor,
                            w_anchor,
                            0.5,
                            0.5,
                            theta,
                        ),
                    )
                )
                # 4 springs
                for i in range(4):
                    if i == 0:
                        gap_spring = 0
                    elif i == 2:
                        gap_spring += L_top / 3
                    else:
                        gap_spring += t_spring / 2 + L_top / 3
                    x_start_p = x_start + t_side + gap_spring
                    y_start_p = y_start + L_side
                    connector.add(
                        (
                            # left side
                            RotateRec(
                                x_start,
                                y_start,
                                x_start_p,
                                y_start_p,
                                t_spring,
                                L_spring,
                                theta,
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
            frame_x = x_beam - w_support / 2 - w_sub - L_comb - d_comb
            frame_y = y_beam + L_support / 2 - L_2 - j * 1200 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = x_beam + w_support / 2 * 3 + L_beam + w_support2 - frame_x
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
                        frame_length,
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
            # hollow part
            connector.add("9 layer")
            # hollow part of support
            for n in range(L_support):
                if n > 0:
                    hollow_support_y += 1
                connector.add(
                    (
                        HollowUnit(hollow_support_x, hollow_support_y, 0.05, 1),
                        HollowUnit(
                            hollow_support_x + w_support, hollow_support_y, 0.05, 1
                        ),
                        Circle(hollow_support_x, hollow_support_y, 0.075, 0.001),
                        Circle(
                            hollow_support_x + w_support,
                            hollow_support_y,
                            0.075,
                            0.001,
                        ),
                    )
                )
                if n == L_support - 1:
                    continue
                connector.add(
                    Circle(
                        hollow_support_x + w_support / 2,
                        hollow_support_y + w_support / 2,
                        0.075,
                        0.001,
                    ),
                )
            for p in range(2):
                # top
                if p == 0:
                    hollow_side_x = hollow_side_x_1
                    hollow_side_y = hollow_side_y_1
                # buttom
                else:
                    hollow_side_x = hollow_side_x_2
                    hollow_side_y = hollow_side_y_2
                hollow_side_buttom_x = hollow_side_x
                hollow_side_buttom_y = hollow_side_y
                for n in range(9):
                    if p == 0:
                        if n > 0:
                            hollow_side_y += 1
                            hollow_side_buttom_x += 1
                        hollow_side_top = hollow_side_buttom_y + L_side + L_spring

                    else:
                        if n > 0:
                            hollow_side_y -= 1
                            hollow_side_buttom_x += 1
                        hollow_side_top = hollow_side_buttom_y - L_side - L_spring
                    connector.add(
                        (
                            HollowUnit(
                                hollow_side_buttom_x + t_spring + t_side,
                                hollow_side_buttom_y,
                                0.05,
                                1.05,
                            ),
                            Circle(
                                hollow_side_buttom_x + t_spring + t_side,
                                hollow_side_buttom_y,
                                0.075,
                                0.001,
                            ),
                            HollowUnit(
                                hollow_side_buttom_x + t_spring + t_side,
                                hollow_side_top,
                                0.05,
                                1.05,
                            ),
                            Circle(
                                hollow_side_buttom_x + t_spring + t_side,
                                hollow_side_top,
                                0.075,
                                0.001,
                            ),
                        )
                    )
                    if n > 6:
                        continue
                    hollow_side_y_temp = (
                        hollow_side_y - 0.05 if p == 0 else hollow_side_y + 0.05
                    )
                    connector.add(
                        (
                            HollowUnit(hollow_side_x, hollow_side_y_temp, 0.05, 1),
                            HollowUnit(
                                hollow_side_x + L_top + t_spring + t_side,
                                hollow_side_y_temp,
                                0.05,
                                1,
                            ),
                            Circle(hollow_side_x, hollow_side_y_temp, 0.075, 0.001),
                            Circle(
                                hollow_side_x + L_top + t_spring + t_side,
                                hollow_side_y_temp,
                                0.075,
                                0.001,
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
                            x_beam
                            - w_support / 2
                            - L_electrode_2
                            - w_sub
                            - L_comb
                            - d_comb,
                            y_beam + L_support / 2 - j * 1200 - L_electrode_2 / 2,
                            L_electrode_2,
                            L_electrode_2,
                            0,
                        ),
                        # right
                        RectangleLH(
                            x_beam + w_support / 2 * 3 + L_beam + w_support2,
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
                    # center
                    RectangleLH(
                        x_comb,
                        frame_y + 5,
                        x_beam + w_support / 2 * 3 + L_beam + w_support2 - x_comb,
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


# # alignment marks in layer 11
# connector.add("11 layer")
# connector.add(AlignCustC1(-200, -5000, 100, 2, 100, 0, 120, 120, 0))
# connector.add(AlignCustC1(8940, -5000, 100, 2, 100, 0, 120, 120, 0))

# connector.add("21 layer")
connector.add("21 layer")
connector.add(
    RectangleLH(
        -410,
        -560,
        1050,
        1150,
        0,
    )
)
# # alignment marks in layer 21
# connector.add(AlignCustC1(-200, -5000, 100, 2, 100, 0, 120, 120, 0))
# connector.add(AlignCustC1(8940, -5000, 100, 2, 100, 0, 120, 120, 0))

# signature
#     text = ["Zhou Lab", "Wei Sun 2024"]
#     fontSize = 50
#     spacing = 50
#     text_x = x_beam
#     text_y = (
#         y_beam
#         + L_support / 2
#         - gap_2 / 2
#         - j * 1050
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

gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.generate(
    "result_wei/tunable_device/comb/Tunable_comb.cnst",
    "result_wei/tunable_device/comb/Tunable_comb.gds",
    show=True,
)
