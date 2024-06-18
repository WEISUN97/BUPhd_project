import sys
import math

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator

from cnstpy.geo import (
    RectangleLH,
    Roundrect,
    RoundedCorners,
    Circle,
    TextOutline,
    RectTaper,
    Points2Shape,
    Comb,
    RotateRec,
    RotateRoundrect,
    HollowUnit,
    Structure,
    AlignCustC1,
)

connector = Structure("Tunable")
for m in range(1):
    for k in range(1):
        r = 0.1  # round corner of beam
        w_cable = 13.65
        r_cable = 10
        w_support = 1
        L_support = 23
        w_support2 = 20
        L_support2 = 20
        w_beam_list = [0.05, 0.075, 0.1]
        L_beam = 100
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 100  # gap between electrodes in y direction
        gap_3 = L_beam  # gap between electrodes in x direction
        gap_actuators_x = 2  # gap between actuators
        gap_actuators_y = 0.4  # gap between actuators and beams
        L_actuator = L_beam - 2 * gap_actuators_x
        h_actuators = 0.5
        L_electrode = 450
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10  # offset of cable in x direction
        x_beam = (
            -(w_support / 2 - L_electrode + gap_actuators_x + L_actuator)
            + k * 1200
            + m * 3500
        )
        x_beam_2 = x_beam + w_support
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode
        L_1 = 0  # length of rectaper
        L_2 = 5  # length of rectaper
        for j in range(3):
            connector.add("10 layer")
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
            x_actuator = x_beam + gap_actuators_x + w_support / 2
            y_actuator = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - j * 100
            )

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
            # beam side
            x_comb = x_beam + w_support / 2
            y_comb = y_beam - j * 100
            hollow_support_x = x_comb - w_support / 2
            hollow_support_y = y_comb + 0.5
            g_comb = 0.3
            b_comb = 0.15
            d_comb = 0.5
            L_overlapping = 1
            L_comb = d_comb + L_overlapping
            # N = math.floor(L_support / 2 / (b_comb + g_comb))
            N = 24
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
            w_sub = 10
            x_comb = x_beam - w_support / 2 - (d_comb + L_comb) - w_sub
            y_comb = y_beam + L_support - d + g_comb + b_comb - j * 100
            d = 0
            N += 1
            connector.add(
                Comb(x_comb, y_comb, L_sub, w_sub, L_comb, b_comb, d, s, N, -90)
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
                            y_start + gap_anchor_buttom + w_top,
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
            # Text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - j * 100 - fontSize / 2
            t2 = [0.05, 0.075, 0.1]
            text = f"{j+1} t={w_beam} t2={t2[j]}"

            connector.add(
                (
                    TextOutline(
                        text, "Times New Roman", spacing, x_text, y_text, fontSize
                    )
                )
            )
            # hollow test
            for i in range(3):
                connector.add(
                    (
                        RectangleLH(
                            x_comb + 400 + i,
                            y_comb - 40,
                            1,
                            50,
                            0,
                        ),
                        RectangleLH(
                            x_comb + 410 + i,
                            y_comb - 40,
                            1,
                            50,
                            0,
                        ),
                    )
                )

            # hollow part
            connector.add("9 layer")
            for n in range(23):
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
                            hollow_support_x + w_support, hollow_support_y, 0.075, 0.001
                        ),
                    )
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
            # hollow test
            for i in range(3):
                x1 = x_comb + 400 + i + 0.5
                x2 = x_comb + 410 + i + 0.5
                y = y_comb - 40 - 0.5
                t2 = [0.05, 0.075, 0.1]
                r_c = [0.075, 0.1, 0.125]
                for n in range(50):
                    y += 1
                    connector.add(
                        (
                            HollowUnit(
                                x1,
                                y,
                                t2[j],
                                1,
                            ),
                            Circle(x1, y, r_c[j], 0.001),
                            HollowUnit(x2, y, t2[j], 1),
                            Circle(x2, y, r_c[j], 0.001),
                        )
                    )

            # frame
            connector.add("11 layer")
            connector.add(
                (
                    RectangleLH(
                        x_comb - 3,
                        y_comb - 47,
                        140,
                        72,
                        0,
                    ),
                )
            )
            connector.add(
                (
                    RectangleLH(
                        x_comb + 170,
                        y_comb - 26,
                        185,
                        23,
                        0,
                    ),
                )
            )
            x1 = x_comb + 400 + i
            x2 = x_comb + 410 + i
            y = y_comb - 40
            t2 = [0.05, 0.075, 0.1]
            r_c = [0.075, 0.1, 0.125]
            connector.add(
                (
                    RectangleLH(
                        x1 - 2.5,
                        y - 0.5,
                        4,
                        51,
                        0,
                    ),
                    RectangleLH(
                        x2 - 2.5,
                        y - 0.5,
                        4,
                        51,
                        0,
                    ),
                )
            )


# Alignment Marks
# connector.add("11 layer")
# connector.add(AlignCustC1(-350, -3150, 100, 2, 100, 0, 120, 120, 0))
# connector.add(AlignCustC1(7000, -3150, 100, 2, 100, 0, 120, 120, 0))


gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.generate(
    "result_wei/tunable_device/comb/Tunable.cnst",
    "result_wei/tunable_device/comb/Tunable.gds",
    show=True,
)
