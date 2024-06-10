import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

import graphic_recognition as gr
from cnst_gen import CNSTGenerator
from geo import PolyPath, Structure, ellipseVector

connector = Structure("Tunable")
connector.add("10 layer")
result = gr.points
# print(result)
for i in range(len(result)):
    point = result[i]
    x = point[0]
    y = point[1]
    connector.add((ellipseVector(x, y, 0.5, 0.5, 0),))
# connector.add(
#     (
#         # def support
#         # PolyPath([(0, 0), (0, 10), (10, 10), (10, 0)], 0.5, 1, 1),
#         ellipseVector(5, 5, 1, 1, 0),
#     ),
# )
gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.generate(
    "result_wei/others/Test/test1.cnst",
    "result_wei/others/Test/test1.gds",
    show=True,
)
