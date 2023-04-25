import random
from delivery import *
from delivery import run_episode, DeliveryQAgent, run_n_episodes
from gotools import main as gotool
from OSM_toolbox import OSM_matrix, josm_direction_manager
import json
import folium
from folium.plugins import PolyLineOffset, AntPath, BeautifyIcon, PolyLineTextPath
import numpy as np
import io
from PIL import Image
from scipy.spatial import distance_matrix as dm
import math


def make_gif():
    frames = [Image.open(image) for image in glob.glob("mapa_\d{1,3}.png")]
    frame_one = frames[0]
    frame_one.save("my_awesome.gif", format="GIF", append_images=frames,
               save_all=True, duration=100, loop=0)
    

def create_map(markeri, tip="", response=None, optional=""):

    if response is not None:
        upute_cm = response
        bounds = [list(min(upute_cm)), list(max(upute_cm))]
    else:
        bounds = [list(min(markeri)), list(max(markeri))]
    m = folium.Map(location=[44.5, 16.5], fit_bounds=bounds, zoom_start=7)

    if tip == "directed":
    #TODO: Napraviti listu
        folium.PolyLine(locations=markeri, weight=3, opacity=0.7).add_to(m)
    else:
        folium.PolyLine(locations=upute_cm, weight=3, opacity=0.7).add_to(m)
    name = len(markeri)
    # if response is not None:
    #     for i in range(0, len(markeri)-1, 1):
    #         if i == 0:
    #             folium.Marker(
    #                location=markeri[i],
    #                popup=folium.Popup(max_width=450, html="Start/End"),
    #                icon=BeautifyIcon(icon_shape="marker", text_color="red", border_color="red", number=i)).add_to(m)
    #             # icon=folium.Icon(color='red', icon="home")
    #         else:
    #             # folium.Marker(
    #             #     location=markeri[i],
    #             #     popup=folium.Popup(max_width=450)).add_to(m)
    #             folium.Marker(location=markeri[i], icon=BeautifyIcon(icon_shape="marker", number=i)).add_to(m)
    # return m
    if optional is 'Save':
        if response is None:
            # m = create_map(markeri, tip)
            # m.save('./route_map_{}.html'.format(name))
            img_data = m._to_png(0)
            img = Image.open(io.BytesIO(img_data))
            img.save('mapa_{}.png'.format(name))
            img.close()
        else:
            # m = create_map(data, markeri, tip)
            # m.save('./route_map_{}.html'.format(name))
            img_data = m._to_png(0)
            img = Image.open(io.BytesIO(img_data))
            img.save('mapa_{}.png'.format(name))
            img.close()


def gradovi_listed(f):
    # file = 'som/src/hr556.tsp'
    # file = 'gradoviCSV.csv'
    file = f
    gradovi = {}
    if file.endswith('.csv'):
        with open(file, mode='r', encoding='utf-8') as infile:
            sve = infile.read()
            redovi = sve.split('\n')

            for i in range(len(redovi)):
                # print(redovi[i].split(';')[4].strip('°E'))
                k1 = redovi[i].split(';')[4].strip('°E')
                k2 = redovi[i].split(';')[3].strip('°N')
                g = redovi[i].split(';')[0]
                gradovi[g] = [float(k1), float(k2)]
            koordinate = list(gradovi.values())
            # koordinate = random.sample(list(gradovi.values()), 10)


    elif file.endswith('.tsp'):
        with open(file, mode='r', encoding='utf-8') as infile:
            bulk = infile.read().split('\n')

            for i in range(7, len(bulk)-1, 1):
                k1 = bulk[i].split(' ')[2]
                k2 = bulk[i].split(' ')[1]
                g = bulk[i].split(' ')[0]
                gradovi[g] = [float(k1), float(k2)]
            # koordinate = random.sample(list(gradovi.values()), 10)
            koordinate = list(gradovi.values())
    else:
        print('Unknown data format!')
        exit()

    return koordinate




def data_flipper(data):
    arr = np.array(data)
    flipped = np.fliplr(arr)
    to_list = flipped.tolist()
    r = list(map(tuple, to_list))
    return r


def map_plotter(markeri, data, tip):
    #TODO: maknuti map plotter funkciju
    if data is None:
        m = create_map(markeri, tip)
        m.save('./route_map_{}.html'.format(tip))
        img_data = m._to_png(1)
        img = Image.open(io.BytesIO(img_data))
        img.save('mapa_{}.png'.format(tip))
    else:
        m = create_map(data, markeri, tip)
        m.save('./route_map_{}.html'.format(tip))
        img_data = m._to_png(1)
        img = Image.open(io.BytesIO(img_data))
        img.save('mapa_{}.png'.format(tip))


def total_distance(indexes, dist_mat):
    total = 0
    for i in range(len(indexes)):
        if i < len(indexes) - 1:
            total += dist_mat[int(indexes[0])][int(indexes[i+1])]
        else:
            # Add the distance from the last point to the first point
            total += dist_mat[int(indexes[0])][int(indexes[0])]
    return total

def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances
    # [END distance_callback]

def main():
    # f = 'gradoviCSV.csv'
    f = 'som/src/hr.tsp'
    popis = gradovi_listed(f)
    ma_t = [tuple(l) for l in popis]
    ma = compute_euclidean_distance_matrix(popis)
    # if f.endswith('.csv'):
    #     # d = json.loads(OSM_matrix(popis))['distances']
    #     distance_matrix = dm(popis, popis, p=2).tolist()
    #     # print(distance_matrix)

    # elif f.endswith('.tsp'):
    #     # distance_matrix = list(dm(popis, popis))
    #     distance_matrix = dm(popis, popis, p=2).tolist()
    # else:
    #     print('Incorrect data format')
    #     exit()
    # print()
    """
    Atributi: 
        - distances -> vraca vrijednost u metrima [m]
        - durations -> vraca vrijednost u sekundama [s]
    """
    #Poziv goTools-a
    c = solution_master(ma_t)
    print(c)
    # c = "Route for vehicle 0:\n0 -> 7 -> 6 -> 8 -> 9 -> 4 -> 3 -> 5 -> 2 -> 1 -> 0\nRoute distance: 75768 miles"
    f = c.split('\n')
    indeksi = f[1].replace(' -> ', ',').split(',')
    ind = np.array(indeksi)
    lista = []

    for i in indeksi:
        lista.append(popis[int(i)])
    # total = total_distance(ind, distance_matrix)
    # print(total)
    # upute = json.loads(josm_direction_manager(lista))
    markeri = data_flipper(lista)
    # print(upute['features'][0]['geometry']['coordinates'])
    # data = data_flipper(upute['features'][0]['geometry']['coordinates'])

    create_map(markeri, tip='directed', optional='Save')

    #TODO: Napisati funkciju koja mjeri vrijeme izračuna za GoogleOR i SOM
    #TODO: Napraviti usporedbu rezultata

# env = DeliveryEnvironment(n_stops = 20, method = "distance")
#
# agent = DeliveryQAgent(env.observation_space, env.action_space)
# # run_episode(env, agent)
# run_n_episodes(env, agent, "training_10_stops.gif")
# env.render()
#
# create_data_model()


if __name__ == '__main__':
    main()
