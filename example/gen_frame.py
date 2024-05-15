from cnst_gen import CNSTGenerator

from geo import RectangleLH, Structure, InstanceSym, ArrayRect

frame_box = Structure('Frame_box')
# draw a 3*3 frame, each frame is 10000*10000, frame width is 300

frame_box.add((
    RectangleLH(0,0,10000,300,0),
    RectangleLH(0,0,300,10000,0),
    RectangleLH(0,9700,10000,300,0),
    RectangleLH(9700,0,300,10000,0),
))

frame = Structure('Frame')

frame.add(
    ArrayRect('Frame_box', x=0, y=0, col=3, row=3, dx=10000, dy=10000, type=1)
)
top = Structure('Top')
top.add(
    InstanceSym('Frame', 0,0, 0,0,3e4,3e4,'N', 1, 0)
)

gen = CNSTGenerator()
gen.add(frame_box)
gen.add(frame)
gen.add(top)
gen.generate(r'result\frame.cnst', r'result\frame.gds', show=True)