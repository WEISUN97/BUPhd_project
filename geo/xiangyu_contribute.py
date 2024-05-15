from enum import Enum

import numpy as np
from .geo import Geo


class TaperIOInverse(Geo):
    def __init__(self, w1, w2, l1, l2, l3, we):
        self.draw = ''
        self.add(WaveguideInverse(0, 0, w1, l1, we, 0))
        self.add(TaperInverse(l1, 0, w1, w2, l2, we))
        self.add(WaveguideInverse(l1+l2, 0, w2, l3, we, 0))


class TaperIO(Geo):
    def __init__(self, w1, w2, l1, l2, l3, name):
        self.draw = f'<{name} struct>'
        self.add(Waveguide(0, 0, w1, l1))
        self.add(Taper(l1, 0, w1, w2, l2))
        self.add(Waveguide(l1+l2, 0, w2, l3))


class WaveguideInverse(Geo):
    def __init__(self, x, y, w, l, we, theta):
        self.draw = f"""
            <{x} {y} {x+l} {y} {w} {we} {theta} 0 0 waveguideInv>
        """


class TaperInverse(Geo):
    def __init__(self, x, y, w1, w2, l, we):
        self.draw = f"""
            <{x} {y} {x+l} {y} {w1+2*we} {w2+2*we} {w1} {w2} 0 linearTaperSlot>
            """


class Waveguide(Geo):
    def __init__(self, x, y, w, l, theta=0):
        self.draw = f"""
            <{x} {y} {x+l} {y} {w} {theta} 0 0 waveguide>
        """


class Taper(Geo):
    def __init__(self, x, y, w1, w2, l):
        self.draw = f"""
            <{x} {y} {x+l} {y} {w1} {w2} 0 linearTaper>
        """


class TaperIOArray(Geo):
    def __init__(self, taperio: TaperIO, n: int, dy: float):
        self.draw = ''
        self.add(taperio)
        self.draw += f"""
            <TaperIOArray struct>
            <TaperIO 0 0 1 {n} 1 {dy} 1 arrayRect>
        """


class ArrayRect(Geo):
    """
    See 2.4.1 Page 49.
    The method instantiates and arrays a GDS structure on a periodic rectangular grid. 
    2 constructors are available. Both define the starting point of the array (x,y) 
    along with the number of columns (Ncolumns) and rows (Nrows).

    : param dx: dx>0 to right, dx<0 to left
    : param dy: dy>0 to up, dy<0 to down
    : param type: 1 or 2
        if type = 1, the array is defined by the starting point (x,y) and the step size (dx,dy)
        if type = 2, the array is defined by the starting point (x,y) and the ending point (col,row)
    """

    def __init__(self, struct_name, x, y, col, row, dx, dy, type: int):
        if type not in [1, 2]:
            raise ValueError("Invalid type value. Type can only be 1 or 2.")
        self.draw = f"""
            <{struct_name} {x} {y} {col} {row} {dx} {dy} {type} arrayRect>
        """


class Structure(Geo):
    def __init__(self, struct_name: str, shapeReso=None):
        self.draw = f'<{struct_name} struct>\n'
        if shapeReso is not None:
            self.draw += f'{shapeReso} shapeReso\n'


class Instance(Geo):
    def __init__(self, struct_name: str, x: float, y: float, MIR: str, MAG: float, theta: float):
        self.draw = f"""
            <{struct_name} {x} {y} {MIR} {MAG} {theta} instance>
        """


class SBand(Geo):
    def __init__(self, x1, y1, x2, y2, w, theta):
        self.draw = f"< {x1} {y1} {x2} {y2} {w} {theta} sBend>\n"


class LabelMakerAuto(Geo):
    def __init__(self, row: int, col: int, font_name: str, font_size: int, x: float, y: float, xr: float, yr: float, dx: float, dy: float, type: str):
        self.draw = f"""
            {{{row}\t{col}\t{font_name}\t{font_size}\t{x}\t{y}\t{xr}\t{yr}\t{dx}\t{dy}\t{type}\tlabelMaker}}
        """


class LabelMaker(Geo):
    def __init__(self, labels: list, row: int, col: int, font_name: str, font_size: int, x: float, y: float, xr: float, yr: float, dx: float, dy: float, type: str):
        labels = '\t'.join(labels)
        self.draw = f"""
            {{{labels}\t{row}\t{col}\t{font_name}\t{font_size}\t{x}\t{y}\t{xr}\t{yr}\t{dx}\t{dy}\t{type}\tlabelMaker}}
        """


class Racetrack(Geo):
    def __init__(self, x: float, y: float, l: float, w: float, rin: float, theta: float, n_seg: int):
        self.draw = f"""
            <{x} {y} {l} {w} {rin} {theta} {n_seg} raceTrack>
        """


