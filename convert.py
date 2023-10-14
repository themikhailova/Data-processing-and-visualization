import pandas as pd
import pyproj


# функция для преобразования
def convert_coordinates(row):
    x, y = row['Координата X (м, система координат СК-1964)'], row['Координата Y (м, система координат СК-1964)']
    lon, lat = transformer.transform(x, y)
    return pd.Series({'Latitude': lat, 'Longitude': lon})


# параметры проекций для МСК-64 и WGS84
msk64 = pyproj.CRS.from_string("+proj=merc +ellps=krass +lat_ts=55.0 +lon_0=37.5 +x_0=0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs")
wgs84 = pyproj.CRS.from_string("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

df = pd.read_excel('data.xlsx')

transformer = pyproj.Transformer.from_crs(msk64, wgs84, always_xy=True)
df[['Latitude', 'Longitude']] = df.apply(convert_coordinates, axis=1)

df.to_excel('converted_coordinates.xlsx', index=False)
