import pyproj

# Переменные для настройки координат
msk64 = pyproj.CRS.from_string("+proj=merc +ellps=krass +lat_ts=55.0 +lon_0=37.5 +x_0=0 +y_0=0 +k=1.0 "
                               "+units=m +nadgrids=@null +no_defs")
wgs84 = pyproj.CRS.from_string("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
transformer = pyproj.Transformer.from_crs(msk64, wgs84, always_xy=True)

# Имена файлов со всеми данными и составными объектами
file_all = '../data/all.xlsx'
file_compos = '../data/composite.xlsx'
