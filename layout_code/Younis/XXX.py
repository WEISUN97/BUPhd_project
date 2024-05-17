import sys
sys.path.append('/Users/bubble/Desktop/PyProjects/layout/Xiangyu2Wei/CNSTPython')

from cnst_gen import CNSTGenerator 
from geo import tJunction, Structure


connector = Structure('Connector')
for i in range(1):
    connector.add((
        tJunction(0, 0, 10, 0.1, 20, 100),
    ))

gen = CNSTGenerator(shapeReso=0.1)
gen.add(connector)
gen.generate('result_wei/XXX.cnst', 'result_wei/XXX.gds', show=True)