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