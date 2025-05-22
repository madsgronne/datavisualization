import folium
import geopandas as gpd
import pandas as pd

# Indlæs kommunegrænser
geo_url = "https://raw.githubusercontent.com/Neogeografen/danmark/master/DK_kommunegrænser.geojson"
kommuner = gpd.read_file(geo_url)

# Indlæs vækstdata
vaekst = pd.read_csv("kommune_vaekst.csv")

# Merge shapefile og vækstdata via kommunenavn
kommuner = kommuner.merge(vaekst, on="navn", how="left")

# Opret Folium-kort
kort = folium.Map(location=[56.0, 10.0], zoom_start=6, tiles="CartoDB positron")

# Choropleth farvekodet efter vækst
choropleth = folium.Choropleth(
    geo_data=kommuner,
    name="Virksomhedsvækst",
    data=kommuner,
    columns=["navn", "vækst"],
    key_on="feature.properties.navn",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Vækst i antal virksomheder (%)",
    nan_fill_color="lightgray"
).add_to(kort)

# Tooltip med kommunenavn og vækst
folium.GeoJsonTooltip(
    fields=["navn", "vækst"],
    aliases=["Kommune:", "Vækst (%):"],
    localize=True
).add_to(choropleth.geojson)

# Gem kortet
kort.save("danmark_vaekstkort.html")
print("Kortet er gemt som 'danmark_vaekstkort.html'")
