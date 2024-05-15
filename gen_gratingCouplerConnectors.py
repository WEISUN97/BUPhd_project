from cnst_gen import CNSTGenerator
from geo import BendWaveguideInv, Structure

n = 80# number of periods
DY = 100
R = 20
connector_distance = 500


connector = Structure('Connector')
for i in range(n):
    line1 = [
        (0, i*DY),
        (-30-3*i, i*DY),
        (-30-3*i, -300),
    ]
    line2 = [
        (connector_distance, i*DY),
        (connector_distance+30+3*i, i*DY),
        (connector_distance+30+3*i, -50-3*i),
        (-30+3*(i+1), -50-3*i),
        (-30+3*(i+1), -300),
    ]
    connector.add((
        BendWaveguideInv(line1, R, 0.43, 1.5),
        BendWaveguideInv(line2, R, 0.43, 1.5),
    ))

gen = CNSTGenerator(shapeReso=0.1)
gen.add(connector)
gen.generate('result\connector.cnst', 'result\connector.gds', show=True)