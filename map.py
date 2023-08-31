import mongoData
# from fastapi import FastAPI, Form, Request
# from pathlib import Path
# import rich
import dataTemplate
from typing import List

import folium

def AddMapFeatureGroup(groupName):
    return folium.FeatureGroup(
        name = groupName, 
        overlay = True,
        show = True,
        control = True
    )

def AddMapCafes(cafe : dataTemplate.CafeModel, featureGroups):
        
        def GetPopupIcon(cafe : dataTemplate.CafeModel):
            if cafe.category == 'vegan cafe':
                return 'mug-hot'
            elif cafe.category == 'cafe':
                return 'mug-saucer'
            elif cafe.category == 'restaurant':
                return 'utensils'
        
        def GetPopupColour(cafe : dataTemplate.CafeModel):
            if cafe.category == 'vegan cafe':
                return 'darkgreen'
            elif cafe.category == 'cafe':
                return 'orange'
            elif cafe.category == 'restaurant':
                return 'purple'
            
        def AddToGroup(cafe : dataTemplate.CafeModel, featureGroups : dataTemplate.LayerGroups, marker : folium.Marker):
            for x in featureGroups.list:
                if cafe.category == 'vegan cafe':
                    marker.add_to(featureGroups[0])
                elif cafe.category == 'cafe':
                    marker.add_to(featureGroups[1])
                elif cafe.category == 'restaurant':
                    marker.add_to(featureGroups[2])

        newMarker = folium.Marker(
            location = [cafe.coords.lat, cafe.coords.long],
            popup = cafe.name,
            icon= folium.Icon(icon = GetPopupIcon(cafe), prefix='fa', color=GetPopupColour(cafe)),
        )

        return newMarker

        # AddToGroup(cafe, featureGroups, newMarker)
        

async def GetMap():
    map = folium.Map(location=[-33.87332753692324, 151.2081342404059], 
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", 
        attr='© OpenStreetMap contributors © CARTO',
        prefer_canvas=True,
        zoom_start=14,
    )

    layercontrol = folium.LayerControl("topright", collapsed=True)

    featureGroups : List = []

    veganGroup = AddMapFeatureGroup("Vegan Cafes").add_to(map)
    cafeGroup = AddMapFeatureGroup("Cafes").add_to(map)
    restaurantGroup = AddMapFeatureGroup("Restaurants").add_to(map)

    featureGroups.append(veganGroup)
    featureGroups.append(cafeGroup)
    featureGroups.append(restaurantGroup)

    for cafe in mongoData.MakeCafesPydantic().list:
        AddMapCafes(map, cafe, featureGroups).add_to(map)

    for x in featureGroups.list:
        layercontrol.add_child(x)

    layercontrol.add_to(map)

    return map
