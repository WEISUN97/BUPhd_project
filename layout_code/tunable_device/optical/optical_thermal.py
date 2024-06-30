import sys
import math

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

from cnstpy import CNSTGenerator

from cnstpy.geo import (
    RectangleLH,
    Roundrect,
    BendWaveguide,
    TextOutline,
    RectTaper,
    Points2Shape,
    Structure,
    AlignCustC1,
)


# connector = Structure("Tunable")
def optical_thermal(connector, x, y, pos, is_AFM=False):
    result = []
    # gap_actuators_y_list = [1, 3]
    for k in range(3):
        r_cable = 10
        L_support = 20  # height of right support
        w_support = L_support / 3 * 4  # length of right support
        w_cable = L_support
        w_beam_list = [0.05, 0.075, 0.1]
        L_beam_list = [200, 350, 500, 500]
        distance = 1500  # gap between two cell in x direction
        gap_2 = 100  # gap between electrodes in y direction
        gap_actuators_x = 2  # gap between actuators
        gap_actuators_y = 1  # gap between actuators and beams
        h_actuators = 0.5
        L_electrode = 350
        cable_in = 10  # length enter the electrode in y direction
        cable_offset = 10 + w_cable / 2  # offset of cable in x direction
        w_beam = w_beam_list[k]
        for j in range(3):
            y_beam = y - j * 1050
            L_beam = L_beam_list[j]
            L_actuator = (L_beam - 2 * gap_actuators_x) / 3
            x_beam = k * distance - L_beam_list[j] / 2 + x
            L_1 = 0  # length of rectaper
            L_2 = 5 * (L_beam / 200)  # length of rectaper
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
            temp = w_support / 4
            p1_1 = [(x_beam + temp, y_beam)]
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
                y_beam + (L_support - w_beam) / 2 - gap_actuators_y - h_actuators
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
            center_start_y_1 = y_beam + L_support
            electrode_y_1 = y_beam + L_support / 2 + gap_2 / 2 + cable_in
            point = [
                (center_start_x_1, center_start_y_1),
                (center_start_x_1, electrode_y_1),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable, 30),))
            # cable of right support
            center_start_x_2 = x_beam + w_support + L_beam + w_support / 8
            center_start_y_2 = y_beam + L_support
            electrode_y_2 = y_beam + L_support / 2 + gap_2 / 2 + cable_in
            point = [
                (center_start_x_2, center_start_y_2),
                (center_start_x_2, electrode_y_2),
            ]
            connector.add((BendWaveguide(point, r_cable, 3 / 4 * w_support, 30),))
            # cable of left electrode
            center_start_x_3 = x_beam + gap_actuators_x + w_support / 2 + L_actuator / 2
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
            tip_center_y = y_beam + L_support / 2 + w_beam / 2
            tip_height = L_beam / 200
            temp = tip_height * math.tan(math.pi / 12)
            points = [
                (tip_center_x - temp, tip_center_y),
                (tip_center_x, tip_center_y + tip_height),
                (tip_center_x + temp, tip_center_y),
            ]
            if is_AFM:
                connector.add(Points2Shape(points))
            result.append([tip_center_x, tip_center_y - w_beam])
            # hollow part
            connector.add("9 layer")
            # AFM Tip
            hollow_temp = temp - 0.1
            hollo_tip_height = hollow_temp / math.tan(math.pi / 12)
            points = [
                (tip_center_x - hollow_temp, tip_center_y),
                (tip_center_x, tip_center_y + hollo_tip_height),
                (tip_center_x + hollow_temp, tip_center_y),
            ]
            if is_AFM:
                connector.add(Points2Shape(points))

            # Text
            connector.add("11 layer")
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
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
                    x_beam - w_support / 2 - 10,
                    electrode_y_3,
                    center_start_x_2 - center_start_x_1 + w_cable + 20,
                    electrode_y_1 - electrode_y_3,
                    0,
                ),
            )
            # pad
            connector.add("20 layer")
            x_start = [
                center_start_x_1 + cable_offset - L_electrode,
                center_start_x_2 - cable_offset,
                center_start_x_3 + w_cable / 2 - L_electrode,
                center_start_x_4 - w_cable / 2,
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
            # frame of lithography (beam part)
            connector.add(
                (
                    RectangleLH(
                        x_beam - w_support / 2 - 5,
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

    # Alignment Marks
    # connector.add("11 layer")
    # connector.add(AlignCustC1(-350, -3150, 100, 2, 100, 0, 120, 120, 0))
    # connector.add(AlignCustC1(7000, -3150, 100, 2, 100, 0, 120, 120, 0))
    return result


# Test
if __name__ == "__main__":
    gen = CNSTGenerator(shapeReso=0.01)
    connector = Structure("Tunable")
    # top left
    position_1 = optical_thermal(connector, 0, 0, "A", True)
    print(position_1)
    # buttom left
    position_3 = optical_thermal(connector, 0, -3000, "B", False)
    print(position_3)
    gen.add(connector)
    gen.generate(
        "result_wei/tunable_device/optical/optical_thermal/optical_thermal.cnst",
        "result_wei/tunable_device/optical/optical_thermal/optical_thermal.gds",
        show=True,
    )
