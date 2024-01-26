import json
from decimal import Decimal

from pandas._libs.missing import NAType


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, NAType):
            return ""
        return json.JSONEncoder.default(self, obj)


def dms_to_decimal(degrees, minutes, seconds, direction):
    try:
        decimal_degrees = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if direction in ["S", "W"]:
            decimal_degrees = -decimal_degrees
        return decimal_degrees
    except:
        return ""


def convert_coordinates(coord_str):
    if isinstance(coord_str, str):
        # Split the input string into components
        parts = coord_str.split()

        # Extract degrees, minutes, seconds, and direction
        degrees = parts[1][:-1]
        minutes = parts[2][:-1]
        try:
            seconds = parts[3][:-2]
        except IndexError:
            return ""
        direction = parts[0]

        # Convert to decimal coordinates
        decimal_coords = dms_to_decimal(degrees, minutes, seconds, direction)

        return decimal_coords
    else:
        return ""
