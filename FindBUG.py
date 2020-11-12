#!/usr/bin/env python
# encoding: utf-8

import argparse
import multiprocessing
import os
import timeit
from time import sleep

from pwn import *
from ScanBUG import Format
from ScanBUG import ArbRW
from ScanBUG import Resgs
from ScanBUG import Heap
from ScanBUG import Stack
from pathlib import Path
import log
import json

from multiprocessing import Process


def path_msg(inlist, type):
    for indir in inlist:
        print("\n------------------------", type, "------------------------")
        if "over_num" in indir:
            strt = "[over bytes]:"+ str(indir["over_num"])
            log.WrLog(strt)
            print(strt)
        if "stdout" in indir:
            strt = "[stdout]:" + str(indir["stdout"])
            log.WrLog(strt)
            print(strt)
        if "stdin" in indir:
            strt = "[stdin]:" + str(indir["stdin"])
            log.WrLog(strt)
            print(strt)
        if "chain" in indir:
            strt = "[jump chain]:" + str(indir["chain"])
            log.WrLog(strt)
            print(strt)
        if "argv" in indir:
            strt = "[argv]:" + str(indir["argv"])
            log.WrLog(strt)
            print(strt)
        print()


# 默认不限制时间
def find_stack_repeat(limit=None):
    stack_overflow(filename, args=argv, start_addr=entry_addr, limit=limit)


# 打印漏洞情况
def find_stack_msg(limit=None):
    # 执行一遍漏洞
    p = Process(target=find_stack_repeat, args=(limit,))  #
    p.start()
    p.join(limit_time)
    if p.is_alive():
        print("[-] runing over limit time,kill it")
        log.WrLog("[-] runing over limit time,kill it")
        p.terminate()
    p.join()

    fp = None
    try:
        fp = open("stack.json", "r+")
    except:
        log.WrLog("find nothing in stack overflow vulnerability!")
        print("find nothing in stack overflow vulnerability!")
        return

    bp_overflow_result = []
    pc_overflow_result = []

    while True:
        str_line = fp.readline()
        if str_line:
            # print(bytes(str_line,"utf-8"))
            json_str = json.loads(str_line)
            # print(type(json_str))
            for k in json_str:
                if k == "bp_overflow_result":
                    bp_overflow_result.append(json_str["bp_overflow_result"])
                if k == "pc_overflow_result":
                    pc_overflow_result.append(json_str["pc_overflow_result"])
        else:
            break
    fp.seek(0)
    # fp.truncate()
    fp.close()
    # os.system("rm tmp.json")
    log.WrLog("\n[+]===has found" + str(len(bp_overflow_result))) + "stack overflow to BP==="
    print("\n[+]===has found", len(bp_overflow_result), "stack overflow to BP===")
    path_msg(bp_overflow_result, "bp_overflow_result")

    print("\n[+]===has found", len(pc_overflow_result), "stack overflow to PC===")
    path_msg(pc_overflow_result, "pc_overflow_result")


def find_stack_overflow():
    times = 1
    find_stack_msg()

    while True:
        print("[+] attempt to find stack overflow vulnerability for {} times".format(times))
        print("1.try again; 2.change limit; 3.return to menu")
        print("input your choice:")
        choice = input()
        try:
            choice = int(choice)
        except:
            print("error input, it must be a num!")
            continue

        if choice == 1:
            find_stack_msg()
            times += 1
            continue

        if choice == 2:
            print("input your limit num:")
            limit = input()
            print("input runing time(min):")
            mins = input()
            try:
                limit = int(limit)
                mins = int(mins)
            except:
                print("error input, it must be a num!")
                continue
            global limit_time
            limit_time = one_min * mins

            find_stack_msg(limit=limit)
            times += 1
            continue

        if choice == 3:
            print("[+] find_stack_overflow() over")
            return
        else:
            print("error input, try again!")
            continue


# 任意地址读写
def find_arbitrary_repeat(limit=None):
    arbitrary_RW_vulnerability(filename, args=argv, start_addr=entry_addr, limit=limit)


def find_arbitrary_msg(limit=None):
    p = Process(target=find_arbitrary_repeat, args=(limit,))  #
    p.start()
    p.join(limit_time)
    if p.is_alive():
        print("[-] runing over limit time,kill it")
        p.terminate()
    p.join()

    fp = None
    try:
        fp = open("tmp.json", "r+")
    except:
        print("find nothing in arbitrary RW vulnerability!")
        return
    arbitrary_R_result = []
    arbitrary_W_result = []
    while True:
        str_line = fp.readline()
        if str_line:
            # print(bytes(str_line,"utf-8"))
            json_str = json.loads(str_line)
            # print(type(json_str))
            for k in json_str:
                if k == "arbitrary_W_result":
                    arbitrary_W_result.append(json_str["arbitrary_W_result"])
                if k == "arbitrary_R_result":
                    arbitrary_R_result.append(json_str["arbitrary_R_result"])
        else:
            break
    fp.seek(0)
    # fp.truncate()
    fp.close()
    # os.system("rm tmp.json")

    print("\n[+]===has found", len(arbitrary_W_result), "arbitrary write===")
    path_msg(arbitrary_W_result, "arbitrary_W_result")

    print("\n[+]===has found", len(arbitrary_R_result), "arbitrary read===")
    path_msg(arbitrary_R_result, "arbitrary_R_result")


