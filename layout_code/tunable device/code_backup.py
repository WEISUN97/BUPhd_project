# for i in range(2):
#     connector.add(
#         (
#             # left
#             rectTaper(
#                 x_beam - w_support / 2,
#                 y_beam - j * 1200,
#                 L_electrode_1,
#                 0,
#                 L_electrode_2,
#                 300,
#                 180,
#             ),
#             # right
#             rectTaper(
#                 x_beam + w_support / 2 * 3 + L_beam,
#                 y_beam - j * 1200,
#                 L_electrode_1,
#                 0,
#                 L_electrode_2,
#                 300,
#                 0,
#             ),
#             # top
#             rectTaper(
#                 x_beam + w_support / 2 + L_beam / 2,
#                 y_beam
#                 - j * 1200
#                 + (L_support + w_beam) / 2
#                 + gap_actuators_y
#                 + L_1
#                 + L_2
#                 + h_actuators,
#                 300,
#                 0,
#                 L_electrode_2,
#                 300,
#                 90,
#             ),
#             # bottom
#             rectTaper(
#                 x_beam + w_support / 2 + L_beam / 2,
#                 y_beam
#                 - j * 1200
#                 + (L_support - w_beam) / 2
#                 - gap_actuators_y
#                 - L_1
#                 - L_2
#                 - h_actuators,
#                 L_electrode_1,
#                 0,
#                 L_electrode_2,
#                 L_electrode_2,
#                 -90,
#             ),
#         )
#     )
