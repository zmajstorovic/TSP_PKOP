import gotools
import time
import numpy as np
import som.src.main as som
import csv
import matplotlib.pyplot as  plt

st = 10
pr = []

for st in range(10, 100, 10):
    pr.append(st)
for st in range(100, 1000, 100):
    pr.append(st)
for st in range(1000, 5500, 500):
    pr.append(st)



def csv_writer(data_entry, option):


    header = ["RBr", "Problem_size", "[D]Global_alg", "[T]Global_alg", "[D] Christofides", "[T] Christofides", "[D]SimAnnealing", "[T]SimAnnealing", "[D]SOM", "[T]SOM"]
    data = data_entry

    with open('countries.csv', 'a', encoding='UTF8', newline='') as f:

        writer = csv.writer(f)
        if option is 'header':
            # write the header
            writer.writerow(header)
            # write the data
        writer.writerow(data)



# problem_size = 800

with open('10k.tsp', mode='r', encoding='utf-8') as infile:
    bulk = infile.read().split('\n')
    gradovi = {}
    for i in range(7, len(bulk) - 1, 1):
        k1 = bulk[i].split(' ')[2]
        k2 = bulk[i].split(' ')[1]
        g = bulk[i].split(' ')[0]
        # gradovi[g] = [math.trunc(float(k1)*100), math.trunc(float(k2)*100)]
        gradovi[g] = [int(k1), int(k2)]
    k = list(gradovi.values())
    # for items in k:
    #     print(math.trunc(items[0]*100))

    koordinate = [tuple(l) for l in k]
x, y =[], []
koordinate[0]
for p in pr:
    print(koordinate[0:p])
    a = koordinate[0:p]
    x, y = zip(*a)
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y)
    plt.title(str(p)+' lokacija')
    # plt.show()
    plt.savefig('C:\\Users\\zmajstorovic\\Documents\\QL_TSP\\Test_scenariji\\'+str(p)+'_lokacija.png')
    x, y = [], []
quit()

for problem_size in pr:



    #Pokreni gotools
    s = time.time()
    C_ortools_distance = gotools.main(problem_size, 'christofides')
    e = time.time()
    Cr_total = round(e-s, 2)
    print(f'OR Tools time {e-s}, distance {C_ortools_distance}')

    s = time.time()
    S_ortools_distance = gotools.main(problem_size, 'SimAnnealing')
    e = time.time()
    Sim_total = round(e-s, 2)
    print(f'OR Tools time {e-s}, distance {S_ortools_distance}')

    #global
    s = time.time()
    glo_ortools_distance = gotools.main(problem_size, 'GlobalCheapest')
    e = time.time()
    glo_total = round(e-s, 2)
    print(f'OR Tools time {e-s}, distance {glo_ortools_distance}')

    s = time.time()
    SOM_distance = som.main(problem_size)
    e = time.time()
    s_total = round(e-s, 2)
    print(f'SOM time {e-s}, distance {SOM_distance}')

    if pr.index(problem_size)+1 != 1:
        csv_writer([pr.index(problem_size)+1, problem_size, glo_ortools_distance, glo_total,
                    C_ortools_distance, Cr_total, S_ortools_distance, Sim_total, int(SOM_distance),
                    round(s_total, 2)], option='x')
    else:
        csv_writer([pr.index(problem_size)+1, problem_size,  glo_ortools_distance, glo_total,
                    C_ortools_distance, Cr_total, S_ortools_distance, Sim_total, int(SOM_distance),
                    round(s_total, 2)], option='header')



