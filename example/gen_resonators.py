from cnst_gen import CNSTGenerator
from geo import WaveguideInverse, Structure, RingResonatorInverse, TextOutline, RectangleC
import numpy as np

DY = 100
WE = 1.5
X_SPAN = 20
LAYER_A = 20 # outside layer
LAYER_B = 30 # core layer get final: A-B
RADIUS = 5
resonatorLayout = Structure('resonators')
gap_values = np.array([70,100,160,270])*1e-3
for i, gap in enumerate(gap_values):
    resonator = RingResonatorInverse(
        x=0, y=i*DY, r=RADIUS, w=0.43, x_span=X_SPAN, lc=3, gap=gap, n_seg=100, we=WE, layerA=20, layerB=30
    )
    waveguide = WaveguideInverse(X_SPAN, i*DY, 0.43, 30, WE, 0)
    label = TextOutline(f'g:{gap*1e3:.0f}nm', 'Calibri', font_size=2*RADIUS, x=X_SPAN+3, y=i*DY+5)
    resonatorLayout.add((resonator, waveguide, label))

gap_values = np.array([160,270])*1e-3
can_gap_values = np.concatenate((np.linspace(60,63,4), np.linspace(30,33,4)))*1e-3
resonator_with_caltileverLayout = Structure('resonator_with_caltilever')
structures = []
for i, gap in enumerate(gap_values):
    struct = Structure(f'gap{gap*1e3:.0f}nm')
    for j, can_gap in enumerate(can_gap_values):
        y = DY*(len(can_gap_values)*i+j)
        resonator = RingResonatorInverse(
            x=0, y=y, r=RADIUS, w=0.43, x_span=X_SPAN, lc=3, gap=gap, n_seg=100, we=WE, layerA=20, layerB=30
        )
        x_center = resonator.info['x_center']
        y_center = resonator.info['y_center']
        cantilever = RectangleC(x_center, y_center+RADIUS+gap+0.43/2+0.16/2, 3, 0.16, 0)
        waveguide = WaveguideInverse(X_SPAN, y, 0.43, 30, WE, 0)
        label = TextOutline(f'g:{gap*1e3:.0f}nm', 'Calibri', font_size=RADIUS*2, x=X_SPAN+3, y=y+5)
        label2 = TextOutline(f'c:{can_gap*1e3:.0f}nm', 'Calibri', font_size=RADIUS*2, x=X_SPAN+3, y=y+2+RADIUS*2)
        struct.add((
            resonator, 
            waveguide,
            f'{LAYER_B} layer',
            cantilever,
            f'{LAYER_A} layer', 
            label,
            label2))
    structures.append(struct)


gen = CNSTGenerator(shapeReso=.1)
gen.add(resonatorLayout)
for struct in structures:
    gen.add(struct)
gen.generate(r'result\resonators.cnst', r'result\resonators.gds', show=True)
