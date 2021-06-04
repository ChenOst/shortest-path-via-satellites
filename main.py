from skyfield.api import EarthSatellite, N, W, wgs84, load
from math import sin, cos, sqrt, atan2, radians
import networkx as nx
import matplotlib.pyplot as plt


satellites_results = []
start_point = {}
end_point = {}


def main():
    ts = load.timescale()
    t = ts.now()
    max_range = int(input("Enter the air distance in km: "))
    g = nx.Graph()

    get_user_input()

    starlink_url = 'http://www.celestrak.com/NORAD/elements/starlink.txt'
    satellites = load.tle_file(starlink_url)

    # distance between ground and satellite
    for satellite in satellites:
        # print(satellite)  # prints more info on the satellite
        if satellite.name != "FALCON 9 DEB":  # We don't want to get info about FALCON 9
            # Geocentric
            geometry = satellite.at(t)
            # Geographic point beneath satellite
            subpoint = wgs84.subpoint(geometry)
            latitude = subpoint.latitude
            longitude = subpoint.longitude

            satellite_info = {"name": satellite.name, "latitude": latitude.degrees, "longitude": longitude.degrees}

            dist1 = calculate_distance(start_point, satellite_info)
            dist2 = calculate_distance(end_point, satellite_info)

            if dist1 < max_range:
                g.add_edge(start_point["name"], satellite_info["name"], weight=dist1)

            if dist2 < max_range:
                g.add_edge(end_point["name"], satellite_info["name"], weight=dist2)

    # distance between two earth satellite
    for i in range(0, len(satellites)):
        for j in range(i+1, len(satellites)-1):
            if satellites[i].name != "FALCON 9 DEB" and satellites[j].name != "FALCON 9 DEB":
                distance = (satellites[i].at(t) - satellites[j].at(t)).distance().km
                if distance < max_range:
                    g.add_edge(satellites[i].name, satellites[j].name, weight=distance)

    pos = nx.spring_layout(g)

    # This option can add satellites name into the graph
    # nx.draw(g, pos, node_color='b', with_labels = True, font_size=10)
    nx.draw(g, pos, node_color='b')
    # draw path in red
    path = nx.shortest_path(g, source="Start Point", target="End Point")
    print(path)
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(g, pos, nodelist=path, node_color='r', node_size=400)
    nx.draw_networkx_edges(g, pos, edgelist=set(path_edges), edge_color='r', width=10)
    plt.axis('equal')
    plt.show()


def calculate_distance(point1, point2):
    # approximate radius of earth in km
    R = 6373.388

    lat1 = radians(point1["latitude"])
    lon1 = radians(point1["longitude"])
    lat2 = radians(point2["latitude"])
    lon2 = radians(point2["longitude"])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def get_user_input():
    start_point_coordinates = input("Enter the start point coordinates: ")
    end_point_coordinates = input("Enter the end point coordinates: ")

    x = start_point_coordinates.split(', ')
    y = end_point_coordinates.split(', ')

    start_point.update({"name": "Start Point", "latitude": float(x[0]), "longitude": float(x[1])})
    end_point.update({"name": "End Point", "latitude": float(y[0]), "longitude": float(y[1])})


if __name__ == "__main__":
    main()