class RacetrackInverse(Geo):
    def __init__(self, x: float, y: float, l: float, w: float, rin: float, theta: float, n_seg: int, we: float):
        self.draw = ''
        self.add((
            One80DegreeBendInv(x=x, y=y+rin+w/2, l1=l/2, l2=l/2,
                               d=2*rin+w, w=w, we=we, n=n_seg, theta=-90),
            One80DegreeBendInv(x=x, y=y-rin-w/2, l1=l/2, l2=l/2,
                               d=2*rin+w, w=w, we=we, n=n_seg, theta=90),
        ))
        if theta != 0:
            raise NotImplementedError(
                "RacetrackInverse reverse theta not implemented.")


class One80DegreeBendInv(Geo):
    def __init__(self, x: float, y: float, l1: int, l2: int, d: int, w: float, we: float, n: int, theta: float):
        self.draw = f'<{x} {y} {l1} {l2} {d} {w} {we} {n} {theta} 180degreeBendInv>\n'


class RingResonator(Geo):
    def __init__(self, x: float, y: float,
                 r: float, w: float,
                 x_span: float, lc: float,
                 gap: float, n_seg: int):
        self.draw = ''
        self.add(Waveguide(x, y, w, x_span))
        self.add(Racetrack(x+x_span/2, y+r+w+gap, lc, w, r-w/2, 0, n_seg))
        self.info = {
            'x': x,
            'y': y,
            'r': r,
            'w': w,
            'x_span': x_span,
            'lc': lc,
            'gap': gap,
            'x_center': x+x_span/2,
            'y_center': y+r+w+gap,
        }


class RingResonatorInverse(Geo):
    def __init__(self, x: float, y: float,
                 r: float, w: float,
                 x_span: float, lc: float,
                 gap: float, n_seg: int, we: float, layerA: int, layerB: int):
        self.draw = ''
        self.add(f'{layerB} layer')
        ringresonator_small = RingResonator(
            x=x, y=y, r=r, w=w, x_span=x_span, lc=lc, gap=gap, n_seg=n_seg
        )
        info = ringresonator_small.info
        self.add(ringresonator_small)
        self.add(f'{layerA} layer')
        x0 = info['x']
        y0 = info['y']
        x_center = info['x_center']
        y_center = info['y_center']
        waveguide_big = Waveguide(
            x=x0, y=y0, w=w+2*we, l=x_span, theta=0
        )
        racetrack_big = Racetrack(
            x=x_center, y=y_center, l=lc, w=w+2*we, rin=r-we-w/2, theta=0, n_seg=n_seg
        )
        self.add(waveguide_big)
        self.add(racetrack_big)
        self.info = {
            'x': x,
            'y': y,
            'r': r,
            'w': w,
            'x_span': x_span,
            'lc': lc,
            'gap': gap,
            'x_center': x+x_span/2,
            'y_center': y+r+w+gap,
        }


class RectangleC(Geo):
    def __init__(self, x: float, y: float, l: float, h: float, theta: float):
        self.draw = f"""
            {x} {y} {l} {h} {theta} rectangleC
        """


class RectangleLH(Geo):
    def __init__(self, x: float, y: float, l: float, h: float, theta: float):
        self.draw = f"""
            {x} {y} {l} {h} {theta} rectangleLH
        """


class FourBandWaveguide(Geo):
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, r, w) -> None:
        self.draw = ''
        self.add(Waveguide(x1, y1, w, x2-x1-r))
        x_21 = x2-r
        y_21 = y2
        x_22 = x2
        y_22 = y2+r if y3 > y2 else y2-r
        x_31 = x3
        y_31 = y3-r if y3 > y2 else y3+r
        x_32 = x3+r
        y_32 = y3
        self.add(NightyBandWaveguide(x_21, y_21, x_22, y_22, w, 0))
        self.add(Waveguide(x_22, y_22, w, abs(
            y_31-y_22), 90 if y3 > y2 else -90))
        if y3 > y2:
            self.add(NightyBandWaveguide(x_32, y_32, x_32+r, y_32+r, w, 180))
        else:
            self.add(NightyBandWaveguide(x_32, y_32, x_31, y_31, w, 0))
        self.add(Waveguide(x_32, y_32, w, x4-x_32))


