from cnst_gen import CNSTGenerator
from geo import TextOutline, Structure




connector = Structure('Connector')
for i in range(10):
    connector.add((
        TextOutline('hahahaha', 'Times New Roman', 10, 10*i, 10*i)
    ))

gen = CNSTGenerator(shapeReso=0.1)
gen.add(connector)
gen.generate('result_wei/connector123.cnst', 'result_wei/connector123.gds', show=True)