def find_arbitrary():
    times = 1
    find_arbitrary_msg()

    while True:
        print("[+] attempt to find arbitrary RW vulnerability for {} times".format(times))
        print("1.try again; 2.change limit; 3.return to menu")
        print("input your choice:")
        choice = input()
        try:
            choice = int(choice)
        except:
            print("error input, it must be a num!")
            continue

        if choice == 1:
            find_arbitrary_msg()
            times += 1
            continue

        if choice == 2:
            print("input your limit num:")
            limit = input()
            print("input runing time(min):")
            mins = input()
            try:
                limit = int(limit)
                mins = int(mins)
            except:
                print("error input, it must be a num!")
                continue
            global limit_time
            limit_time = one_min * mins

            find_arbitrary_msg(limit=limit)
            times += 1
            continue

        if choice == 3:
            print("[+] find_arbitrary() over")
            return
        else:
            print("error input, try again!")
            continue


# 寻找寄存器错误
def find_error_regs_repeat(limit=None):
    error_regs(filename, args=argv, start_addr=entry_addr, limit=limit)


def find_error_regs_msg(limit=None):
    p = Process(target=find_error_regs_repeat, args=(limit,))  #
    p.start()
    p.join(limit_time)
    if p.is_alive():
        print("[-] runing over limit time,kill it")
        p.terminate()
    p.join()

    fp = None
    try:
        fp = open("tmp.json", "r+")
    except:
        print("find nothing in error regs vulnerability!")
        return
    pc_error_result = []
    bp_error_result = []
    sp_error_result = []
    unknow_error_result = []
    while True:
        str_line = fp.readline()
        if str_line:
            # print(bytes(str_line,"utf-8"))
            json_str = json.loads(str_line)
            # print(type(json_str))
            for k in json_str:
                if k == "pc_error_result":
                    pc_error_result.append(json_str["pc_error_result"])
                if k == "sp_error_result":
                    sp_error_result.append(json_str["sp_error_result"])
                if k == "bp_error_result":
                    bp_error_result.append(json_str["bp_error_result"])
                if k == "unknow_error_result":
                    unknow_error_result.append(json_str["unknow_error_result"])
        else:
            break
    fp.seek(0)
    # fp.truncate()
    fp.close()
    # os.system("rm tmp.json")

    print("\n[+]===has found", len(pc_error_result), "pc reg error===")
    path_msg(pc_error_result, "pc_error_result")
    print("\n[+]===has found", len(sp_error_result), "sp reg read===")
    path_msg(sp_error_result, "sp_error_result")
    print("\n[+]===has found", len(bp_error_result), "bp reg read===")
    path_msg(bp_error_result, "bp_error_result")
    print("\n[+]===has found", len(unknow_error_result), "unknow error===")
    path_msg(unknow_error_result, "unknow_error_result")


def find_error_regs():
    times = 1
    find_error_regs_msg()

    while True:
        print("[+] attempt to find error regs vulnerability for {} times".format(times))
        print("1.try again; 2.change limit; 3.return to menu")
        print("input your choice:")
        choice = input()
        try:
            choice = int(choice)
        except:
            print("error input, it must be a num!")
            continue

        if choice == 1:
            find_error_regs_msg()
            times += 1
            continue

        if choice == 2:
            print("input your limit num:")
            limit = input()
            print("input runing time(min):")
            mins = input()
            try:
                limit = int(limit)
                mins = int(mins)
            except:
                print("error input, it must be a num!")
                continue
            global limit_time
            limit_time = one_min * mins

            find_error_regs_msg(limit=limit)
            times += 1
            continue

        if choice == 3:
            print("[+] find_error_regs() over")
            return
        else:
            print("error input, try again!")
            continue


# 寻找格式化字符串漏洞
def find_format_repeat(limit=None):
    fmt_vulnerability(filename, args=argv, start_addr=entry_addr, limit=limit)


def find_format_msg(limit=None):
    p = Process(target=find_format_repeat, args=(limit,))  #
    p.start()
    p.join(limit_time)
    if p.is_alive():
        print("[-] runing over limit time,kill it")
        p.terminate()
    p.join()

    fp = None
    try:
        fp = open("tmp.json", "r+")
    except:
        print("find nothing in format string vulnerability!")
        return
    fmt_result = []

    while True:
        str_line = fp.readline()
        if str_line:
            json_str = json.loads(str_line)
            for k in json_str:
                if k == "fmt_result":
                    fmt_result.append(json_str["fmt_result"])
        else:
            break

    fp.seek(0)
    # fp.truncate()
    fp.close()
    # os.system("rm tmp.json")

    print("\n[+]===has found", len(fmt_result), "fmt string vulnerability===")
    path_msg(fmt_result, "fmt_result")


