import sys
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from collections import Counter
from sklearn import cluster, metrics
import socket
import signal
from random import sample, randint
import random
import xml.etree.ElementTree as ET
import mmap
import time
import math
import gc

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cluster_num = 10
valid_invalid_num = 10
exec=""
total_argv = []
fname = './pods.txt'
bitmap_size = 1 << 16
output_path = ""

cluster_num = 10
valid_invalid_num = 10

RECEIVE_MSG_LEN = 1000


evaluate_valid_num = []

def connect_to_fuzzer():
    print(f"[*] port = {PORT}")
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print("connect success")
    return conn, addr

def cal_means(k, bitmap):
    n = np.array(bitmap)
    c = cluster.MeanShift(bandwidth=k).fit(n)
    return c.labels_, max(c.labels_) + 1

def receive_argv(conn, addr):
    global exec
    print("=============")
    argv_count = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
    print(argv_count, type(argv_count), len(argv_count))
    
    ret = []
    for i in range(int(argv_count)):
        argv = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
        if(argv == "skip"):
            continue
        ret.append(argv.split(" "))
    
    argv_count = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
    print(argv_count)
    for i in range(int(argv_count)):
        argv = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
        print(argv)
        ret.append(argv.split(" "))

    argv_count = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
    print(argv_count)
    for i in range(int(argv_count)):
        argv = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
        print(argv)
        ret.append(argv.split(" "))
    print("=============")
    return ret

def get_path_file(path):
    ret = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for f in fileNames:
            ret.append(path + "/" +f)
    return ret

def exec_argv(file_name, cur_argv):
    tmp_bitmap_list = []
    real_bitmap_list = []
    total_bitmap = set()
    
    for argv in cur_argv:
        tmp = []
        argv_tmp = []
        for a in argv:
            argv_tmp.append(a.replace("@@", file_name))
        out = ""
        
        try:
            out = subprocess.check_output(['./afl-showmap', '-q', '-e', '-o', '/dev/stdout', '-m', 'none', '-t', '500'] + argv_tmp)
        except subprocess.CalledProcessError as e:
            print(e.returncode, e.cmd)

        for line in out.splitlines():
            edge = line.split(b':')[0]
            tmp.append(edge)
            total_bitmap.add(edge)
        tmp_bitmap_list.append(tmp)
    for item in tmp_bitmap_list:
        tmp = []
        for i in total_bitmap:
            if(i in item):
                tmp.append(1)
            else:
                tmp.append(0)
        real_bitmap_list.append(tmp)
    return real_bitmap_list


def print_argv():
    print(exec)
    for item in total_argv:
        print(item.argv, item.must)

def init_mmap():
    fd = open(fname, "r+b")
    mm = mmap.mmap(fd.fileno(), bitmap_size, access=mmap.ACCESS_WRITE, offset=0)
    print("mmap open")
    return fd, mm

def read_bitmap():
    print("read bitmap")
    mm.seek(0)
    ret = mm.readline()
    return ret

def cal_cluster(num):
    ret = []
    for i in range(len(num[0])):
        sum = 0
        for j in range(len(num)):
            sum = sum + num[j][i]
        ret.append(sum/len(num))
    return ret

def cal_cluster_valid(num):
    ret = []
    for i in range(len(num[0])):
        min = 1e9
        for j in range(len(num)):
            if(num[j][i] < min):
                min = num[j][i]
        ret.append(min)
    return ret

def cal_cluster_invalid(num):
    ret = []
    for i in range(len(num[0])):
        max = 0
        for j in range(len(num)):
            if(num[j][i] > max):
                max = num[j][i]
        ret.append(max)
    return ret