class BendWaveguideInv(Geo):
    def __init__(self, points: list[tuple[float, float]], r: float, w: float, we: float) -> None:
        n_points = len(points)
        self.draw = ''
        if n_points < 2:
            raise ValueError("At least 2 points are required.")
        if n_points == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            vec = np.array([x2-x1, y2-y1]) / \
                np.linalg.norm(np.array([x2-x1, y2-y1]))
            theta = np.arctan2(vec[1], vec[0])*180/np.pi
            self.add(WaveguideInverse(x1, y1, w, np.linalg.norm(
                np.array([x2-x1, y2-y1])), we, theta))
        else:
            x_start = points[0][0]
            y_start = points[0][1]
            for i in range(n_points-1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                vec1 = np.array([x2-x1, y2-y1]) / \
                    np.linalg.norm(np.array([x2-x1, y2-y1]))
                theta1 = np.arctan2(vec1[1], vec1[0])*180/np.pi
                if i == n_points-2:
                    if n_points == 2:
                        self.add(WaveguideInverse(x_start, y_start, w, np.linalg.norm(
                            np.array([x2-x1, y2-y1])), we, theta1))
                    else:
                        self.add(WaveguideInverse(x_start, y_start, w, np.linalg.norm(
                            np.array([x2-x_start, y2-y_start])), we, theta1))
                    break
                self.add(WaveguideInverse(x_start, y_start, w, np.linalg.norm(
                    np.array([x2-x_start, y2-y_start]))-r, we, theta1))
                x3, y3 = points[i+2]
                vec2 = np.array([x3-x2, y3-y2]) / \
                    np.linalg.norm(np.array([x3-x2, y3-y2]))
                theta2 = np.arctan2(vec2[1], vec2[0])*180/np.pi
                theta21 = computeAngleDegrees(vec1, vec2)
                x21 = x2+r if theta1 == 180 else x2-r if theta1 == 0 else x2
                y21 = y2+r if theta1 == -90 else y2-r if theta1 == 90 else y2
                x22 = x2-r if theta2 == 180 else x2+r if theta2 == 0 else x2
                y22 = y2+r if theta2 == 90 else y2-r if theta2 == -90 else y2
                if theta21 > 0:
                    self.add(NightyBandWaveguideInv(
                        x21, y21, r, r, w, we, theta1))
                else:
                    self.add(NightyBandWaveguideInv(
                        x22, y22, r, r, w, we, theta2+180))
                x_start = x22
                y_start = y22
                
class BendWaveguide(Geo):
    def __init__(self, points: list[tuple[float, float]], r: float, w: float) -> None:
        n_points = len(points)
        self.draw = ''
        if n_points < 2:
            raise ValueError("At least 2 points are required.")
        if n_points == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            vec = np.array([x2-x1, y2-y1]) / \
                np.linalg.norm(np.array([x2-x1, y2-y1]))
            theta = np.arctan2(vec[1], vec[0])*180/np.pi
            self.add(Waveguide(x1, y1, w, np.linalg.norm(
                np.array([x2-x1, y2-y1])), theta))
        else:
            x_start = points[0][0]
            y_start = points[0][1]
            for i in range(n_points-1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                vec1 = np.array([x2-x1, y2-y1]) / \
                    np.linalg.norm(np.array([x2-x1, y2-y1]))
                theta1 = np.arctan2(vec1[1], vec1[0])*180/np.pi
                if i == n_points-2:
                    if n_points == 2:
                        self.add(Waveguide(x_start, y_start, w, np.linalg.norm(
                            np.array([x2-x1, y2-y1])), theta1))
                    else:
                        self.add(Waveguide(x_start, y_start, w, np.linalg.norm(
                            np.array([x2-x_start, y2-y_start])), theta1))
                    break
                self.add(Waveguide(x_start, y_start, w, np.linalg.norm(
                    np.array([x2-x_start, y2-y_start]))-r, theta1))
                x3, y3 = points[i+2]
                vec2 = np.array([x3-x2, y3-y2]) / \
                    np.linalg.norm(np.array([x3-x2, y3-y2]))
                theta2 = np.arctan2(vec2[1], vec2[0])*180/np.pi
                theta21 = computeAngleDegrees(vec1, vec2)
                x21 = x2+r if theta1 == 180 else x2-r if theta1 == 0 else x2
                y21 = y2+r if theta1 == -90 else y2-r if theta1 == 90 else y2
                x22 = x2-r if theta2 == 180 else x2+r if theta2 == 0 else x2
                y22 = y2+r if theta2 == 90 else y2-r if theta2 == -90 else y2
                if theta21 > 0:
                    self.add(NightyBandWaveguide(
                        x21, y21, r, r, w, theta1))
                else:
                    self.add(NightyBandWaveguide(
                        x22, y22, r, r, w,  theta2+180))
                x_start = x22
                y_start = y22    

class NightyBandWaveguide(Geo):
    def __init__(self, x1, y1, l, h, w, theta) -> None:
        self.draw = f'<{x1} {y1} {l} {h} {w} {theta} 90degreeBendLH>'


class NightyBandWaveguideInv(Geo):
    def __init__(self, x1, y1, l, h, w, we, theta) -> None:
        self.draw = f'<{x1} {y1} {l} {h} {w} {we} {theta} 90degreeBendInv>'


class ExponentialTaper(Geo):
    def __init__(self, x1, y1, L, w1, w2, n_seg, theta) -> None:
        self.draw = f'<{x1} {y1} {L} {w1} {w2} {n_seg} {theta} exponentialTaper>'


class LabelMakerAutoOutline(Geo):
    def __init__(self, row: int, col: int, font_name: str, font_size: int, x: float, y: float, xr: float, yr: float, dx: float, dy: float, type: str) -> None:
        self.draw = f'{{{row}\t{col}\t{font_name}\t{font_size}\t{x}\t{y}\t{xr}\t{yr}\t{dx}\t{dy}\t{type}\tlabelOutline}}'


class TextOutline(Geo):
    def __init__(self, text: str, font_name: str, font_size: int, x, y) -> None:
        self.draw = f'<{{{{{text}}}}} {{{{{font_name}}}}} {font_size} {x} {y} textOutline>'


class InstanceSym(Geo):
    def __init__(self, struct_name: str, x: float, y: float, x_ll, y_ll, x_ur, y_ur, MIR: str, MAG: float, theta: float):
        self.draw = f'<{struct_name} {x} {y} {x_ll} {y_ll} {x_ur} {y_ur} {MIR} {MAG} {theta} instanceSym>'


class GratingCouplerWaveguide(Geo):

    def __init__(self, x, y, w, l, we, lambda_0, neff, nc, theta_c, r, g_p, ratio, ng, ns, layer_waveguide, layer_grating, theta) -> None:
        """
        Initialize the OpticIO class.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            w (float): The width of the waveguide.
            l (float): The length of the waveguide.
            we (float): The spacing aside the waveguide.
            lambda_0 (float): The central wavelength.
            neff (float): The effective index.
            nc (float): The cladding index.
            theta_c (float): The critical angle.
            r (float): The radius.
            g_p (float): The grating period.
            ratio (float): The ratio.
            ng (float): Numners of grating.
            ns (float): The substrate index.
            l_wg (float): The waveguide length.
            ec (float): The coupling efficiency.
            theta (float): The angle.

        Returns:
            None
        """
        self.draw = f'<{x} {y} {w} {l} 0 {we} {lambda_0} {neff} {nc} {theta_c} {r} {g_p} {ratio} {ng} {ns} {layer_waveguide} {layer_grating} 0 {theta} gratingCWGinv>\n'
        x1, y1 = 0, w/2
        x2, y2 = w/2/np.tan(np.deg2rad(theta_c/2)), w/2
        x3, y3 = r*1.3*np.cos(np.deg2rad(theta_c/2)), r * \
            1.3*np.sin(np.deg2rad(theta_c/2))
        x4, y4 = x3, -y3
        x5, y5 = x2, -y2
        x6, y6 = x1, -y1
        x7, y7 = 0, -r*1.35*np.tan(np.deg2rad(theta_c/2))
        x8, y8 = x3*1.1, y7
        x9, y9 = x8, -y8
        x10, y10 = x7, -y7
        box_points = [
            (x1, y1),
            (x2, y2),
            (x3, y3),
            (x4, y4),
            (x5, y5),
            (x6, y6),
            (x7, y7),
            (x8, y8),
            (x9, y9),
            (x10, y10),
        ]
        self.add(f'{layer_waveguide} layer')
        self.add(Points2Shape(box_points))


class Points2Shape(Geo):
    def __init__(self, points: list[tuple[float, float]]) -> None:
        self.draw = ''
        for point in points:
            self.draw += f'{point[0]} {point[1]}\n'
        self.draw += 'points2shape'


class Circle(Geo):
    def __init__(self, x: float, y: float, r: float) -> None:
        self.draw = f'{x} {y} {r} {r} 0 ellipseVector'

class DiskResonatorInv(Geo):
    def __init__(self, x,y,r,w,we,x_span, gap, layerA:int, layerB:int, shapeReso=None) -> None:
        if shapeReso is not None:
            self.draw = f'{shapeReso} shapeReso\n'
        else:
            self.draw = ''
        self.add(f'{layerB} layer')
        self.add(Circle(x+x_span/2, y+w/2+gap+r, r))
        self.add(Waveguide(x, y, w, x_span, 0))
        self.add(f'{layerA} layer')
        self.add(Circle(x+x_span/2, y+w/2+gap+r, r+we))
        self.add(Waveguide(x, y, w+2*we, x_span, 0))

def computeAngleDegrees(v1, v2):
    dot_product = np.dot(v1, v2)
    cross_product = np.cross(v1, v2)
    angle_radians = np.arctan2(cross_product, dot_product)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees
