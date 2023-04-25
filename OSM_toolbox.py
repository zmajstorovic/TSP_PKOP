import requests

def josm_direction_manager(data):

    # body = {"coordinates": [[18.415, 45.659], [16.342, 46.308], [16.423, 46.21], [16.075, 45.714], [18.8, 45.29],
    #                         [17.4, 45.84], [16.195, 43.059], [15.779, 43.761], [13.853, 44.961], [16.417, 45.884],
    #                         [15.08, 45.37], [17.37, 43.204], [16.4, 43.909], [18.99, 45.35], [15.904, 46.026],
    #                         [15.233, 44.114], [15.981, 45.812], [15.805, 45.857], [16.077, 46.092], [18.694, 45.072]],
    #         "options": {"avoid_borders": "all"}, "preference": "shortest"}
    body = {"coordinates": data,
                "options": {"avoid_borders": "all"}, "preference": "shortest"}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248120c22d418e04cd591189388e30f4526',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=body,
                         headers=headers)
    # print(call.status_code, call.reason)
    # print(call.text)
    return call.text



def direction_manager():
    body = {"coordinates": [[18.415,45.659],[16.342,46.308],
                            [16.423,46.210],[16.075,45.714],
                            [18.800,45.290],[17.400,45.840],
                            [16.195,43.059],[15.779,43.761],
                            [13.853,44.961],[16.417,45.884],
                            [15.080,45.370],[17.370,43.204],
                            [16.400,43.909],[18.990,45.350],
                            [15.904,46.026],[15.233,44.114],
                            [15.981,45.812],[15.805,45.857],
                            [16.077,46.092],[18.694,45.072]]}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248120c22d418e04cd591189388e30f4526',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=body, headers=headers)

    print(call.status_code, call.reason)
    print(call.text)


def single_direction_manager():
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    call = requests.get(
        'https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248120c22d418e04cd591189388e30f4526&start=16.342,46.308&end=18.415,45.659',
        headers=headers)
    print(call.text)


# body = {"locations":[[9.70093,48.477473],[9.207916,49.153868],[37.573242,55.801281],[115.663757,38.106467]]}
def OSM_matrix(data):

    body = {"locations":data, "metrics":["distance","duration"]}
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf6248120c22d418e04cd591189388e30f4526',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
    return call.text

# print(call.status_code, call.reason)
# print(call.text)
# response: {"durations":[
# [0.0,5786.74,90559.09,394856.69],
# [5589.28,0.0,89296.84,393594.44],
# [90304.2,88731.82,0.0,308207.47],
# [394077.72,392505.31,307312.97,0.0]],

# "destinations":[{"location":[9.700817,48.476406],"snapped_distance":118.92},
# {"location":[9.207772,49.153882],"snapped_distance":10.57},
# {"location":[37.572963,55.801279],"snapped_distance":17.45},
# {"location":[115.665017,38.100717],"snapped_distance":648.79}],

# "sources":[{"location":[9.700817,48.476406],"snapped_distance":118.92},
# {"location":[9.207772,49.153882],"snapped_distance":10.57},
# {"location":[37.572963,55.801279],"snapped_distance":17.45},
# {"location":[115.665017,38.100717],"snapped_distance":648.79}],
#
# "metadata":{"attribution":"openrouteservice.org | OpenStreetMap contributors","service":"matrix","timestamp":1677151144048,"query":{"locations":[[9.70093,48.477473],[9.207916,49.153868],[37.573242,55.801281],[115.663757,38.106467]],"profile":"driving-car","responseType":"json"},"engine":{"version":"6.8.0","build_date":"2022-10-21T14:34:31Z","graph_date":"2023-02-19T15:04:34Z"}}}
