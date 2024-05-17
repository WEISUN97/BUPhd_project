from cnst_gen import CNSTGenerator
from geo import RectangleLH, Structure


connector = Structure('Connector')
for i in range(10):
    connector.add((
        RectangleLH(0, 0, 10, 0.1, 0)
    ))

gen = CNSTGenerator(shapeReso=0.1)
gen.add(connector)
gen.generate('result_wei/XXX.cnst', 'result_wei/XXX.gds', show=True)