from cnst_gen import CNSTGenerator
from geo import DiskResonatorInv, Structure, TextOutline
import numpy as np

disk = Structure('DiskResonator')

radius_values = np.linspace(4,6,3)
gap_values = np.linspace(60,170,5)*1e-3

for i, radius in enumerate(radius_values):
    for j, gap in enumerate(gap_values):
        y = (i*len(gap_values) + j)*1e3
        disk.add((
            DiskResonatorInv(
                x=0,
                y=y,
                r=5,
                w=0.43,
                we=1.5,
                x_span=3e3,
                gap=100e-3,
                layerA=20,
                layerB=30,
                shapeReso=0.001
            ),
            '0.1 shapeReso',
            TextOutline(
                x=1.5e3+10,
                y=y+5,
                text=f'R:{radius:.0f}um G:{gap*1e3:.1f}nm',
                font_name='Calibri',
                font_size=10,
            )
        ))

generator = CNSTGenerator()
generator.add(disk)
generator.generate(r'result\disk_resonator.cnst', r'result\disk_resonator.gds', show=True)
