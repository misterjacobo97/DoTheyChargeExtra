
from pymongo.mongo_client import MongoClient
import dataTemplate

from dotenv import load_dotenv
import os

load_dotenv()

def GetDB():
    uri =  os.environ["MONGO_URL"]
    client = MongoClient(uri)

    return client.DoTheyChargeExtraDB#cafes

def GetCafeDocs(room : str = None):
    if room:
        return GetDB().VeganCafes.find({'name':room})#.cafeinfo.find({'name':room})
    return GetDB().VeganCafes.find({})#cafeinfo.find({})

def MakeCafesPydantic(room : str = None):
    cafesList = dataTemplate.CafeList()

    for x in GetCafeDocs(room):
        cafe = dataTemplate.CafeModel()
        cafe.coords.lat = x['coords']['lat']
        cafe.coords.long = x['coords']['long']
        cafe.name = x['name']
        cafe.category = x['category']

        for mylk in x['mylks']:
            newMylk = dataTemplate.MylkModel()
            newMylk.type = mylk['type'],
            newMylk.name = mylk['name'],
            newMylk.extraCharge = mylk['extraCharge']
            
            cafe.mylks.append(newMylk)

        cafe.chai.name = x['chai']['name']
        cafe.chai.vegan = x['chai']['vegan']

        cafe.timeLogged = x['timeLogged']

        if room is not None:
            return cafe
        else:
            cafesList.list.append(cafe)

    return cafesList