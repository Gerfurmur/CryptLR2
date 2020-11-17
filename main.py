from datetime import datetime
import birthday_attack
#import rho_attack
import tryThreading as rho_attack
import numpy as np
import matplotlib.pyplot as plt


collision_quantity = 200
xx_start = 15
xx_end = 21


rng = np.arange(xx_end - xx_start)
bits_number = xx_start + rng


def save(name='', fmt='png'):
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')


def br_attack():
    times = [0]*(xx_end - xx_start)
    memories = [0]*(xx_end - xx_start)
    collisions = [[] for i in range(xx_end - xx_start)]
    for xx in range(xx_start, xx_end):
        for i in range(collision_quantity):
            start_time = datetime.now()
            col = birthday_attack.attack(xx)
            end_time = datetime.now()
            collisions[xx - xx_start].append((col[0].hex(), col[1].hex()))
            times[xx - xx_start] += (end_time - start_time).microseconds
            memories[xx - xx_start] += birthday_attack.size_br_attack
        times[xx - xx_start] /= collision_quantity
        memories[xx - xx_start] /= collision_quantity
    print("birthday attack collisions:", collisions)
    print("birthday attack average time of searching:", times)
    print("birthday attack average memory cost:", memories)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.stackplot(bits_number, times)
    ax.set_title('Birthday attack time chart')
    ax.set_ylabel('Time, mcs')
    ax.set_xlim(xmin=bits_number[0], xmax=bits_number[-1])
    fig.tight_layout()
    save(name='Birthday attack time chart', fmt='png')
    plt.show()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.stackplot(bits_number, memories)
    ax.set_title('Birthday attack memory chart')
    ax.set_ylabel('Memory, bytes')
    ax.set_xlim(xmin=bits_number[0], xmax=bits_number[-1])
    fig.tight_layout()
    save(name='Birthday attack memory chart', fmt='png')
    plt.show()
    with open('birthday_attack_collisions.txt', 'w') as write_file:
        for xx in range(xx_end - xx_end, xx_end - xx_start):
            part = "Out bits shaXX number = " + str(xx + xx_start)
            part += "\n----------------------------------------------\n"
            write_file.write(part)
            for i in range(collision_quantity):
                string = "Collision number " + str(i + 1) + ": " + str(collisions[xx][i]) + "\n"
                write_file.write(string)


def rho_pl_attack():
    times = [0]*(xx_end - xx_start)
    memories = [0]*(xx_end - xx_start)
    collisions = [[] for i in range(xx_end - xx_start)]
    for xx in range(xx_start, xx_end):
        for i in range(collision_quantity):
            start_time = datetime.now()
            col = rho_attack.attack(xx)
            while col is None:
                start_time = datetime.now()
                col = rho_attack.attack(xx)
            end_time = datetime.now()
            collisions[xx - xx_start].append((col[0].hex(), col[1].hex()))
            times[xx - xx_start] += (end_time - start_time).microseconds
            memories[xx - xx_start] += rho_attack.size_rho_attack
        times[xx - xx_start] /= collision_quantity
        memories[xx - xx_start] /= collision_quantity
    print("rho attack collisions:", collisions)
    print("rho attack average time of searching:", times)
    print("rho attack average memory cost:", memories)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.stackplot(bits_number, times)
    ax.set_title('Rho Pollard attack time chart')
    ax.set_ylabel('Time, mcs')
    ax.set_xlim(xmin=bits_number[0], xmax=bits_number[-1])
    fig.tight_layout()
    save(name='Rho Pollard attack time chart', fmt='png')
    plt.show()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.stackplot(bits_number, memories)
    ax.set_title('Rho Pollard attack memory chart')
    ax.set_ylabel('Memory, bytes')
    ax.set_xlim(xmin=bits_number[0], xmax=bits_number[-1])
    fig.tight_layout()
    save(name='Rho Pollard attack memory chart', fmt='png')
    plt.show()
    with open('rho_pollard_attack_collisions.txt', 'w') as write_file:
        for xx in range(xx_end - xx_end, xx_end - xx_start):
            part = "Out bits shaXX number = " + str(xx + xx_start)
            part += "\n----------------------------------------------\n"
            write_file.write(part)
            for i in range(collision_quantity):
                string = "Collision number " + str(i + 1) + ": " + str(collisions[xx][i]) + "\n"
                write_file.write(string)


def main():
    br_attack()
    rho_pl_attack()


if __name__ == "__main__":
    main()
