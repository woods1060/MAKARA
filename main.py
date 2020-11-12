import argparse
from eprogress import LineProgress, CircleProgress
import time
import FindBUG
filename = ""

def CreateCFG():
    global filename


def main(args):
    # pass
    FindBUG.main(args)


if __name__ == '__main__':
    global filename

    circle_progress = CircleProgress(title='Initialize loading')
    for i in range(1, 10):
        circle_progress.update(i)
        time.sleep(0.1)

    line_progress = LineProgress(title='Scan System Information')
    for i in range(1, 101):
        line_progress.update(i)
        time.sleep(0.2)

    line_progress = LineProgress(title='Scan Patch')
    for i in range(1, 101):
        line_progress.update(i)
        time.sleep(0.5)

    line_progress = LineProgress(title='Scan Model')
    for i in range(1, 101):
        line_progress.update(i)
        time.sleep(0.5)

    # print("\033[34mSuixinBlog: https://suixinblog.cn\033[0m")
    # 初始化运行时间
    one_min = 60
    limit_time = one_min * 20
    # 导入变元表
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="the target program to analyze")
    parser.add_argument('-l', '--args_size', help="the bytes of each arg to the target program", default=False)
    parser.add_argument('-n', '--args_num', help="the num of args to the target program", default=False)
    parser.add_argument('-s', '--start_addr', help="set the start_addr to the entry_addr to execve target program",
                        default=False)
    parser.add_argument('-t', '--run_time', help="set the run_time to limit angr running time(min)", default=False)
    args = parser.parse_args()
    main(args)
