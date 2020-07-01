import pandas
import folium

def el_color(el):
    if el<1000 :
        return "green"
    elif 1000<= el <3000:
        return "orange" 
    else:
        return "red"

data = pandas.read_csv("Volcanoes.csv")
latitudes = list(data.LAT)
longitudes = list(data.LON)
name = list(data.NAME)
elev = list(data.ELEV)

corona_data = pandas.read_csv("global_covid19_mortality_rates.csv")
lat1 = list(corona_data.Latitude)
lon1 = list(corona_data.Longitude)
conf=list(corona_data.Confirmed)
death=list(corona_data.Deaths)
mort = list(corona_data.Mortality_Rate)
coun=list(corona_data.Country)

html="""
Volcano name:<a href="https://en.wikipedia.org/wiki/%s" target="_blank">%s</a><br>
Height: %s m
"""

html1="""
<h3>Country: %s</h3><br>
Confirmed: %s<br>
Deaths: %s<br>
Mortality Rate: %s
"""
#Layer1
map = folium.Map(location=[38.58,-99],zoom_start=4)

#Layer2
fgv = folium.FeatureGroup(name="Volcanoes")

for lat,lon,n,el in zip(latitudes,longitudes,name,elev):
    iframe = folium.IFrame(html=html % (n,n,el), width=200, height=80)
    fgv.add_child(folium.CircleMarker(location=[lat,lon],popup=folium.Popup(iframe) , tooltip=n,
    fill_color=el_color(el), color="grey", fill_opacity=0.7))


#Layer3
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data = open("world.json","r",encoding="utf-8-sig").read(),
style_function=lambda x: {'fillColor': 'red' if x['properties']['POP2005']<10000000 
else 'orange' if 10000000< x['properties']['POP2005'] <20000000 else 'green'}))

#Layer4
fgc = folium.FeatureGroup(name="Covid19")
for lat,lon,con,dea,mor,cou in zip(lat1,lon1,conf,death,mort,coun):
    iframe = folium.IFrame(html=html1 % (cou,str(con),str(dea),str(mor)), width=250, height=150)
    fgc.add_child(folium.Marker(location=[lat,lon],popup=folium.Popup(iframe) , tooltip=cou))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(fgc)
map.add_child(folium.LatLngPopup())

#LayerControl
map.add_child(folium.LayerControl())


map.save("Map1.html")