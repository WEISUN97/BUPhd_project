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

connector = Structure("Tunable")
gap_actuators_y_list = [1, 3]
for m in range(1):
    for k in range(1):
        r = 0.1  # round corner of beam
        r_cable = 10
        w_support = 20
        L_support = 15
        w_cable = L_support
        w_beam_list = [0.05, 0.075, 0.1]
        L_beam = 100 + k * 50
        gap_2 = 100  # gap between electrodes in y direction
        gap_actuators_x = 2  # gap between actuators
        gap_actuators_y = gap_actuators_y_list[m]  # gap between actuators and beams
        L_actuator = (L_beam - 2 * gap_actuators_x) / 3
        h_actuators = 0.5
        L_electrode = 450
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10 + w_cable / 2  # offset of cable in x direction
        x_beam = (
            -(w_support / 2 - L_electrode + gap_actuators_x + L_actuator)
            + k * 1200
            + m * 3500
        )
        y_beam = -L_support / 2 - gap_2 / 2 - L_electrode
        L_1 = 0  # length of rectaper
        L_2 = 5  # length of rectaper
        for j in range(1):
            connector.add("10 layer")
            w_beam = w_beam_list[j] * 2
            # beam
            connector.add(
                RectangleLH(
                    x_beam + w_support / 2,
                    y_beam + (L_support - w_beam) / 2 - j * 1050,
                    L_beam,
                    w_beam,
                    0,
                ),
            )
            temp = w_support / 4
            p1_1 = [(x_beam + temp, y_beam - j * 1200)]
            p2_1 = [(p1_1[0][0] + temp, p1_1[0][1] + (L_support - w_beam) / 2)]
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
                - j * 1050
            )
            for i in range(2):
                x_actuator = (
                    x_beam
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
            center_start_x_1 = x_beam - w_support / 8
            center_start_y_1 = y_beam + L_support - j * 1050
            electrode_y_1 = y_beam + gap_2 / 2 - j * 1050 + cable_in
            point = [
                (center_start_x_1, center_start_y_1),
                (center_start_x_1, electrode_y_1),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of right support
            center_start_x_2 = x_beam + w_support + L_beam + w_support / 8
            center_start_y_2 = y_beam + L_support - j * 1050
            electrode_y_2 = y_beam + L_support / 2 + gap_2 / 2 - j * 1050 + cable_in
            point = [
                (center_start_x_2, center_start_y_2),
                (center_start_x_2, electrode_y_2),
            ]
            connector.add((BendWaveguide(point, r_cable, 3 / 4 * w_support, 30),))
            # cable of left electrode
            center_start_x_3 = x_beam + gap_actuators_x + w_support / 2 + L_actuator / 2
            center_start_y_3 = (
                y_beam
                + (L_support - w_beam) / 2
                - gap_actuators_y
                - h_actuators
                - L_2
                - j * 1050
            )
            electrode_y_3 = y_beam + L_support / 2 - gap_2 / 2 - j * 1050 - cable_in
            point = [
                (center_start_x_3, center_start_y_3),
                (center_start_x_3, electrode_y_3),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            center_start_x_4 = x_actuator + L_actuator / 2
            point = [
                (center_start_x_4, center_start_y_3),
                (center_start_x_4, electrode_y_3),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))

            # Text
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - j * 1050 - fontSize / 2
            text = (
                f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} L/t={int(L_beam/w_beam)}"
            )

            connector.add(
                (
                    TextOutline(
                        text, "Times New Roman", spacing, x_text, y_text, fontSize
                    )
                )
            )
            # pad
            connector.add("20 layer")
            x_start = [
                center_start_x_1 + cable_offset - L_electrode,
                center_start_x_2 - cable_offset,
                center_start_x_3 + cable_offset - L_electrode,
                center_start_x_4 - cable_offset,
            ]
            y_start = [
                electrode_y_1 - cable_in,
                electrode_y_2 - cable_in,
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


# # Alignment Marks
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