def cal_num(valid, invalid):
    print(valid, invalid)
    
    w = []
    for i in range(20):
        w.append(0)

    tmp = []
    for i in range(len(valid)):
        tmp.append(valid[i] - invalid[i])
        evaluate_valid_num.append(valid[i] / 3 * 2)

    grade = 20
    a = set()
    while grade > 0:
        max = -1e9
        index = -1
        for i in range(len(tmp)):
            if i in a:
                continue
            if(max < tmp[i]):
                max = tmp[i]
                index = i
        a.add(index)
        w[index] = w[index] + grade
        grade = grade - 1


    tmp = []
    for i in range(len(valid)):
        tmp.append(valid[i] / invalid[i])
    grade = 20
    a = set()
    while grade > 0:
        max = -1e9
        index = -1
        for i in range(len(tmp)):
            if i in a:
                continue
            if(max < tmp[i]):
                max = tmp[i]
                index = i

        w[index] = w[index] + grade
        a.add(index)
        grade = grade - 1
    print(w)
    
    max = -1e9
    index = -1
    for i in range(len(w)):
        if(max < w[i]):
            max = w[i]
            index = i
    
    with open("./argv_num_result", "w") as f:
        f.write(str(index+1))
        f.write(str(valid[index]/3*2))

    return index+1, valid[index] / 3 * 2 
    # for i in range(len(valid)-1, -1, -1):
        # if(valid[i] / 2 > invalid[i] and valid[i] < 30 and valid[i] > 10 and invalid[i] <= 10):
        # if(valid[i] / 2 > invalid[i] and valid[i] < 30):
            # return i+1, invalid[i]+1
    
    # for i in range(len(valid)):
        # if(valid[i] - invalid[i] >= 10 and valid[i] > 10 and invalid[i] < 10):
        # if(valid[i] - invalid[i] >= 10 and valid[i] / 2 > invalid[i]):
            # return i+1, 10


def init_cluster_parameter(conn, addr):
    global cluster_num
    global valid_invalid_num
    count_file = len(get_path_file(sys.argv[2])) + len(get_path_file(sys.argv[3]))
    file_list = get_path_file(sys.argv[2])

    k = 0
    group_num = 0
    valid = 1e9
    
    conn.send(str.encode(str(count_file)))
    # input()
    valid_num = []
    invalid_num = []
    for file in file_list:
        argv = receive_argv(conn, addr)
        total_bitmap = exec_argv(file, argv)
        tmp = []
        for i in range(1, 20):
            group, l= cal_means(i, total_bitmap)
            tmp.append(l)
            print("valid", l)
        valid_num.append(tmp)
        
        k = k + len(total_bitmap[0])
        group_num = group_num + l
        valid = min(valid, l)
        print(group, l)

        conn.send(str.encode("OK"))
    
    file_list = get_path_file(sys.argv[3])

    for file in file_list:
        argv = receive_argv(conn, addr)
        total_bitmap = exec_argv(file, argv)
        tmp = []
        for i in range(1, 20):
            group, l= cal_means(i, total_bitmap)
            tmp.append(l)
            print("invalid", l)
        invalid_num.append(tmp)
        k = k + len(total_bitmap[0])
        group_num = group_num + l
        valid = min(valid, l)
        print(group, l)


        conn.send(str.encode("OK"))
    
    # print(valid_num)
    cluster_num, valid_invalid_num = cal_num(cal_cluster_valid(valid_num), cal_cluster_invalid(invalid_num))
    
    # cluster_num, valid_invalid_num = 3, 5
    # cluster_num, valid_invalid_num = cal_num(cal_cluster(valid_num), cal_cluster(invalid_num))
    # print(invalid_num)
    # print(cal_cluster(invalid_num))

    # cluster_num = math.log2(k / len(file_list))
    # valid_invalid_num = valid
    print(cluster_num, valid_invalid_num)

exec_binary = ""
total_argv = []
class argv:
    def __init__(self, parameter, must):
        self.parameter = parameter
        self.must = must

