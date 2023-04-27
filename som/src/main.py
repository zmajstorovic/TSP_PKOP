from sys import argv
import numpy as np
from io_helper import read_tsp, normalize
from neuron import generate_network, get_neighborhood, get_route
from distance import select_closest, euclidean_distance, route_distance
from plot import plot_network, plot_route
import folium
import io
from PIL import Image
import matplotlib.pyplot as plt



def novi_plot(route):
    koordinate = []
    gradovi = {}
    with open('10k.tsp', mode='r', encoding='utf-8') as infile:
        bulk = infile.read().split('\n')
        for i in range(7, len(bulk) - 1, 1):
            k1 = bulk[i].split(' ')[1]
            k2 = bulk[i].split(' ')[2]
            g = bulk[i].split(' ')[0]
            gradovi[int(g)] = [float(k1), float(k2)]

        # koordinate = random.sample(list(gradovi.values()), 10)
        # koordinate = list(gradovi.values())
    grad = []
    #stvori parove
    for r in route:
        if(int(r)-1==0):
            koordinate.append([gradovi[int(279)], gradovi[int(r)]])
        else:
            koordinate.append([gradovi[int(r)-1], gradovi[int(r)]])

    #TODO: složiti listu koordinata za folium
    bounds = [list(min(koordinate)), list(max(koordinate))]
    m = folium.Map(location=[44.5, 16.5], fit_bounds=bounds, zoom_start=7)
    for k in range(0, len(koordinate)-1, 1):
        # print(koordinate[k:k+2])
        print(koordinate[k])
        folium.PolyLine(locations=koordinate[k], weight=3, opacity=0.7).add_to(m)
        # m.save('./route_map_{}.html'.format(tip))

    img_data = m._to_png(1)
    img = Image.open(io.BytesIO(img_data))
    img.save('SOM_route.png')

def nx_net(redoslijed):
    def tsp_read():
        with open('10k.tsp', mode='r', encoding='utf-8') as infile:
            bulk = infile.read().split('\n')
            gradovi={}
            for i in range(7, len(bulk)-1, 1):
                k1 = bulk[i].split(' ')[2]
                k2 = bulk[i].split(' ')[1]
                g = bulk[i].split(' ')[0]
                gradovi[g] = [int(k1), int(k2)]
            k = list(gradovi.values())
            koordinate = [tuple(l) for l in k]
        return koordinate
    lokacije = tsp_read()
    tmp = redoslijed.copy()
    redoslijed.append(tmp[0])
    # lokacije = [
    #     (288, 149), (288, 129), (270, 133), (256, 141), (256, 157), (246, 157),
    #     (236, 169), (228, 169), (228, 161), (220, 169), (212, 169), (204, 169),
    #     (196, 169), (188, 169), (196, 161), (188, 145), (172, 145), (164, 145),
    #     (156, 145), (148, 145), (140, 145), (148, 169), (164, 169), (172, 169),
    #     (156, 169), (140, 169), (132, 169), (124, 169), (116, 161), (104, 153),
    #     (104, 161), (104, 169), (90, 165), (80, 157), (64, 157), (64, 165),
    #     (56, 169), (56, 161), (56, 153), (56, 145), (56, 137), (56, 129),
    #     (56, 121), (40, 121), (40, 129), (40, 137), (40, 145), (40, 153),
    #     (40, 161), (40, 169), (32, 169), (32, 161), (32, 153), (32, 145),
    #     (32, 137), (32, 129), (32, 121), (32, 113), (40, 113), (56, 113),
    #     (56, 105), (48, 99), (40, 99), (32, 97), (32, 89), (24, 89),
    #     (16, 97), (16, 109), (8, 109), (8, 97), (8, 89), (8, 81),
    #     (8, 73), (8, 65), (8, 57), (16, 57), (8, 49), (8, 41),
    #     (24, 45), (32, 41), (32, 49), (32, 57), (32, 65), (32, 73),
    #     (32, 81), (40, 83), (40, 73), (40, 63), (40, 51), (44, 43),
    #     (44, 35), (44, 27), (32, 25), (24, 25), (16, 25), (16, 17),
    #     (24, 17), (32, 17), (44, 11), (56, 9), (56, 17), (56, 25),
    #     (56, 33), (56, 41), (64, 41), (72, 41), (72, 49), (56, 49),
    #     (48, 51), (56, 57), (56, 65), (48, 63), (48, 73), (56, 73),
    #     (56, 81), (48, 83), (56, 89), (56, 97), (104, 97), (104, 105),
    #     (104, 113), (104, 121), (104, 129), (104, 137), (104, 145), (116, 145),
    #     (124, 145), (132, 145), (132, 137), (140, 137), (148, 137), (156, 137),
    #     (164, 137), (172, 125), (172, 117), (172, 109), (172, 101), (172, 93),
    #     (172, 85), (180, 85), (180, 77), (180, 69), (180, 61), (180, 53),
    #     (172, 53), (172, 61), (172, 69), (172, 77), (164, 81), (148, 85),
    #     (124, 85), (124, 93), (124, 109), (124, 125), (124, 117), (124, 101),
    #     (104, 89), (104, 81), (104, 73), (104, 65), (104, 49), (104, 41),
    #     (104, 33), (104, 25), (104, 17), (92, 9), (80, 9), (72, 9),
    #     (64, 21), (72, 25), (80, 25), (80, 25), (80, 41), (88, 49),
    #     (104, 57), (124, 69), (124, 77), (132, 81), (140, 65), (132, 61),
    #     (124, 61), (124, 53), (124, 45), (124, 37), (124, 29), (132, 21),
    #     (124, 21), (120, 9), (128, 9), (136, 9), (148, 9), (162, 9),
    #     (156, 25), (172, 21), (180, 21), (180, 29), (172, 29), (172, 37),
    #     (172, 45), (180, 45), (180, 37), (188, 41), (196, 49), (204, 57),
    #     (212, 65), (220, 73), (228, 69), (228, 77), (236, 77), (236, 69),
    #     (236, 61), (228, 61), (228, 53), (236, 53), (236, 45), (228, 45),
    #     (228, 37), (236, 37), (236, 29), (228, 29), (228, 21), (236, 21),
    #     (252, 21), (260, 29), (260, 37), (260, 45), (260, 53), (260, 61),
    #     (260, 69), (260, 77), (276, 77), (276, 69), (276, 61), (276, 53),
    #     (284, 53), (284, 61), (284, 69), (284, 77), (284, 85), (284, 93),
    #     (284, 101), (288, 109), (280, 109), (276, 101), (276, 93), (276, 85),
    #     (268, 97), (260, 109), (252, 101), (260, 93), (260, 85), (236, 85),
    #     (228, 85), (228, 93), (236, 93), (236, 101), (228, 101), (228, 109),
    #     (228, 117), (228, 125), (220, 125), (212, 117), (204, 109), (196, 101),
    #     (188, 93), (180, 93), (180, 101), (180, 109), (180, 117), (180, 125),
    #     (196, 145), (204, 145), (212, 145), (220, 145), (228, 145), (236, 145),
    #     (246, 141), (252, 125), (260, 129), (280, 133)]
    x, y = [], []
    # Presloži listu
    for i in redoslijed:
        x.append(lokacije[int(i)][0])
        y.append(lokacije[int(i)][1])
    # x.append(lokacije[0][0])
    # y.append(lokacije[0][1])
    for i in range(0, len(x), 1):
        plt.plot(x[i:i + 2], y[i:i + 2], 'r.-')
    # plt.plot(x[0], y[0], 'y.-')
    plt.show()

