from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from map import GetMap


import mongowebform, mongoData

app = FastAPI()

@app.get("/")
async def root():
    map = await GetMap()

    return Response(map.get_root().render())

@app.get("/cafes_info")
async def NewEntry(cafe = None):

    if cafe:
        return HTMLResponse(
            mongowebform.MakeWebform(cafe)
        )
    
    return HTMLResponse(
        mongowebform.MakeWebform()
    )

@app.get('/get_cafe')
def GetCafe(cafe = None):
    cafeinfo = mongoData.MakeCafesPydantic()

    
    html = f"""
    <table style="width: 100%">

        <tr>
            <th>Name</th>
            <th>category</th>

            <th>Mylk 1</th>
            <th>Name</th>
            <th>X</th>
            <th>Mylk 2</th>
            <th>Name</th>
            <th>X</th>
            <th>Mylk 3</th>
            <th>Name</th>
            <th>X</th>

            <th>type</th>
            <th>name</th>
            <th>vegan</th>

            <th>Lat</th>
            <th>Long</th>
        </tr> 
    """

    # if not cafe:
    #     cafeinfo = cafeinfo.list

    for x in cafeinfo.list:
        html += f"""
            <tr>
            <td>{x.name}</td>
            <td>{x.category}</td>
        """

        for y in x.mylks:
            html += f"""
            <td>{y.type[0]}</td>
            <td>{y.name[0]}</td>
            <td>{y.extraCharge}</td>
            """

        html += f"""
            <td>{x.chai.type}</td>
            <td>{x.chai.name}</td>
            <td>{x.chai.vegan}</td>
            <td>{x.coords.lat}</td>
            <td>{x.coords.long}</td>
        """

    html += "</table>"
        
    return HTMLResponse(
        html
    )

# app.mount('/css/webform', app=StaticFiles(directory='css'), name="webform.css")


@app.get("/css/{style}")
def GetStyle(style):
    return FileResponse(f"./css/{style}.css")