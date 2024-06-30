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
    Circle,
    RotateRoundrect,
    RotateRec,
    HollowUnit,
    Structure,
    AlignCustC1,
)

# connector = Structure("Tunable")


def optical_comb(connector, x, y, pos, is_AFM=False):
    # gap_actuators_y_list = [1, 3]
    result = []
    w_beam_list = [0.05, 0.075, 0.1]
    for k in range(3):
        r = 0.1  # round corner of beam
        r_cable = 10
        w_support = 1  # width of left support
        L_support = 28  # height of left support
        L_support2 = 20  # height of right support
        w_support2 = L_support2 / 3 * 4  # length of right support
        w_cable = L_support2
        L_beam_list = [200, 350, 500]  # length of beam
        distance = 1500  # gap between two cell in x direction
        gap_2 = 100  # gap between electrodes in y direction
        gap_actuators_x = 2  # gap between actuators
        h_actuators = 0.5
        L_electrode = 350
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10 + w_cable / 2  # offset of cable in x direction
        w_beam = w_beam_list[k]
        for j in range(3):
            x_beam = k * distance - L_beam_list[j] / 2 + x
            y_beam = y - j * 1050
            L_beam = L_beam_list[j]
            L_actuator = (L_beam - 2 * gap_actuators_x) / 3
            L_1 = 0  # length of rectaper
            L_2 = 5 * (L_beam / 200)  # length of rectaper
            gap_actuators_y = 1
            connector.add("10 layer")
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

            # comb drive
            # left support
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
                        y_beam + (L_support - w_beam) / 2 - r,
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
                Comb(
                    x_comb,
                    y_comb,
                    L_support,
                    w_support,
                    L_comb,
                    b_comb,
                    d,
                    s,
                    N,
                    90,
                )
            )
            # fixed side
            L_sub = N * 2 * (b_comb + g_comb) + b_comb
            w_sub = w_cable
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
            t_side = 0.85
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
            # actuators
            y_actuator = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
            )
            for i in range(2):
                x_actuator = (
                    x_beam
                    - w_support
                    + gap_actuators_x
                    + w_support / 2
                    + i * (L_actuator + L_beam - 2 * (L_actuator + gap_actuators_x))
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

            # cables
            # cables of beam
            # cable of lefy support
            center_start_x_1 = x_comb + w_cable / 2
            center_start_y_1 = y_beam + (L_sub + L_support) / 2
            electrode_y_1 = y_beam + L_support / 2 + gap_2 / 2 + cable_in
            point = [
                (center_start_x_1, center_start_y_1),
                (center_start_x_1, electrode_y_1),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of right support
            center_start_x_2 = x_beam + w_support / 2 + L_beam + w_support2 / 8 * 5
            center_start_y_2 = y_beam + L_support / 2 + L_support2 / 2
            electrode_y_2 = y_beam + L_support / 2 + gap_2 / 2 + cable_in
            point = [
                (center_start_x_2, center_start_y_2),
                (center_start_x_2, electrode_y_2),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of left electrode
            center_start_x_3 = (
                x_beam - w_support + gap_actuators_x + w_support / 2 + L_actuator / 2
            )
            center_start_y_3 = (
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators - L_2
            )
            electrode_y_3 = y_beam + L_support / 2 - gap_2 / 2 - cable_in
            point = [
                (center_start_x_3, center_start_y_3),
                (center_start_x_3, electrode_y_3),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            center_start_x_4 = x_actuator + L_actuator / 2
            center_start_y_4 = center_start_y_3
            electrode_y_4 = electrode_y_3
            point = [
                (center_start_x_4, center_start_y_4),
                (center_start_x_4, electrode_y_4),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # AFM Tip
            tip_center_x = x_beam + w_support / 2 + L_beam / 2
            # print(f"center of the beam is 'tip_center_x'{tip_center_x}")
            tip_center_y = y_beam + L_support / 2 + w_beam / 2
            tip_height = L_beam / 200
            temp = tip_height * math.tan(math.pi / 12)
            points = [
                (tip_center_x - temp, tip_center_y),
                (tip_center_x, tip_center_y + tip_height),
                (tip_center_x + temp, tip_center_y),
            ]
            result.append([tip_center_x, tip_center_y - w_beam])
            if is_AFM:
                connector.add(Points2Shape(points))

            # hollow part
            connector.add("9 layer")
            # AFM Tip
            hollow_temp = temp - 0.1
            hollo_tip_height = hollow_temp / math.tan(math.pi / 12)
            # print(hollo_tip_height)
            points = [
                (tip_center_x - hollow_temp, tip_center_y),
                (tip_center_x, tip_center_y + hollo_tip_height),
                (tip_center_x + hollow_temp, tip_center_y),
            ]
            if is_AFM:
                connector.add(Points2Shape(points))

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
                connector.add(
                    Circle(
                        hollow_comb_x + w_support / 2,
                        hollow_comb_y + w_support / 2,
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
            connector.add("11 layer")
            # Text
            fontSize = 25
            spacing = 25
            x_text = x_beam - w_support + w_support / 2 + L_beam + 120
            y_text = y_beam + L_support / 2 - fontSize / 2
            text = f"{pos} {j+1}.{k+1} L={L_beam} t={w_beam}"

            connector.add(
                (
                    TextOutline(
                        text, "Times New Roman", spacing, x_text, y_text, fontSize
                    )
                )
            )
            # frame of EBL
            connector.add(
                RectangleLH(
                    center_start_x_1 - w_cable / 2 - 10,
                    electrode_y_3,
                    center_start_x_2 - center_start_x_1 + w_cable + 20,
                    electrode_y_1 - electrode_y_3,
                    0,
                ),
            )
            # pads
            connector.add("20 layer")
            x_start = [
                center_start_x_1 + cable_offset - L_electrode,
                center_start_x_2 - cable_offset,
                center_start_x_3 + w_cable / 2 - L_electrode,
                center_start_x_4 - w_cable / 2,
            ]
            y_start = [
                electrode_y_1 - cable_in,
                electrode_y_2 - cable_in + 5,
                electrode_y_3 - L_electrode + cable_in,
                electrode_y_3 - L_electrode + cable_in,
            ]
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
            # frame of lithography (beam part)
            connector.add(
                (
                    RectangleLH(
                        center_start_x_1 - w_cable / 2 - 5,
                        electrode_y_3 + 5,
                        center_start_x_2 - center_start_x_1 + w_cable + 10,
                        electrode_y_1 - electrode_y_3 - 10,
                        0,
                    ),
                    # waveguide part
                    RectangleLH(
                        center_start_x_3 + w_cable / 2 + 15,
                        electrode_y_3 + cable_in - L_electrode - 20,
                        center_start_x_4 - center_start_x_3 - w_cable - 30,
                        L_electrode + 20,
                        0,
                    ),
                )
            )
            # frame of lithography
            connector.add("21 layer")
            connector.add(
                RectangleLH(
                    x_start[0] - 10,
                    y_start[2] - 10,
                    x_start[1] + L_electrode - x_start[0] + 20,
                    y_start[0] + L_electrode - y_start[2] + 20,
                    0,
                ),
            )

    # # Alignment Marks
    # connector.add("11 layer")
    # connector.add(AlignCustC1(-350, -3150, 100, 2, 100, 0, 120, 120, 0))
    # connector.add(AlignCustC1(7000, -3150, 100, 2, 100, 0, 120, 120, 0))
    return result


# Test
if __name__ == "__main__":
    gen = CNSTGenerator(shapeReso=0.01)
    connector = Structure("Tunable")
    # top right
    position_2 = optical_comb(connector, 7500, 0, "C", True)
    print(position_2)
    # buttom left
    position_4 = optical_comb(connector, 7500, -3000, "D", False)
    print(position_4)
    gen.add(connector)
    gen.generate(
        "result_wei/tunable_device/optical/optical_thermal/optical_thermal.cnst",
        "result_wei/tunable_device/optical/optical_thermal/optical_thermal.gds",
        show=True,
    )