def main(pr_size):
    # if len(argv) != 2:
    #     print("Correct use: python src/main.py <filename>.tsp")
    #     return -1

    # problem1 = read_tsp('hr556.tsp')
    problem = read_tsp('10k.tsp')

    route = som(problem[0:pr_size], 100000)

    problem = problem.reindex(route)

    distance = route_distance(problem)

    # novi_plot(problem['city'])
    # print(problem['winner'])

    print('Route found of length {}'.format(distance))
    return distance

def som(problem, iterations, learning_rate=0.8):
    """Solve the TSP using a Self-Organizing Map."""

    # Obtain the normalized set of cities (w/ coord in [0,1])
    cities = problem.copy()

    cities[['x', 'y']] = normalize(cities[['x', 'y']])

    # The population size is 8 times the number of cities
    n = cities.shape[0] * 8

    # Generate an adequate network of neurons:
    network = generate_network(n)
    print('Network of {} neurons created. Starting the iterations:'.format(n))

    for i in range(iterations):
        if not i % 100:
            print('\t> Iteration {}/{}'.format(i, iterations), end="\r")
        # Choose a random city
        city = cities.sample(1)[['x', 'y']].values
        winner_idx = select_closest(network, city)
        # Generate a filter that applies changes to the winner's gaussian
        gaussian = get_neighborhood(winner_idx, n//10, network.shape[0])
        # Update the network's weights (closer to the city)
        network += gaussian[:,np.newaxis] * learning_rate * (city - network)
        # Decay the variables
        learning_rate = learning_rate * 0.99997
        n = n * 0.9997

        # Check for plotting interval
        if not i % 1000:
            plot_network(cities, network, name='diagram/'+str(i)+'_'+str(len(cities))+'.png')

        # Check if any parameter has completely decayed.
        if n < 1:
            print('Radius has completely decayed, finishing execution',
            'at {} iterations'.format(i))
            break
        if learning_rate < 0.001:
            print('Learning rate has completely decayed, finishing execution',
            'at {} iterations'.format(i))
            break
    else:
        print('Completed {} iterations.'.format(iterations))

    plot_network(cities, network, name='diagram/final_'+str(len(cities))+'.png')

    red = []
    route = get_route(cities, network)
    for r in route:
        red.append(r)
    # print(red)

    plot_route(cities, route, 'diagram/route_'+str(len(cities))+'.png')
    # nx_net(red)
    return route

if __name__ == '__main__':
    main(1)
