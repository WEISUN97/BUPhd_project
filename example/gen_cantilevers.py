from cnst_gen import CNSTGenerator
from geo import Waveguide, Structure, RectangleLH, ExponentialTaper, Geo, TextOutline
import numpy as np

DY = 100
WE = 1.5
X_SPAN = 20
LAYER_A = 20 # outside layer
LAYER_B = 30 # core layer get final: A-B
RADIUS = 5
class Cantilever(Geo):
    def __init__(self, x: float, y: float, w: float, l: float, w2: float, l2: float) -> None:
        """
        Initialize a Cantilever object.

        Args:
            x (float): The x-coordinate of the Cantilever's position.
            y (float): The y-coordinate of the Cantilever's position.
            w (float): The width of the Cantilever.
            l (float): The length of the Cantilever.
            w2 (float): The width of the tapering region.
            l2 (float): The length of the tapering region.

        Returns:
            None
        """
        self.draw = ''
        self.add((
            ExponentialTaper(x+l2, y+w2/2, l2, w, w2, 50, 180),
            RectangleLH(x+l2, y+w2/2-w/2, l, w, 0),
            ExponentialTaper(x+l2+l, y+w2/2, l2, w, w2, 50, 0)
        ))
        
class CantileverInverse(Geo):
    def __init__(self, x:float,y:float,w: float, l: float, w2: float, l2: float, offset: float, layerA:int, layerB:int) -> None:
        self.draw = ''
        self.add(f'{layerB} layer')
        self.add(Cantilever(x+offset, y+offset,w,l,w2,l2))
        self.add(f'{layerA} layer')
        self.add(RectangleLH(x, y, l+2*l2+2*offset, w2+2*offset, 0))
can_inv = Structure('Cantilever')

t_values = np.array(range(10,100,10))*1e-3
ratio_values = [1000, 5e3, 1e4, 7e3]
ratio_values = np.sort(ratio_values)[::-1]

x=0
max_l = 0
for t in t_values:
    x += max_l+10
    max_l = t*max(ratio_values)
    for i, ratio in enumerate(ratio_values):
        can_inv.add((
            CantileverInverse(x=x, y=i*20, w=t, l=t*ratio, w2=2, l2=2,
                              offset=1,layerA=LAYER_A,layerB=LAYER_B),
            TextOutline(f'L/t{ratio/1e3:.0f}k','Calibri',10,x,i*20+5)
        ))
    can_inv.add(TextOutline(f't{t*1e3:.0f}','Calibri',20,x,-25))
gen = CNSTGenerator(shapeReso=0.1)
gen.add(can_inv)

gen.generate(r'result\cantilever.cnst', r'result\cantilever.gds', show=True)
        