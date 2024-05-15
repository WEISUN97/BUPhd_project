from cnst_gen import CNSTGenerator
from geo import Waveguide, FourBandWaveguide, Structure
generator = CNSTGenerator(shapeReso=0.001)
generator.add('20 layer')
n = 80
x1 = 0
y1 = 0
x2=20
y2=0
x3=20
y3=-20
x4=280
y4=-20
generator.add(Structure('Connector'))
for i in range(n):
    y1 += 30
    x2 += 3
    y2 = y1
    x3 = x2
    y3 += 3
    y4 = y3
    four_band = FourBandWaveguide(
        x1=x1, y1=y1, 
        x2=x2, y2=y2,
        x3=x3, y3=y3,
        x4=x4, y4=y4,
        r=10, w=0.43
    )
    generator.add(four_band)

generator.generate(r'result\waveguide_test.cnst',r'result\waveguide_test.gds',show=True)