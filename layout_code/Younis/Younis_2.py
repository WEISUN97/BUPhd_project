import sys

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
    Boolean,
    Structure,
)

connector = Structure("beam")
for m in range(2):
    for k in range(3):
        # m = 0
        # k = 0
        r = 0.5  # round corner of beam
        w_cable = 2
        r_cable = 10
        w_support = 10
        L_support = 10
        w_beam = 0.2
        L_beam = 10 + k * 5
        gap_1 = 10  # gap between electrodes and beams
        gap_2 = 50  # gap between electrodes in y direction
        gap_3 = 20  # gap between electrodes in x direction
        gap_cell_x = 850  # gap between cells in x direction
        gap_actuators_x = 0.25  # gap between actuators
        gap_actuators_y = 0.2  # gap between actuators and beams
        L_actuators = [
            [3 + k * 2.5, 3 + k * 3, 3],
            [3 + k * 2.5, 3 + k * 2.5, 3],
            [3 + k * 2.5, 3, 3 + k * 2.5],
            [3 + k * 2.5, 3, 3 + k * 2.5],
            [7 + k * 2.5, 4 + k * 2.5, 7 + k * 2.5],
            [7 + k * 2.5, 4 + k * 2.5, 7 + k * 2.5],
            [4.75 + k * 2.5, 4.75 + k * 2.5],
        ]
        h_actuators = 3
        L_electrode = 350
        x_beam = (
            k * gap_cell_x + gap_1 + L_electrode + w_support / 2 + 3 * m * gap_cell_x
        )
        y_beam = -L_support

        for i in range(7):
            # beams and supports
            if i != 2 and i != 3:
                connector.add(
                    (
                        tJunction(
                            x_beam,
                            y_beam - i * 850,
                            w_support,
                            w_beam,
                            L_support,
                            L_beam,
                        ),
                        roundedCorners(
                            x_beam + w_support / 2 + r,
                            y_beam + (L_support + w_beam) / 2 + r - i * 850,
                            r,
                            180,
                        ),
                        roundedCorners(
                            x_beam + w_support / 2 + r,
                            y_beam + (L_support - w_beam) / 2 - r - i * 850,
                            r,
                            90,
                        ),
                    ),
                )
            else:
                connector.add(
                    (
                        hJunction(
                            x_beam,
                            y_beam - i * 850,
                            w_support,
                            w_beam,
                            L_support,
                            L_beam,
                        ),
                        roundedCorners(
                            x_beam + w_support / 2 + r,
                            y_beam + (L_support + w_beam) / 2 + r - i * 850,
                            r,
                            180,
                        ),
                        roundedCorners(
                            x_beam + w_support / 2 + r,
                            y_beam + (L_support - w_beam) / 2 - r - i * 850,
                            r,
                            90,
                        ),
                        roundedCorners(
                            x_beam + w_support / 2 + L_beam - r,
                            y_beam + (L_support + w_beam) / 2 + r - i * 850,
                            r,
                            270,
                        ),
                        roundedCorners(
                            x_beam + w_support / 2 + L_beam - r,
                            y_beam + (L_support - w_beam) / 2 - r - i * 850,
                            r,
                            0,
                        ),
                    ),
                )
            connector.add(
                (
                    tJunction(
                        x_beam, y_beam - i * 850, w_support, w_beam, L_support, L_beam
                    ),
                    roundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support + w_beam) / 2 + r - i * 850,
                        r,
                        180,
                    ),
                    roundedCorners(
                        x_beam + w_support / 2 + r,
                        y_beam + (L_support - w_beam) / 2 - r,
                        r,
                        90,
                    ),
                ),
            )
        # electrodes
        for j in range(7):
            for i in range(2):
                for p in range(2):
                    connector.add(
                        RectangleLH(
                            x_beam
                            + w_support / 2
                            - L_electrode
                            + p * (L_electrode + gap_3)
                            + gap_actuators_x
                            + L_actuators[j][0],
                            y_beam
                            + L_support / 2
                            + gap_2 / 2
                            - i * (gap_2 + L_electrode)
                            - j * 850,
                            L_electrode,
                            L_electrode,
                            0,
                        ),
                    )
        # actuators
        for j in range(7):
            L_actuators_j = L_actuators[j]
            if j < 4 or j == 6:
                gap_actuators_x_temp = gap_actuators_x
                for i in range(len(L_actuators_j)):
                    if i > 0:
                        gap_actuators_x_temp += L_actuators_j[i - 1] + gap_actuators_x
                    connector.add(
                        roundrect(
                            x_beam + w_support / 2 + gap_actuators_x_temp,
                            y_beam
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - h_actuators
                            - j * 850,
                            L_actuators_j[i],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                    )
            elif j == 4 or j == 5:
                gap_temp = (
                    L_beam
                    + gap_actuators_y
                    + h_actuators / 2
                    - L_actuators_j[0]
                    - gap_actuators_x
                    - L_actuators_j[1],
                )[0]
                connector.add(
                    (
                        roundrect(
                            x_beam + w_support / 2 + gap_actuators_x,
                            y_beam
                            + (L_support - w_beam) / 2
                            - gap_actuators_y
                            - h_actuators
                            - j * 850,
                            L_actuators_j[0],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                        roundrect(
                            x_beam + w_support / 2 + gap_actuators_x,
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            - j * 850,
                            L_actuators_j[2],
                            h_actuators,
                            0.5,
                            0.5,
                            0,
                        ),
                        rectSUshape(
                            x_beam
                            + w_support / 2
                            + gap_actuators_x
                            + L_actuators_j[0]
                            + gap_temp,
                            y_beam
                            + (L_support + w_beam) / 2
                            + gap_actuators_y
                            + h_actuators / 2
                            - j * 850,
                            L_actuators_j[1],
                            2 * gap_actuators_y + h_actuators + w_beam,
                            -L_actuators_j[1],
                            h_actuators,
                            -90,
                        ),
                    )
                )

        # cables
        for j in range(7):
            # cables of beam
            center_start_x = x_beam
            center_start_y = y_beam + L_support - j * 850
            electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
            point = [
                (center_start_x, center_start_y),
                (center_start_x, electrode_y),
            ]
            connector.add((BendWaveguide(point, r_cable, w_cable),))
            L_actuators_j = L_actuators[j]
            gap_actuators_x_temp = gap_actuators_x
            for i in range(2):
                if i > 0:
                    gap_actuators_x_temp += +L_actuators_j[i - 1] + gap_actuators_x
                center_start_x = (
                    x_beam + w_support / 2 + gap_actuators_x_temp + L_actuators_j[i] / 2
                )
                center_start_y = (
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators
                    - j * 850
                )
                electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, electrode_y),
                ]
                if i == 0:
                    if j == 2 or j == 3:
                        p2_y = center_start_y - 12
                        p3_x = center_start_x - w_support - 15
                        electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850
                        electrode_x = p3_x
                        point = [
                            (center_start_x, center_start_y),
                            (center_start_x, p2_y),
                            (p3_x, p2_y),
                            (electrode_x, electrode_y),
                        ]
                        connector.add((BendWaveguide(point, r_cable, w_cable),))
                    else:
                        connector.add((BendWaveguide(point, r_cable, w_cable),))

                if i > 0:
                    electrode_y = (
                        y_beam + L_support / 2 - gap_2 / 2 - j * 850 - w_cable / 2
                    )
                    electrode_x = (
                        x_beam
                        + w_support / 2
                        - L_electrode
                        + (L_electrode + gap_3)
                        + gap_actuators_x
                        + L_actuators[j][0],
                    )[0]
                    point = [
                        (center_start_x, center_start_y),
                        (center_start_x, electrode_y),
                        (electrode_x, electrode_y),
                    ]
                    electrode_x = center_start_x + gap_3
                    electrode_y = y_beam + L_support / 2 - gap_2 / 2 - j * 850
                    # connector.add(
                    #     (
                    #         slash(
                    #             center_start_x,
                    #             center_start_y,
                    #             electrode_x,
                    #             electrode_y,
                    #             w_cable,
                    #         ),
                    #     )
                    # )
                    if j != 2 and j != 3:
                        x2 = center_start_x + (center_start_y - electrode_y)
                        y2 = center_start_y + (electrode_x - center_start_x)
                        connector.add(
                            (
                                sBend(
                                    center_start_x,
                                    center_start_y,
                                    x2,
                                    y2,
                                    w_cable,
                                    -90,
                                ),
                            )
                        )
                    else:
                        connector.add((BendWaveguide(point, r_cable, w_cable),))

            # third cable of 0/1 beam
            if j == 0 or j == 1:
                L_temp = (
                    gap_actuators_x * 3
                    + L_actuators_j[0]
                    + L_actuators_j[1]
                    + L_actuators_j[-1]
                )
                center_start_x = x_beam + w_support / 2 + L_temp
                center_start_y = (
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators / 2
                    - j * 850
                )
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
                electrode_x = center_start_x + gap_3
                point = [
                    (center_start_x, center_start_y),
                    (electrode_x, center_start_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable),))
            # third cable of 2/3 beam
            if j == 2 or j == 3:
                center_start_x = (
                    x_beam
                    + w_support / 2
                    + 2.5 * L_actuators_j[0]
                    + 3 * gap_actuators_x
                )
                center_start_y = (
                    y_beam
                    + (L_support - w_beam) / 2
                    - gap_actuators_y
                    - h_actuators
                    - j * 850
                )
                p2_y = center_start_y - 12
                p3_x = center_start_x + w_support + 30
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
                electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable),))
            if j == 4 or j == 5:
                center_start_x = (
                    x_beam + w_support / 2 + L_actuators_j[0] / 2 + gap_actuators_x
                )
                center_start_y = (
                    y_beam
                    + (L_support + w_beam) / 2
                    + gap_actuators_y
                    + h_actuators
                    - j * 850
                )
                p2_y = center_start_y + 10
                p3_x = center_start_x + gap_3 + 15
                electrode_y = y_beam + L_support / 2 + gap_2 / 2 - j * 850
                electrode_x = p3_x
                point = [
                    (center_start_x, center_start_y),
                    (center_start_x, p2_y),
                    (p3_x, p2_y),
                    (electrode_x, electrode_y),
                ]
                connector.add((BendWaveguide(point, r_cable, w_cable),))
        # # Text
        for j in range(7):
            fontSize = 25
            spacing = 25
            x_text = x_beam + w_support / 2 + L_beam + 60
            y_text = y_beam + L_support / 2 - j * 850 - fontSize / 2
            text = [
                f"No.{k+1}.{j+1}.{m+1} L={L_beam} t={w_beam} L/t={L_beam/w_beam}",
            ]
            connector.add(
                (
                    multyTextOutline(
                        text, "Times New Roman", fontSize, spacing, x_text, y_text
                    )
                )
            )
gen = CNSTGenerator(shapeReso=0.01)
gen.add("2 layer")
gen.add(connector)
gen.generate("result_wei/Younis.cnst", "result_wei/Younis.gds", show=True)
