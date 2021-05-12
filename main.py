import networkx as nx
from skyfield.api import EarthSatellite, N, W, wgs84, load
from math import sin, cos, sqrt, atan2, radians


my_dict = {}
satellites_results = []


def main():
    ts = load.timescale()
    t = ts.now()

    #get_user_input()

    starlink_url = 'http://www.celestrak.com/NORAD/elements/starlink.txt'
    satellites = load.tle_file(starlink_url)
    print('Loaded', len(satellites), 'satellites')

    for satellite in satellites:
        # print(satellite) prints more info on the satellite
        if satellite.name != "FALCON 9 DEB": # We don't want to get info about FALCON 9
            # Geocentric
            geometry = satellite.at(t)
            # Geographic point beneath satellite
            subpoint = wgs84.subpoint(geometry)
            latitude = subpoint.latitude
            longitude = subpoint.longitude
            satellites_results.append({"name": satellite.name, "latitude": latitude.degrees, "longitude": longitude.degrees})
    print(satellites_results)


def calculate_distance(point1, point2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(point1["latitude"])
    lon1 = radians(point1["longitude"])
    lat2 = radians(point2["latitude"])
    lon2 = radians(point2["longitude"])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    print("Result:", distance)
    print("Should be:", 278.546, "km")


def get_user_input():
    start_point_coordinates = input("Enter the start point coordinates: ")
    end_point_coordinates = input("Enter the end point coordinates: ")
    x = start_point_coordinates.split(', ')
    y = end_point_coordinates.split(', ')
    # results.append(
    #     {
    #        {"name": "Start", "lat": float(x[0]), "lon": float(x[1])},
    #        {"name": "End", "lat": float(y[0]), "lon": float(y[1])},
    #     }
    # )


if __name__ == "__main__":
    main()