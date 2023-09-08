import mongoData
from dataTemplate import AddNewCafe, Cafe

AddNewCafe(
    "shift test",
    "Vegan Cafe"
)

def CafeSelection():
    cafes = mongoData.MakeCafesPydantic().list

    form = f"""
        <label for="cafe">Cafes:</label>
        <select name="cafe" id="cafe-select" hx-get="/get_cafe" hx-target="#cafe-label" hx-indicator=".htmx-indicator">
        """
        
    for x in cafes:
        form += f'<option value="{x.name}"> {x.name} </option>'

    form += "</select><br>"
    # form += "<button >send</button>"

    return form

def MakeCafeTable():
    cafeinfo = Cafe()

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
    print(cafeinfo.name)
    for x in cafeinfo.objects:
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
    return html

def MakeWebform():
    form = f"""
        <html>
        <head>
            <script src="https://unpkg.com/htmx.org@1.9.5"></script>
            <link rel="stylesheet" href="/css/webform" type="text/css"/>
        </head>
        <body>
            <div id="cafe-table">
                {MakeCafeTable()}
            </div>

        </body>
        </html>"""

    return form