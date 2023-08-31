from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

class CoordinatesModel(BaseModel):
    lat : float = None
    long : float = None

class ChaiModel(BaseModel):
    name : str = None
    vegan : bool = False
    type : str = None

class MylkModel(BaseModel):
    name : str = None
    type : str = None
    extraCharge : bool = False

class CafeModel(BaseModel):
    category : str = None
    name : str = None
    coords : CoordinatesModel = CoordinatesModel()
    mylks : List[MylkModel] = []
    chai : ChaiModel = ChaiModel()
    timeLogged : datetime = None

class CafeList(BaseModel):
    list : List[CafeModel] = []

# tamplates for maps
class LayerGroups(BaseModel):
    list : List = []