import shapely
from shapely.geometry import Point, LineString
import numpy as np

# Google headquarters:
google_lat = 37.422131
google_lon = -122.084801

# Apple headquarters
apple_lat = 37.33467267707233
apple_lon = -122.0089722675975

google = Point(google_lat, google_lon)
apple = Point(apple_lat, apple_lon)

line = LineString([google, apple])

pts = []
for div in np.arange(0.1,1,0.1):
   pts.extend(line.interpolate(div, normalized=True).coords[:])

print(pts[0])