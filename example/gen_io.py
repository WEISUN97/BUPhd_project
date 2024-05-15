from cnst_gen import CNSTGenerator
from geo import TaperInverse, TaperIOInverse, Structure, ArrayRect, Instance, LabelMakerAutoOutline
import numpy as np
WIDTH = 0.43
DY = 100
NROWS = int(8000/DY)
FONT_SIZE = 20
generator = CNSTGenerator()
edge_coupler = Structure('EdgeCoupler')
taper = TaperIOInverse(
    w1=0.1,
    w2=WIDTH,
    l1=1500,
    l2=500,
    l3=500,
    we=1.5)
edge_coupler.add(taper)

taper_array = Structure('TArray')
taper_array.add((
    ArrayRect('EdgeCoupler', x=0, y=0, col=0,row=NROWS, dx=0, dy=DY, type=1)
))

io = Structure('IO')
io.add((
    Instance('TArray', 1e3,1e3,'N',1,0),
    Instance('TArray', 9e3,1e3,'Y',1,0),
))
text_array = Structure('TextArray', shapeReso=1)
text_array.add((
    LabelMakerAutoOutline(
        row=NROWS,col=0,font_name='Calibri', font_size=30, x=0, y=0,
        xr=0, yr=0, dx=0, dy=-DY, type='autoOutLett'
    ),
))
generator.add('2 layer')
generator.add(edge_coupler)
generator.add(taper_array)
generator.add(io)
generator.add(text_array)

generator.generate(r'result\io.cnst', r'result\io.gds', show=True)
