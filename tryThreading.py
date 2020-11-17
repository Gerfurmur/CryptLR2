import threading
import math
import shaXX


bytesize = 8
zero_code = 48
table = {1: 64, 2: 32, 3: 16, 4: 8, 5: 4, 6: 2, 7: 1}
size_rho_attack = 0
result = None


class MyThread(threading.Thread):
    number_threads = 2
    sha_size = 16
    zero_bytes_num_for_pb = 1
    s = [[], []]

    def __init__(self, num):
        super().__init__(daemon=True)
        self.num = num
        self.y_0 = shaXX.generate()
        self.iter_num = 0
        self.y_i = self.y_0
        self.found_pair = None
        self.found_p_lst_num = None
        MyThread.q = int(MyThread.sha_size/2 - math.log2(MyThread.number_threads))

    def pb(self, y_i):
        return bytes(MyThread.zero_bytes_num_for_pb) + y_i

    def compare(self):
        number_bytes_comparing = (MyThread.q // bytesize)
        table_eq = MyThread.q % bytesize
        for byte in range(number_bytes_comparing):
            if bin(self.y_i[byte]) != bin(0):
                return False
        if table_eq != 0:
            if len(bin(self.y_i[MyThread.q // bytesize])) > len(bin(table[table_eq])):
                return False
        return True

    def found(self):
        y = None
        z = None
        if MyThread.s != [[], []]:
            if self.found_pair[1] > self.iter_num:
                d = self.found_pair[1] - self.iter_num
                y = MyThread.s[self.found_p_lst_num][0][0]
                z = MyThread.s[self.num][0][0]
            else:
                d = self.iter_num - self.found_pair[1]
                y = MyThread.s[self.num][0][0]
                z = MyThread.s[self.found_p_lst_num][0][0]
            for i in range(d):
                y = self.pb(shaXX.get(y, MyThread.sha_size))
            while self.pb(shaXX.get(y, MyThread.sha_size)) != self.pb(shaXX.get(z, MyThread.sha_size)):
                y = self.pb(shaXX.get(y, MyThread.sha_size))
                z = self.pb(shaXX.get(z, MyThread.sha_size))
            return y, z

    def run(self):
        global size_rho_attack, result
        while not isinstance(result, tuple):
            self.iter_num += 1
            self.y_i = self.pb(shaXX.get(self.y_i, MyThread.sha_size))
            if not self.compare():
                continue
            for element in MyThread.s[self.num]:
                if self.y_i == element[0]:
                    self.found_pair = element
                    self.found_p_lst_num =  self.num
                    result = self.found()
            MyThread.s[self.num].append((self.y_i, self.iter_num))
            size_rho_attack += (self.y_i, self.iter_num).__sizeof__()


def attack(sha_size=16):
    global result, size_rho_attack
    result = None
    size_rho_attack = 0
    MyThread.sha_size = sha_size
    MyThread.s = [[], []]
    thread1 = MyThread(0)
    thread2 = MyThread(1)
    thread1.start()
    thread2.start()
    thread1.join(2)
    thread2.join(2)
    return result
'''
for i in range(100):
    print(i)
    print("result", attack(sha_size=20))
    print(size_rho_attack)'''