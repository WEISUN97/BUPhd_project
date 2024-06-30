import sys
import math

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator

from cnstpy.geo import (
    RectangleLH,
    Roundrect,
    RoundedCorners,
    TextOutline,
    RectTaper,
    Points2Shape,
    Comb,
    RotateRec,
    RotateRoundrect,
    HollowUnit,
    Circle,
    Structure,
    Instance,
    AlignCustC1,
)


connector = Structure("Tunable")
L_beam_list = [100, 500, 1000]
w_beam_list = [0.05, 0.1, 0.2, 0.1, 0.05, 0.1, 0.2, 0.1]
gap_actuators_y_list = [1, 3]  # gap between actuators and beams
for m in range(2):
    gap_actuators_y = gap_actuators_y_list[m]
    for k in range(3):
        # y_beam = -562.025 + 1200
        y_beam = 1200
        r = 0.1  # round corner of beam
        w_cable = 27.45
        r_cable = 10
        w_support = 1
        L_support = 28
        w_support2 = 40
        L_support2 = 40
        L_electrode = 350
        # L_beam = 100 + k * 50
        L_beam = 100
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 100  # gap between electrodes in y direction
        gap_3 = L_beam  # gap between electrodes in x direction
        gap_actuators_x = 2  # gap between actuators
        h_actuators = 0.5
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        temp_x = 0 if k == 0 else L_beam_list[k - 1]
        x_beam = m * 4500 + k * 1000 + temp_x
        L_1 = 150  # length of rectaper
        L_2 = 50  # length of rectaper
        for j in range(8):
            y_beam -= 1200
            connector.add("10 layer")
            L_beam = L_beam_list[k]
            w_cable = 50 + (150 / 900) * (L_beam - 100)
            if k > 0 and (j == 3 or j == 7):
                continue
            if k == 0 and (j == 3 or j == 7):
                L_beam = 3000
                w_cable = 200
            L_actuator = L_beam - 30
            gap_3 = L_beam  # gap between electrodes in x direction
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            w_beam = w_beam_list[j]
            # beam
            connector.add(
                RectangleLH(
                    x_beam + w_support / 2,
                    y_beam + (L_support - w_beam) / 2,
                    L_beam,
                    w_beam,
                    0,
                ),
            )
            # right support
            temp = w_support2 / 4

            p1_2 = [
                (
                    x_beam + w_support / 2 + L_beam + temp,
                    y_beam + (L_support + L_support2) / 2,
                )
            ]
            p2_2 = [(p1_2[0][0] - temp, p1_2[0][1] - L_support2 / 2 + w_beam / 2)]
            p3_2 = [(p2_2[0][0], p2_2[0][1] - w_beam)]
            p4_2 = [(p1_2[0][0], p1_2[0][1] - L_support2)]
            p5_2 = [(p4_2[0][0] + 0.75 * w_support2, p4_2[0][1])]
            p6_2 = [(p5_2[0][0], p1_2[0][1])]
            connector.add(
                (Points2Shape(p1_2 + p2_2 + p3_2 + p4_2 + p5_2 + p6_2),),
            )

            # actuators
            x_actuator = x_beam + w_support / 2 + L_beam / 2 - L_actuator / 2
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
                        y_actuator - L_2 - L_1 - 10,
                        w_cable,
                        L_1 + 10,
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
                        y_actuator + L_2 + h_actuators + L_1 + 10,
                        w_cable,
                        L_1 + 10,
                        L_actuator - h_actuators,
                        L_2,
                        -90,
                    ),
                )
            )
            # comb drive
            # def left support
            c = 3  # number of support except the beam support
            for i in range(c):
                connector.add(
                    RectangleLH(
                        x_beam - w_support / 2 - i * w_support,
                        y_beam,
                        w_support,
                        L_support,
                        0,
                    ),
                )
            # round corner of left support
            connector.add(
                (
                    RoundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support + w_beam) / 2 + r,
                        r,
                        180,
                    ),
                    RoundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support - w_beam) / 2 - r - j * 100,
                        r,
                        90,
                    ),
                )
            )
            # beam side
            x_comb = x_beam - c * w_support + w_support / 2
            y_comb = y_beam
            hollow_comb_x = x_comb - w_support / 2
            hollow_comb_y = y_comb + 0.5
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
            # fixed side
            L_sub = N * 2 * (b_comb + g_comb) + b_comb
            w_sub = 36
            x_comb = x_comb - w_support - (d_comb + L_comb) - w_sub
            y_comb = y_beam + L_support - d + g_comb + b_comb
            d = 0
            N += 1
            connector.add(
                Comb(x_comb, y_comb, L_sub, w_sub, L_comb, b_comb, d, s, N, -90)
            )
            # Spring
            t_spring = 0.15
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
                    x_start = x_beam - w_support + w_support / 2
                    y_start = y_beam + L_support - 7
                    hollow_side_x_1 = x_start + 0.5
                    hollow_side_y_1 = y_start + 0.5 + 0.05
                # buttom spring
                else:
                    theta = 180
                    x_start = x_start + L_top + 2 * (t_side + t_spring)
                    d_gap = (L_support / 2 - 3) * 2
                    y_start = y_beam + L_support + 1 - d_gap
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
            x_text = (
                x_beam - w_support + w_support / 2 + L_beam / 2 + L_electrode / 2 + 60
            )
            y_text = y_beam + L_electrode / 2 + 60
            text = f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} G={gap_actuators_y}"

            connector.add(
                (TextOutline(text, "Times New Roman", fontSize, x_text, y_text))
            )
            # frame of actuator
            frame_x = x_comb
            frame_y = y_beam + L_support / 2 - L_2 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = (
                x_beam - w_support + w_support / 2 * 3 + L_beam + w_support2 - frame_x
            )
            x_actuator = x_beam - w_support + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
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
                        x_beam
                        - w_support
                        + w_support / 2
                        + L_beam / 2
                        + w_cable / 2
                        + 10,
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
                        x_beam
                        - w_support
                        + w_support / 2
                        + L_beam / 2
                        - w_cable / 2
                        - 10,
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
                    hollow_comb_y += 1
                # hollow part of all vertical support (number = c+1)
                for i in range(c + 1):
                    connector.add(
                        (
                            HollowUnit(
                                hollow_comb_x + i * w_support,
                                hollow_comb_y,
                                0.05,
                                1,
                            ),
                            Circle(
                                hollow_comb_x + i * w_support,
                                hollow_comb_y,
                                0.075,
                                0.001,
                            ),
                        )
                    )
                    # intersection of vertical support
                    if i < c and n < L_support - 1:
                        connector.add(
                            Circle(
                                hollow_comb_x + w_support / 2 + i * w_support,
                                hollow_comb_y + w_support / 2,
                                0.075,
                                0.001,
                            ),
                        )
                if n == L_support - 1:
                    continue
            # spring part
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
            # "left, right, top, bottom"
            x_start = [
                x_comb - L_electrode,
                x_beam - w_support + w_support / 2 * 3 + L_beam + w_support2,
                x_beam - w_support + w_support / 2 + L_beam / 2 - L_electrode / 2,
                x_beam - w_support + w_support / 2 + L_beam / 2 - L_electrode / 2,
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
            frame_x = x_beam - w_support - w_support / 2
            frame_y = y_beam + L_support / 2 - L_2 - 10
            frame_height = (L_2 + gap_actuators_y + h_actuators) * 2 + w_beam + 20
            frame_length = 1.5 * w_support + L_beam
            x_actuator = x_beam - w_support + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
            )
            connector.add(
                (
                    # center
                    RectangleLH(
                        x_comb,
                        frame_y + 5,
                        x_beam
                        - w_support
                        + w_support / 2 * 3
                        + L_beam
                        + w_support2
                        - x_comb,
                        frame_height - 10,
                        0,
                    ),
                    # down
                    RectangleLH(
                        x_beam
                        - w_support
                        + w_support / 2
                        + L_beam / 2
                        + w_cable / 2
                        + 5,
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
                        x_beam
                        - w_support
                        + w_support / 2
                        + L_beam / 2
                        - w_cable / 2
                        - 5,
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
            x_text = (
                x_beam - w_support + w_support / 2 + L_beam / 2 + L_electrode / 2 + 35
            )
            y_text = y_beam + L_electrode / 2 + 55
            connector.add((RectangleLH(x_text - 2.5, y_text - 2.5, 315, 35, 0),))

connector.add("11 layer")
text = "Zhou Lab\nWei Sun 2024"
fontSize = 50
spacing = 50
text_x = temp_text[0][3] + L_electrode + 1500
text_y = temp_text[1][3] + 100
connector.add((TextOutline(text, "Times New Roman", fontSize, text_x, text_y, spacing)))
# frame of text in layer 20
connector.add("20 layer")
connector.add(
    RectangleLH(
        text_x - 20,
        text_y - 2 * fontSize,
        320,
        2 * fontSize + 20 + spacing,
        0,
    )
)

# frame of lithography
connector.add("21 layer")
connector.add(
    RectangleLH(
        -391.5 - 10,
        -8939.55 - 10,
        8390.5 + 391.5 + 20,
        565.525 + 8939.55 + 20,
        0,
    )
)

# Array
array = Structure("Array")
for i in range(3):
    array.add(Instance(connector, 10000 * i, 0, "N", 1, 0))

# alignment marks in layer 11
array.add("11 layer")
array.add(AlignCustC1(-510, -3600, 100, 2, 100, 0, 120, 120, 0))
array.add(AlignCustC1(28510, -3600, 100, 2, 100, 0, 120, 120, 0))
array.add(AlignCustC1(-510, -6600, 100, 2, 100, 0, 120, 120, 0))
array.add(AlignCustC1(28510, -6600, 100, 2, 100, 0, 120, 120, 0))
# alignment marks in layer 21
array.add("21 layer")
array.add(AlignCustC1(-510, -3600, 100, 2, 100, 0, 120, 120, 0))
array.add(AlignCustC1(28510, -3600, 100, 2, 100, 0, 120, 120, 0))
array.add(AlignCustC1(-510, -6600, 100, 2, 100, 0, 120, 120, 0))
array.add(AlignCustC1(28510, -6600, 100, 2, 100, 0, 120, 120, 0))

gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.add(array)
gen.generate(
    "result_wei/tunable_device/comb/Tunable_comb.cnst",
    "result_wei/tunable_device/comb/Tunable_comb.gds",
    show=True,
)
