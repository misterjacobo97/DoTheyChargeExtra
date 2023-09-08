from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import mongoengine

import dotenv
import os

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

dotenv.load_dotenv()

mongoengine.connect(host = os.environ["MONGO_URL"])

class Chai(mongoengine.EmbeddedDocument):
    type = mongoengine.StringField()
    name = mongoengine.StringField()
    vegan = mongoengine.BooleanField()

class Mylk(mongoengine.EmbeddedDocument):
    type = mongoengine.StringField(required = True)
    name = mongoengine.StringField()
    chargeExtra = mongoengine.BooleanField()

class Cafe(mongoengine.Document):
    lastedit = mongoengine.DateTimeField(default=datetime.utcnow)
    name = mongoengine.StringField(required=True)
    category = mongoengine.StringField(required=True)
    address = mongoengine.StringField()
    coords = mongoengine.GeoPointField()
    mylks = mongoengine.EmbeddedDocumentListField(document_type=Mylk)
    chai = mongoengine.EmbeddedDocumentField(document_type=Chai)
    meta = {
        'indexes':[{
            'fields': ['$name', '$category'],
            'default_language': 'english',
            'weights': {'name': 10, 'category': 8}
        }],
        'collection': 'VeganCafes'
    }

def AddNewCafe(
        cafe_name: str, 
        cafe_category: str,
        cafeAddress : str = None,
        NewCoords : list = [0,0],
        OatName : str = None,
        SoyName : str = None,
        AlmondName : str = None,
        chargeX : bool = False,
        chaiName : str = None,
        chaiType : str = None,
        chaiVegan : bool = False
    ):

    valid_categories = list(['Vegan Cafe', 'Cafe', 'Restaurant'])

    if cafe_category not in valid_categories:
        return ValueError.with_traceback()
    
    oat = Mylk(
        type = "Oat",
        name = OatName,
        chargeExtra = chargeX
    )
    soy = Mylk(
        type = "Soy",
        name = SoyName,
        chargeExtra = chargeX
    )
    almond = Mylk(
        type = "Almond",
        name = AlmondName,
        chargeExtra = chargeX,
    )

    chaiObj = Chai(
        type = chaiType,
        name = chaiName,
        vegan = chaiVegan
    )


    new_cafe = Cafe(
        name = cafe_name,
        category = cafe_category,
        address = cafeAddress,
        coords = NewCoords,
        mylks = [oat, soy, almond],
        chai = chaiObj
    )
    new_cafe.save()