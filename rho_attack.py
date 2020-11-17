import threading
import math
import shaXX


bytesize = 8
zero_code = 48
table = {1: 64, 2: 32, 3: 16, 4: 8, 5: 4, 6: 2, 7: 1}
size_rho_attack = 0


class MyThread():
    number_threads = 2
    sha_size = 16
    zero_bytes_num_for_pb = 1
    s = [[], []]

    def __init__(self):
        self.num = [i for i in range(MyThread.number_threads)]
        self.y_0 = [shaXX.generate() for i in range(MyThread.number_threads)]
        self.iter_num = [0]*MyThread.number_threads
        self.y_i = self.y_0
        self.found_pair = None
        self.found_p_lst_num = None
        MyThread.q = int(MyThread.sha_size/2 - math.log2(MyThread.number_threads))

    def pb(self, y_i):
        return y_i + bytes(MyThread.zero_bytes_num_for_pb)

    def compare(self, thread):
        number_bytes_comparing = (MyThread.q // bytesize)
        table_eq = MyThread.q % bytesize
        for byte in range(number_bytes_comparing):
            if bin(self.y_i[thread][byte]) != bin(0):
                return False
        if table_eq != 0:
            if len(bin(self.y_i[thread][MyThread.q // bytesize])) != len(bin(table[table_eq])):
                return False
        return True

    def found(self, thread):
        y = None
        z = None
        if MyThread.s != [[], []]:
            if self.found_pair[1] > self.iter_num[thread]:
                d = self.found_pair[1] - self.iter_num[thread]
                y = MyThread.s[self.found_p_lst_num][0][0]
                z = MyThread.s[thread][0][0]
            else:
                d = self.iter_num[thread] - self.found_pair[1]
                y = MyThread.s[thread][0][0]
                z = MyThread.s[self.found_p_lst_num][0][0]
            for i in range(d):
                y = self.pb(shaXX.get(y, MyThread.sha_size))
            while self.pb(shaXX.get(y, MyThread.sha_size)) != self.pb(shaXX.get(z, MyThread.sha_size)):
                y = self.pb(shaXX.get(y, MyThread.sha_size))
                z = self.pb(shaXX.get(z, MyThread.sha_size))
            return y, z

    def run(self):
        global size_rho_attack
        while True:
            for thread in range(MyThread.number_threads):
                self.iter_num[thread] += 1
                self.y_i[thread] = self.pb(shaXX.get(self.y_i[thread], MyThread.sha_size))
                if not self.compare(thread):
                    continue
                for lst_num in range(MyThread.number_threads):
                    for element in MyThread.s[lst_num]:
                        if self.y_i == element[0]:
                            self.found_pair = element
                            self.found_p_lst_num = lst_num
                            return self.found(thread)
                MyThread.s[thread].append((self.y_i[thread], self.iter_num[thread]))
                size_rho_attack += (self.y_i[thread], self.iter_num[thread]).__sizeof__()


def attack(sha_size=16):
    global size_rho_attack
    result = None
    size_rho_attack = 0
    MyThread.sha_size = sha_size
    MyThread.s = [[], []]
    thread1 = MyThread()
    result = thread1.run()
    return result

for i in range(2):
    print(i)
    print("result", attack())
    print(size_rho_attack)