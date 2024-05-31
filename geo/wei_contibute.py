from geo.xiangyu_contribute import *
from .geo import Geo
from geo import *
from numpy import *
from typing import Literal


class tJunction(Geo):
    def __init__(
        self,
        x: float,
        y: float,
        w1: float,
        w2: float,
        L1: float,
        L2: float,
        r=0,
        N=0,
        theta=0,
    ):
        self.draw = f"""
            {x} {y} {w1} {w2} {L1} {L2} {r} {N} {theta} tJunction
        """


class hJunction(Geo):
    def __init__(
        self,
        x: float,
        y: float,
        w1: float,
        w2: float,
        L1: float,
        L2: float,
        r=0,
        N=0,
        theta=0,
    ):
        self.draw = f"""
            {x} {y} {w1} {w2} {L1} {L2} {r} {N} {theta} hJunction
        """


class roundedCorners(Geo):
    def __init__(self, x: float, y: float, r: float, theta=180, N=10):
        self.draw = ""
        theta1 = theta / 180 * pi
        theta2 = theta1 + pi / 2
        p1 = [(x + r * cos(theta1), y + r * sin(theta1))]
        p2 = [(x + r * cos(theta2), y + r * sin(theta2))]
        p3 = [
            (
                x + sqrt(2) * r * cos(theta1 + pi / 4),
                y + sqrt(2) * r * sin(theta1 + pi / 4),
            )
        ]
        arcPointsTheta = linspace(theta1, theta2, N + 2)[1:-1]
        arcPoints = []
        for i in range(len(arcPointsTheta)):
            x_n = x + r * cos(arcPointsTheta[i])
            y_n = y + r * sin(arcPointsTheta[i])
            arcPoints += [(x_n, y_n)]
        self.add(Points2Shape(p1 + arcPoints + p2 + p3))


class rectSUshape(Geo):
    def __init__(
        self,
        x: float,
        y: float,
        L1: float,
        L2: float,
        L3: float,
        W=0,
        theta=0,
    ):
        self.draw = f"""
            {x} {y} {L1} {L2} {L3} {W} {theta} rectSUshape
        """


class multyTextOutline(Geo):
    def __init__(
        self,
        text: list[str],
        font_name: str,
        font_size: float,
        spacing: float,
        x: float,
        y: float,
    ):
        self.draw = ""
        for i in range(len(text)):
            self.add(TextOutline(text[i], font_name, font_size, x, y - i * spacing))


class Boolean(Geo):
    def __init__(
        self,
        layer_1: float,
        layer_2: float,
        layer_3: float,
        operation: str,
    ):
        self.draw = f"""
            genArea1 devices {layer_1} genArea\n
            genArea2 devices {layer_2} genArea\n
            genArea1 genArea2 {layer_3} subtract {operation}
        """


class roundrect(Geo):
    def __init__(
        self,
        x: float,
        y: float,
        l: float,
        h: float,
        r_x: float,
        r_y: float,
        theta: float,
    ):
        self.draw = f"""
            {x} {y} {l} {h} {r_x} {r_y} {theta} roundrect
        """


class sBend(Geo):
    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        w: float,
        theta: float,
    ):
        self.draw = f"""
            <{x1} {y1} {x2} {y2} {w} {theta} sBend>
        """


class slash(Geo):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, w: float):
        self.draw = ""
        p1 = [(x1 - w / 2, y1)]
        p2 = [(x1 + w / 2, y1)]
        p3 = [(x2 + w / 2, y2)]
        p4 = [(x2 - w / 2, y2)]
        self.add(Points2Shape(p1 + p2 + p3 + p4))


class sBendLH(Geo):
    def __init__(
        self,
        x1: float,
        y1: float,
        L: float,
        H: float,
        w: float,
        theta: float,
    ):
        self.draw = f"""
            {x1} {y1} {L} {H} {w} {theta} sBendLH
        """


class circlethree(Geo):
    def __init__(
        self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, N: float
    ):
        self.draw = f"""
        {x1} {y1} {x2} {y2} {x3} {y3} {N} circlethree
    """


class rectTaper(Geo):
    def __init__(
        self,
        x: float,
        y: float,
        w1: float,
        L1: float,
        w2: float,
        L2: float,
        theta: float,
    ):
        self.draw = f"""
       {x} {y} {w1} {L1} {w2} {L2} {theta} rectTaper 
    """


class comb(Geo):
    def __init__(
        self,
        x: float,
        y: float,
        L1: float,
        w1: float,
        L2: float,
        w2: float,
        d: float,
        s: float,
        N: int,
        theta: float,
    ):
        self.draw = ""
        # substrate of comb
        self.add(RectangleLH(x, y, L1, w1, theta))
        theta_pi = theta / 180 * pi
        # comb teeth
        for i in range(N):
            # before rotation
            x2 = x + d + (s + w2) * i
            y2 = y + w1
            # after rotation
            x3 = (x2 - x) * cos(theta_pi) - (y2 - y) * sin(theta_pi) + x
            # print(x3)
            y3 = (x2 - x) * sin(theta_pi) + (y2 - y) * cos(theta_pi) + y
            self.add(RectangleLH(x3, y3, w2, L2, theta))


# class spring(Geo):
#     def __init__(
#         self,
#         # (x, y) pos of left shuttle
#         x: float,
#         y: float,
#         L: float,
#         w: float,
#     ):
#         self.draw = ""
#         # shuttles of springs
#         self.add(RectangleLH(x, y, 0.22, 29, 0))
#         self.add(RectangleLH(x, y, 1, 1, 0))
#         self.add(RectangleLH(x, y, 1, 1, 0))


#         # anchors of springs

#         # folding truss of springs
