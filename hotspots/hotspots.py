from geopy.distance import geodesic
import math

# Fonction pour calculer la distance euclidienne
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y1 - y2)**2)

# Fonction pour interpoler entre deux points
def interpolate(lat1, lon1, lat2, lon2, fraction):
    lat_new = lat1 + fraction * (lat2 - lat1)
    lon_new = lon1 + fraction * (lon2 - lon1)
    return lat_new, lon_new

# Fonction pour redimensionner une liste en insérant des points à distance de 0.1 km
def resize_with_distance(lat_list, lon_list, distance_km=0.1):
    new_lat_list = []
    new_lon_list = []

    for i in range(len(lat_list) - 1):
        lat1, lon1 = lat_list[i], lon_list[i]
        lat2, lon2 = lat_list[i + 1], lon_list[i + 1]

        new_lat_list.append(lat1)
        new_lon_list.append(lon1)

        distance_between_points = geodesic((lat1, lon1), (lat2, lon2)).kilometers

        if distance_between_points > distance_km:
            num_points = int(distance_between_points / distance_km)
            
            for j in range(1, num_points):
                fraction = j / num_points
                new_lat, new_lon = interpolate(lat1, lon1, lat2, lon2, fraction)
                new_lat_list.append(new_lat)
                new_lon_list.append(new_lon)

    new_lat_list.append(lat_list[-1])
    new_lon_list.append(lon_list[-1])

    return new_lat_list, new_lon_list

# Fonction pour calculer les distances entre deux listes de points
def distances(listx1, listy1, listx2, listy2):
    dist = []
    for i in range(len(listx1) - 1):
        testx = euclidean_distance(listx1[i], listy1[i], listx2[0], listy2[0])
        x1, y1, x2, y2 = listx1[i], listy1[i], listx2[0], listy2[0]
        for j in range(len(listx2) - 1):
            minx = euclidean_distance(listx1[i], listy1[i], listx2[j], listy2[j])
            if minx < testx:
                testx = minx
                x2, y2 = listx2[j], listy2[j]
        dist.append([testx, x1, y1, x2, y2])
    return dist

# Fonction principale pour détecter les hotspots
def detect_hotspots(lat1, long1, lat2, long2, threshold=0.18):
    lat1_resized, long1_resized = resize_with_distance(lat1, long1, distance_km=0.1)
    lat2_resized, long2_resized = resize_with_distance(lat2, long2, distance_km=0.1)
    
    distance = distances(lat1_resized, long1_resized, lat2_resized, long2_resized)
    hotspot = False
    POLYs, POLY = [], []
    
    for row in distance:
        if row[0] > threshold:
            if not hotspot:
                hotspot = True
                POLY.append(row)
            else:
                POLY.append(row)
        else:
            if hotspot:
                POLYs.append(POLY)
                hotspot = False
                POLY = []
    
    if hotspot:
        POLYs.append(POLY)

    return POLYs
