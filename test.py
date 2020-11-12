#from pwn import *
import json
import logging
import timeit
from ScanBUG import  Heap
from ScanBUG import  Format
from ScanBUG import  ArbRW
from ScanBUG import  Stack
from ScanBUG import  Resgs
import multiprocessing
import os
import sys
import io

one_min = 60
fmt_vulnerability = Format.Check_format_string
arbitrary_RW_vulnerability = ArbRW.Check_arbitrary_RW
stack_overflow = Stack.Check_StackOverflow
heap_vulnerability = Heap.Check_heap
error_regs = Resgs.Check_regs_error

def path_msg(inlist, type):
    for indir in inlist:
        print("\n------------------------", type, "------------------------")
        if "over_num" in indir:
            print("[over bytes]:", indir["over_num"])
        if "stdout" in indir:
            print("[stdout]:\n", indir["stdout"])
        if "stdin" in indir:
            print("[stdin]:\n", indir["stdin"])
        if "chain" in indir:
            print("[jump chain]:\n", indir["chain"])
        if "argv" in indir:
            print("[argv]:\n", indir["argv"])
        print()

class RedirectStdout:
    def __init__(self):
        self.content = ''  #保存输出文本
        self.savedStdout = sys.stdout  #保存输出模式
        self.memObj, self.fileObj, self.nulObj = None, None, None

    # 外部的print语句将执行本write()方法，并由当前sys.stdout输出
    def write(self, outStr):
        # self.content.append(outStr)
        self.content += outStr

    def toCons(self):  # 标准输出重定向至控制台
        sys.stdout = self.savedStdout  # sys.__stdout__

    def toMemo(self):  # 标准输出重定向至内存
        self.memObj = io.StringIO()
        sys.stdout = self.memObj

    def toFile(self, file='out.txt'):  # 标准输出重定向至文件
        self.fileObj = open(file, 'a+', 1)  # 改为行缓冲
        sys.stdout = self.fileObj

    def toMute(self):  # 抑制输出
        self.nulObj = open(os.devnull, 'w')
        sys.stdout = self.nulObj

    def restore(self):  #重置状态
        self.content = ''
        if self.memObj.closed != True:
            self.memObj.close()
        if self.fileObj.closed != True:
            self.fileObj.close()
        if self.nulObj.closed != True:
            self.nulObj.close()
        sys.stdout = self.savedStdout  # sys.__stdout__

# 默认不限制时间
def find_stack_repeat(filename,argv,entry_addr,limit=None):
    logging.getLogger("requests").setLevel(logging.WARNING)
    redirObj = RedirectStdout()
    redirObj.toMute()
    stack_overflow(filename, args=argv, start_addr=entry_addr, limit=limit)

#任意地址读写
def find_arbitrary_repeat(filename,argv,entry_addr,limit=None):
    logging.getLogger("requests").setLevel(logging.WARNING)
    redirObj = RedirectStdout()
    redirObj.toMute()
    arbitrary_RW_vulnerability(filename,args=argv,start_addr=entry_addr,limit=limit)

# 默认不限制时间
def find_error_regs(filename,argv,entry_addr,limit=None):
    logging.getLogger("requests").setLevel(logging.WARNING)
    redirObj = RedirectStdout()
    redirObj.toMute()
    error_regs(filename, args=argv, start_addr=entry_addr, limit=limit)

# 默认不限制时间
def find_format(filename,argv,entry_addr,limit=None):
    logging.getLogger("requests").setLevel(logging.WARNING)
    redirObj = RedirectStdout()
    redirObj.toMute()
    fmt_vulnerability(filename, args=argv, start_addr=entry_addr, limit=limit)

# 默认不限制时间
def find_heap_vul(filename,argv,entry_addr,limit=None):
    logging.getLogger("requests").setLevel(logging.WARNING)
    redirObj = RedirectStdout()
    redirObj.toMute()
    heap_vulnerability(filename, args=argv, start_addr=entry_addr, limit=limit)

def find_heap_vul_msg(limit=20):
    p = multiprocessing.Process(target=find_heap_vul, args=(limit,))  #
    p.start()
    limit_time = limit * one_min
    p.join(limit_time)
    if p.is_alive():
        print("[-] runing over limit time,kill it")
        p.terminate()
    p.join()

    fp = None
    try:
        fp = open("tmp.json", "r+")
    except:
        print("find nothing in heap vulnerability!")
        return

    uaf_R_result = []
    uaf_W_result = []
    double_free_result = []
    error_free_result = []
    while True:
        str_line = fp.readline()
        if str_line:
            # print(bytes(str_line,"utf-8"))
            json_str = json.loads(str_line)
            # print(type(json_str))
            for k in json_str:
                if k == "uaf_R_result":
                    uaf_R_result.append(json_str["uaf_R_result"])
                if k == "uaf_W_result":
                    uaf_W_result.append(json_str["uaf_W_result"])
                if k == "double_free_result":
                    double_free_result.append(json_str["double_free_result"])
                if k == "error_free_result":
                    error_free_result.append(json_str["error_free_result"])
        else:
            break
    fp.seek(0)
    # fp.truncate()
    fp.close()
    # os.system("rm tmp.json")

    print("\n[+]===has found", len(uaf_R_result), "uaf read===")
    path_msg(uaf_R_result, "uaf_R_result")
    print("\n[+]===has found", len(uaf_W_result), "uaf write===")
    path_msg(uaf_W_result, "uaf_W_result")
    print("\n[+]===has found", len(double_free_result), "double free===")
    path_msg(double_free_result, "double_free_result")
    print("\n[+]===has found", len(error_free_result), "error free ptr===")
    path_msg(error_free_result, "error_free_result")

def Test():
    pass

if __name__ == '__main__':

    #for i in range(0,1):
    filename = "./test/stack"
    argv = None
    entry_addr = None
    limit_time = 5 * 60
    start = timeit.default_timer()
    pool = multiprocessing.Pool(processes=5)
    pool.apply_async(find_stack_repeat, (filename, argv, entry_addr, limit_time))
    pool.apply_async(find_arbitrary_repeat, (filename, argv, entry_addr, limit_time))
    pool.apply_async(find_error_regs, (filename, argv, entry_addr, limit_time))
    pool.apply_async(find_format, (filename, argv, entry_addr, limit_time))
    pool.apply_async(find_heap_vul, (filename, argv, entry_addr, limit_time))
    # pool.apply_async(main)
    pool.close()
    pool.join()
    end = timeit.default_timer()
    print('Running time: %s Seconds' % (end - start))