def find_format():
    times = 1
    find_format_msg()

    while True:
        print("[+] attempt to find fmt string vulnerability for {} times".format(times))
        print("1.try again; 2.change limit; 3.return to menu")
        print("input your choice:")
        choice = input()
        try:
            choice = int(choice)
        except:
            print("error input, it must be a num!")
            continue

        if choice == 1:
            find_format_msg()
            times += 1
            continue

        if choice == 2:
            print("input your limit num:")
            limit = input()
            print("input runing time(min):")
            mins = input()
            try:
                limit = int(limit)
                mins = int(mins)
            except:
                print("error input, it must be a num!")
                continue
            global limit_time
            limit_time = one_min * mins

            find_format_msg(limit=limit)
            times += 1
            continue

        if choice == 3:
            print("[+] find_format() over")
            return
        else:
            print("error input, try again!")
            continue


# 寻找堆漏洞
def find_heap_vul_repeat(limit=None):
    heap_vulnerability(filename, args=argv, start_addr=entry_addr, limit=limit)


def find_heap_vul_msg(limit=None):
    p = Process(target=find_heap_vul_repeat, args=(limit,))  #
    p.start()
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


def find_heap_vul():
    times = 1
    find_heap_vul_msg()

    while True:
        print("[+] attempt to find heap vulnerability for {} times".format(times))
        print("1.try again; 2.change limit/time; 3.return to menu")
        print("input your choice:")
        choice = input()
        try:
            choice = int(choice)
        except:
            print("error input, it must be a num!")
            continue

        if choice == 1:
            find_heap_vul_msg()
            times += 1
            continue

        if choice == 2:
            print("input your limit num:")
            limit = input()
            print("input runing time(min):")
            mins = input()
            try:
                limit = int(limit)
                mins = int(mins)
            except:
                print("error input, it must be a num!")
                continue
            global limit_time
            limit_time = one_min * mins
            find_heap_vul_msg(limit=limit)
            times += 1
            continue

        if choice == 3:
            print("[+] find_heap_vul() over")
            return
        else:
            print("error input, try again!")
            continue


def main():
    print("[+] the msg of target program:")
    os.system("checksec {}".format(filename))
    sleep(1)
    start = timeit.default_timer()
    pool = multiprocessing.Pool(processes=5)
    pool.apply_async(find_stack_overflow)
    pool.apply_async(find_arbitrary)
    pool.apply_async(find_error_regs)
    pool.apply_async(find_format)
    pool.apply_async(find_heap_vul)
    # pool.apply_async(main)
    pool.close()
    pool.join()
    end = timeit.default_timer()
    TaskTime = end - start
    log.WrLog()


if __name__ == '__main__':
    fmt_vulnerability = Format.Check_format_string
    arbitrary_RW_vulnerability = ArbRW.Check_arbitrary_RW
    stack_overflow = Stack.Check_StackOverflow
    heap_vulnerability = Heap.Check_heap
    error_regs = Resgs.Check_regs_error
    one_min = 60
    limit_time = one_min * 20

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="the target program to analyze")
    parser.add_argument('-l', '--args_size', help="the bytes of each arg to the target program", default=False)
    parser.add_argument('-n', '--args_num', help="the num of args to the target program", default=False)
    parser.add_argument('-s', '--start_addr', help="set the start_addr to the entry_addr to execve target program",
                        default=False)
    parser.add_argument('-t', '--run_time', help="set the run_time to limit angr running time(min)", default=False)

    args = parser.parse_args()
    filename = args.file

    if not Path(filename).is_file():
        print("[-] '{}' is not exist or not a file!".format(filename))
        exit(1)

    args_num = False
    args_size = False
    entry_addr = False
    argv = None
    if args.run_time:
        limit_time = one_min * int(args.run_time)

    if args.args_size or args.args_num:
        if args.args_size and args.args_num:
            try:
                args_size = int(args.args_size, 16)
            except Exception as e:
                print("[-] invaild args_size! it must be a hex num")
                raise e
            try:
                args_num = int(args.args_num, 16)
            except Exception as e:
                print("[-] invaild args_num! it must be a hex num")
                raise e
            argv = []
            for _ in range(args_num):
                argv.append(args_size)
        else:
            print("[-] -l -n must use together")
            exit(1)

    if args.start_addr:
        try:
            entry_addr = int(args.start_addr, 16)
        except Exception as e:
            print("[-] invaild entry_addr! it must be a hex num")
            raise e

    main()
