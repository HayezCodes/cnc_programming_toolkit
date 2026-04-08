import math


def solve_triangle(opposite=None, adjacent=None, hypotenuse=None):
    result = {}

    if opposite and adjacent:
        hyp = math.sqrt(opposite**2 + adjacent**2)
        angle = math.degrees(math.atan(opposite / adjacent))
        result["opposite"] = opposite
        result["adjacent"] = adjacent
        result["hypotenuse"] = hyp
        result["angle"] = angle

    elif opposite and hypotenuse:
        adj = math.sqrt(hypotenuse**2 - opposite**2)
        angle = math.degrees(math.asin(opposite / hypotenuse))
        result["opposite"] = opposite
        result["adjacent"] = adj
        result["hypotenuse"] = hypotenuse
        result["angle"] = angle

    elif adjacent and hypotenuse:
        opp = math.sqrt(hypotenuse**2 - adjacent**2)
        angle = math.degrees(math.acos(adjacent / hypotenuse))
        result["opposite"] = opp
        result["adjacent"] = adjacent
        result["hypotenuse"] = hypotenuse
        result["angle"] = angle

    return result