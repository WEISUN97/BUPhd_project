import sys

sys.path.append("/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython")

import graphic_recognition as gr
from cnst_gen import CNSTGenerator
from geo import PolyPath, Structure, ellipseVector

connector = Structure("Tunable")
connector.add("10 layer")
result = gr.contours
# print(result)
for i in range(len(result)):
    line = result[i]
    for j in range(len(line)):
        print(line)
        line[j] = (line[j][0], line[j][1])
    print(line)
    connector.add(
        (PolyPath(line, 0.5, 1, 1),),
    )
gen = CNSTGenerator(shapeReso=0.01)
gen.add(connector)
gen.generate(
    "result_wei/others/Test/test.cnst",
    "result_wei/others/Test/test.gds",
    show=True,
)
