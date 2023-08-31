import mongoData
import dataTemplate
from typing import List

import folium

def AddMapFeatureGroup(groupName, map):
    return folium.FeatureGroup(
        name = groupName, 
        overlay = True,
        show = True,
        control = True
    )

def MakeMylkHTML(cafe : dataTemplate.CafeModel):
    html = ""

    for x in cafe.mylks:
        html += f"<h5><b>{x.type}: </b></h5>"
        if type(x.name) is None:
            html += "<h5><b>Not known!</b></h5>"
        else:
            html += f"<h5><b>{x.name}</b></h5>"

            html += f"<h5><b>Extra cost?</b> {x.extraCharge}</h5>"

    return html

def htmlTemplate(cafe : dataTemplate.CafeModel):
    txt = f"""

        <h4><b>{cafe.name}</b></h4>

        <h5><b>Category:</b></h5> 
        <h6>{(cafe.category).capitalize()}</h6>
        <br>

        """

    
    popupHTML = folium.Html(data=(txt + MakeMylkHTML(cafe)),script=True)
    return popupHTML


def AddMapCafes(cafe : dataTemplate.CafeModel):
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
        
    newPop = folium.Popup(
        html=htmlTemplate(cafe)
    )

    newMarker = folium.Marker(
        location = [cafe.coords.lat, cafe.coords.long],
        popup = newPop,
        icon= folium.Icon(icon = GetPopupIcon(cafe), prefix='fa', color=GetPopupColour(cafe)),
    )

    return newMarker

async def GetMap():
    dark_layer = folium.TileLayer(name="Dark",tiles="CartoDB dark_matter",attr="© OpenStreetMap contributors © CARTO")

    map = folium.Map(
        location=[-33.87332753692324, 151.2081342404059],
        prefer_canvas=True,
        zoom_start=14,
        tiles=dark_layer,
    )

    folium.TileLayer(tiles="CartoDB Positron", name="Light", attr="© OpenStreetMap contributors © CARTO").add_to(map)


    veganGroup = AddMapFeatureGroup("Vegan Cafes", map)
    cafeGroup = AddMapFeatureGroup("Cafes", map)
    restaurantGroup = AddMapFeatureGroup("Restaurants", map)

    for cafe in mongoData.MakeCafesPydantic().list:
        if cafe.category == 'vegan cafe':
            veganGroup.add_child(AddMapCafes(cafe))

        elif cafe.category == 'cafe':
            cafeGroup.add_child(AddMapCafes(cafe))

        elif cafe.category == 'restaurant':
            restaurantGroup.add_child(AddMapCafes(cafe))

    veganGroup.add_to(map)
    cafeGroup.add_to(map)
    restaurantGroup.add_to(map)

    folium.LayerControl("topright", collapsed=True).add_to(map)

    return map