def receive_all_argv(conn, addr):
    global total_argv
    global exec_binary
    global output_path

    exec_binary = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
    while(exec_binary == ""):
        exec_binary = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
    
    conn.send(str.encode("OK"))
    print(exec_binary)
    parameter_len = int(conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', ''))
    conn.send(str.encode("OK"))
    print(parameter_len)

    for i in range(parameter_len):
        parameter_count = int(conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', ''))
        conn.send(str.encode("OK"))

        tmp = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
        parameter_must = False
        conn.send(str.encode("OK"))
        if(tmp == "true"):
            parameter_must = True

        parameter = []
        for j in range(parameter_count):
            tmp = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
            conn.send(str.encode("OK"))
            parameter.append(tmp.split())

        total_argv.append(argv(parameter, parameter_must))
    
    output_path = conn.recv(RECEIVE_MSG_LEN).decode("utf-8").replace('\x00', '')
    conn.send(str.encode("OK"))


def random_cluster_argv(num, cur):
    global total_argv
    global exec_binary
    tmp = []
    tmp.append(exec_binary)
    # print(num, cur)
    if(num == 1):
        for i in range(len(total_argv)):
            if(i == cur or total_argv[i].must == True):
                t = random.sample(total_argv[i].parameter, 1)
                for item in t[0]:
                    tmp.append(item)
        return tmp
    elif (num >= 2):
        count = 0
        for i in range(len(total_argv)):
            r = random.randint(0, len(total_argv))
            if(total_argv[i].must == True):
                t = random.sample(total_argv[i].parameter, 1)
                for item in t[0]:
                    tmp.append(item)
            elif(r <= num and count < num):
                count = count + 1
                t = random.sample(total_argv[i].parameter, 1)
                for item in t[0]:
                    tmp.append(item)
        return tmp

def gen_ran_argv():
    l = len(total_argv)
    total = []
    for i in range(l):
        total.append(random_cluster_argv(1, i))
    count = l #random.randint(l, 2*l)
    for i in range(count):
        total.append(random_cluster_argv(2, i))
    count = l #random.randint(1, l)
    for i in range(count):
        total.append(random_cluster_argv(3, i))
    return total

def check_file(file_list, total):
    for item in file_list:
        if(item not in total):
            return False
    return True
if __name__ == "__main__":
    conn, addr = connect_to_fuzzer()
    # fd, mm = init_mmap()
    init_cluster_parameter(conn, addr)
    
    receive_all_argv(conn, addr)
        
    gc.collect()

    # print(total_argv) 
    # for item in total_argv:
        # print(item.parameter)
        # print(item.must)

    out_path = output_path + "/queue"
    seed_path = output_path + "/seed_info"
    output_path = os.path.abspath(output_path)
    print(output_path)
    total_seed = set()
    sort_flag = False

    for i in range(20):
        os.mkdir(str(i), 0755)
        evaluate_path = output_path + "/" + str(i) + "/"

        count = 0
        cluster_num = i + 1
        valid_invalid_nume = valuate_valid_num[i]

        while True:
            if count == 1050:
                break;
            count = count + 1
            file_list = get_path_file(out_path)
            file_set = set()

            file_list.sort()

            for item in file_list:
                if item in total_seed:
                    continue
                total_seed.add(item)
                argv = gen_ran_argv()
                bitmap = exec_argv(item, argv)
                group, l = cal_means(cluster_num, bitmap)
                print(item)
                print(group, l)
                
                argv_group = {}
                for i in range(len(group)):
                    if argv_group.get(group[i]) is not None:
                        argv_group[group[i]].append(i)
                    else: 
                        argv_group[group[i]] = [i]

                print(argv_group)
                filename_list = item.split("/")
                filename = filename_list[len(filename_list) - 1]
                evaluate_path = evaluate_path + filename
                result_path = output_path + "/seed_info/" + filename
                argv_path = output_path + "/seed_argv/" + filename
                with open(result_path, "w") as f:
                    if (l >= valid_invalid_num):
                        f.write("1")
                    else:
                        f.write("0")

                with open(evaluate_path, "w") as f:
                    if (l >= valid_invalid_num):
                        f.write("1")
                    else:
                        f.write("0")
                # if(l >= valid_invalid_num):
                with open(argv_path, "w") as f:
                    f.write(str(l))
                    f.write("\n")
                    for key in argv_group.keys():
                        f.write(str(len(argv_group[key])))
                        f.write("\n")
                        for value in argv_group[key]:
                            f.write(str(len(argv[value])))
                            f.write(" ")
                            for i in argv[value]:
                                t = i.replace("@@", output_path + "/.cur_input")
                                f.write(t)
                                f.write(" ")
                            f.write("\n")    
                # update set
                for a in argv:
                    del a
                del argv
                for b in bitmap:
                    del b
                # for key in argv_group:
                    # del argv_group[key]
                del argv_group
                del bitmap
                del group 

                gc.collect()
