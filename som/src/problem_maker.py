import random
n = 10000

with open('coordinates.tsp', 'w') as f:
    for i in range(1, n+1):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        f.write(f"{i} {x} {y}\n")
    f.write('EOF')
    f.close()
