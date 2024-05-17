from .geo import Geo

class tJunction(Geo):
    def __init__(self, x: float, y: float, w1: float, w2: float, L1:float, L2:float, r=0, N=0, theta=0):
        self.draw = f"""
            {x} {y} {w1} {w2} {L1} {L2} {r} {N} {theta} tJunction
        """

class hJunction(Geo):
    def __init__(self, x: float, y: float, w1: float, w2: float, L1:float, L2:float, r=0, N=0, theta=0):
        self.draw = f"""
            {x} {y} {w1} {w2} {L1} {L2} {r} {N} {theta} hJunction
        """