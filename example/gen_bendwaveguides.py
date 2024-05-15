from cnst_gen import CNSTGenerator
from geo import BendWaveguide, Structure
import numpy as np

generator = CNSTGenerator(shapeReso=1e-3)
struct = Structure('BendWaveguide')

for i in range(8):
    points = [
        (0,-100-100*i),
        (80+i*3,-100-100*i),
        (80+i*3,-3-i*3),
        (3e3-80-i*3,-3-i*3),
        (3e3-80-i*3,-100-100*i),
        (3e3,-100-100*i)
    ]
    points = [(x, y+800) for x, y in points]
    struct.add(BendWaveguide(points,45,0.43,1.5))
for i in range(8):
    points = [
        (0,0+100*i),
        (3000,0+100*i)
    ]
    points = [(x, y+800) for x, y in points]
    struct.add(BendWaveguide(points,45,0.43,1.5))

generator.add('2 layer')
generator.add(struct)
generator.generate(r'result\bend_waveguide.cnst', r'result\bend_waveguide.gds', show=True)