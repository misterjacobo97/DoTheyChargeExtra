from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import HTMLResponse
from map import GetMap

app = FastAPI()

@app.get("/")
async def root():
    map = await GetMap()

    return Response(map.get_root().render())

@app.get("/new_entry")
async def NewEntry():
    return HTMLResponse(
        """<!DOCTYPE>
        <html>
        <body>hello</body>
        </html>
        """
    )