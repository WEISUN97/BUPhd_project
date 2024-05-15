from cnst_gen import CNSTGenerator
from geo import GratingCouplerWaveguide, Structure, TextOutline

grating = Structure('GratingCoupler')

grating.add(
    GratingCouplerWaveguide(
        x=0,y=0,w=0.43, l=0, 
        we=1.5, lambda_0=1.55, neff=2.68, nc=1, theta_c=20, 
        r=100, g_p=0.66, ratio=0.5, ng=70, ns=50, layer_waveguide=2, layer_grating=3, theta=0
    )
)

generator = CNSTGenerator(shapeReso=0.1)
generator.add(grating)
generator.generate(r'result\grating_coupler.cnst', r'result\grating_coupler.gds', show=True)