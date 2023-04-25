import gotools
import time
import numpy as np
import som.src.main as som
import csv

# def timer(state):
#     #start
#     duration = 0
#     if state is 'start':
#         start = time.time()
#     #stop
#     if state is 'stop':
#         stop = time.time()
#     #reset
#     if state is 'reset':
#         start, stop = 0, 0
#     if state is 'duration':
#         duration = start-stop
#         return duration
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



