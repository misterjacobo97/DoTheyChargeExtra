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

def MakePopupHead():
    style = """
        <style>
            .leaflet-popup-content-wrapper, .leaflet-popup-tip {background : #393939 !important;}

            h4, h5, h6 {color : white;}

        </style>
        """
    
    return style

def MakePopupHTML(cafe : dataTemplate.CafeModel):
    title = f"""
        <div>
        <img src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600">

        <h4><b>{cafe.name}</b></h4>

        <h5><b>Category:</b> {(cafe.category).capitalize()} </h5> 
        </div>
        <br>
        """

    body = ""
    for x in cafe.mylks:
        body += f"<h5><b>{x.type[0].upper()}: </b></h5>"
        if x.name[0] is None:
            body += "<h5><b>Not known!</b></h5>"
        else:
            body += f"<h5><b>{x.name[0].capitalize()}</b></h5>"

            body += f"<h5><b>Extra cost?</b> {x.extraCharge}</h5>"

    popupHTML = folium.Html(width=200,data=(title + body),script=True)
    return popupHTML

def MakeMarker(cafe : dataTemplate.CafeModel):
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
        html=MakePopupHTML(cafe),
        lazy=True
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
            veganGroup.add_child(MakeMarker(cafe))

        elif cafe.category == 'cafe':
            cafeGroup.add_child(MakeMarker(cafe))

        elif cafe.category == 'restaurant':
            restaurantGroup.add_child(MakeMarker(cafe))

    veganGroup.add_to(map)
    cafeGroup.add_to(map)
    restaurantGroup.add_to(map)

    # adding scalability for mobile display
    map.get_root().header.add_child(folium.Element(
        MakePopupHead()
    ))

    folium.LayerControl("topright", collapsed=True).add_to(map)

    return map
