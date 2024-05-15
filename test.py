from cnst_gen import CNSTGenerator
from geo import BendWaveguide, Structure, RectangleC



points = [
    (0,0),
    (100,0),
    (100,-100),
    (200,-100)
]


bd=BendWaveguide(
    points, r=10,w=1
)


generator = CNSTGenerator()
generator.add('<Bendw struct>')
generator.add(bd)
generator.generate(r'result\bend_waveguide.cnst', r'result\bend_waveguide.gds', show=True)