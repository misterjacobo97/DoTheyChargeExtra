import mongoData
import dataTemplate
from typing import List

import folium

def oldcss():
    style = """

        .container,
        .title,
        .title-popup-icon,
        .subtitle,
        .popup-body,
        .popup-body-title {
        display: flex;
        flex-direction: column;
        }

        .container{
        width: 70vw;
        display: flex;
        align-items: stretch;
        padding: 0;
        }

        .popup-body{
        align-items: stretch;
        }

        .popup-body-title {
        align-items: center;
        }

        .popup-body-content-brand,
        .popup-body-content-extra {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        }

        .popup-body-content {
        display: flex;
        width:100%;
        flex-direction: row;
        justify-content: stretch;
        }

        .popup-body-content>.content-headings,
        .content-info, .popup-divider {
        display: flex;
        flex-direction: column;
        }

        .popup-divider{
        flex-basis: 20%;
        }

        .content-headings, .content-info {
        flex-basis: 100%;
        align-items: stretch;
        }
        .content-headings{
        text-align: end;
        }

        .leaflet-popup-content-wrapper,
        .leaflet-popup-tip {
        background: #393939 !important;
        }

        h4,
        h5,
        h6 {
        color: white;
        }

        .subtitle {
        width: 100%;
        text-align: center;
        }

        .subtitle>h5 {
        color: #636363;
        font-family: serif;
        font-style: italic;
        }

        .fa-solid {
        width: 100%;
        text-align: center;
        }

        .fa-2xl {
        font-size: xx-large !important;
        }

        .title-popup-icon {
        width: 100%;
        text-align: center;
        padding-top: 10%;
        padding-bottom: 15%;
        }

        .title-popup {
        text-align: center;
        margin: flex;
        padding: 1%;
        border: 2px solid #636363;
        border-right-style: none;
        border-left-style: none;
        }

        /* 
        .popup-body-title {
        } */
    """
    
    return style

def AddMapFeatureGroup(groupName, map):
    return folium.FeatureGroup(
        name = groupName, 
        overlay = True,
        show = True,
        control = True
    )

def MakePopupHead():
    style = "<style>" + oldcss() + "</style>" #open(".\css\popupStyles.css").read() + "</style>"

    return style

def MakePopupHTML(cafe : dataTemplate.CafeModel, icon : str, iconColour : str):
    title = f"""
        <div class=title>
            <div class="title-popup-icon">
                <i class="fa-solid fa-{icon} fa-2xl" style="color: {iconColour};"></i>
            </div>
            <div class="title-popup">
                <h4><b>{cafe.name}</b></h4>
            </div>
            <div class=subtitle>
                <h5>{(cafe.category).capitalize()} </h5> 
            </div>
        </div>
        <br>
        """

    body = "<div class=popup-body>"
    for x in cafe.mylks:
        body += f"<div class=popup-body-title><h5><b>{x.type[0].capitalize()}</b></h5></div>"

        body += "<div class=popup-body-content>"
        
        body += "<div class=content-headings><h5 id=brand-tag>Brand:</h5><h5 id=extra-cost-title>Extra cost:</h5></div>"

        body += "<div class=popup-divider></div>"

        body += "<div class=content-info>"
        
        if x.name[0] is None:
            body += "<h5 id=unknown-tag>Not known!</h5><h5 id=unknown-tag>Not known!</h5>"
        else:
            body += f"<h5 id=name-tag>{x.name[0].capitalize()}</h5>"

            body += f"<h5 id=extra-cost-tag>{x.extraCharge}</h5>"
        body += "</div></div>"

    popupHTML = folium.Html(width=200,data=("<div class=container>" + title + body + "</div>"),script=True)
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

    def GetPopupTitleColour(cafe : dataTemplate.CafeModel):
        if cafe.category == 'vegan cafe':
            return '#728224'
        elif cafe.category == 'cafe':
            return '#f59630'
        elif cafe.category == 'restaurant':
            return '#cf51b6'
        
    newPop = folium.Popup(
        html=MakePopupHTML(cafe, GetPopupIcon(cafe), GetPopupTitleColour(cafe)),
        lazy=True
    )

    newMarker = folium.Marker(
        location = [cafe.coords.lat, cafe.coords.long],
        popup = newPop,
        icon= folium.Icon(icon=GetPopupIcon(cafe), prefix='fa', color=GetPopupColour(cafe)),
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
