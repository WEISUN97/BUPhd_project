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
    Structure,
    AlignCustC1,
)

gen = CNSTGenerator(shapeReso=0.01)
connector = Structure("Tunable")
connector.add("10 layer")
for m in range(1):
    for k in range(3):
        r = 1  # round corner of beam
        w_cable = 13.65
        r_cable = 10
        w_support = 1
        L_support = 15
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
                    RoundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support + w_beam) / 2 + r - j * 300,
                        r,
                        180,
                    ),
                    RoundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support - w_beam) / 2 - r - j * 300,
                        r,
                        90,
                    ),
                )
            )

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
            y_comb = y_beam - j * 1050
            hollow_support_x = x_comb - w_support / 2
            hollow_support_y = y_comb + 0.5
            g_comb = 0.3
            b_comb = 0.15
            d_comb = 0.5
            L_overlapping = 1
            L_comb = d_comb + L_overlapping
            # N = math.floor(L_support / 2 / (b_comb + g_comb))
            N = 14
            d = (L_support - N * 2 * (b_comb + g_comb) - b_comb) / 2
            N += 1
            s = b_comb + 2 * g_comb
            connector.add(
                Comb(x_comb, y_comb, L_support, w_support, L_comb, b_comb, d, s, N, 90)
            )
            # fixed side
            L_sub = N * 2 * (b_comb + g_comb) + b_comb
            w_sub = 10
            x_comb = x_beam - w_support / 2 - (d_comb + L_comb) - w_sub
            y_comb = y_beam + L_support - d + g_comb + b_comb - j * 1050
            d = 0
            N += 1
            connector.add(
                Comb(x_comb, y_comb, L_sub, w_sub, L_comb, b_comb, d, s, N, -90)
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
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of left support
            center_start_x = x_beam - w_support / 2 - L_comb - d_comb - w_sub / 2
            center_start_y = y_beam + L_support + g_comb + b_comb - j * 300
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
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
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # Spring
            t_spring = 0.15
            L_spring = 20
            t_side = 0.85
            L_anchor = w_anchor = 5
            gap_anchor = 2
            gap_anchor_buttom = 1
            L_top = 9
            w_top = 1
            L_side = w_top + gap_anchor_buttom + L_anchor
            for n in range(2):
                # top spring
                if n == 0:
                    theta = 0
                    x_start = x_beam + w_support / 2
                    y_start = y_beam + L_support - 3 - j * 1050
                    hollow_side_x_1 = x_start + 0.5
                    hollow_side_y_1 = y_start + 0.5
                else:
                    theta = 180
                    x_start = x_start + L_top + 2 * (t_side + t_spring)
                    d_gap = (L_support / 2 - 3) * 2
                    y_start = y_beam + L_support - 3 - j * 1050 - d_gap
                    hollow_side_x_2 = x_start - 0.5 - L_top - (t_side + t_spring)
                    hollow_side_y_2 = y_start - 0.5
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
        for j in range(3):
            w_beam = 0.04 + j * 0.01
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 10
            y_text = y_beam + L_support / 2 - j * 300 - fontSize / 2
            text = (
                f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} L/t={int(L_beam/w_beam)}"
            )
            connector.add(
                (
                    TextOutline(
                        text,
                        "Times New Roman",
                        fontSize,
                        x_text + 20,
                        y_text,
                        spacing,
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
