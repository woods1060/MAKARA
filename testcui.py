import curses
import time
import random
from eprogress import LineProgress, CircleProgress
import timeit
import log
stdscr = curses.initscr()


def display_info(str, x, y, colorpair=2):
    '''''使用指定的colorpair显示文字'''
    global stdscr
    stdscr.addstr(y, x, str, curses.color_pair(colorpair))
    stdscr.refresh()


def display_info_flash(str, x, y):
    global stdscr
    stdscr.addstr(y, x, str, curses.A_BLINK)
    stdscr.refresh()


def get_ch_and_continue():
    '''''演示press any key to continue'''
    global stdscr
    # 设置nodelay，为0时会变成阻塞式等待
    stdscr.nodelay(0)
    # 输入一个字符
    ch = stdscr.getch()
    # 重置nodelay,使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)
    return True


def set_win():
    '''''控制台设置'''
    global stdscr
    # 使用颜色首先需要调用这个方法
    curses.start_color()
    # ：0：黑色，1：红色，2：绿色，3：黄色，4：蓝色，5：洋红色，6：青色和 7：白色
    # 文字和背景色设置，设置了两个color pair，分别为1和2
    # 先文本，后背景
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # 红底白字
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # 黄底白字
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_CYAN)  # 青底白字
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # 黑底白字
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)  # 黑底红字
    # 关闭屏幕回显
    curses.noecho()
    # 输入时不需要回车确认
    curses.cbreak()
    # 设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)


def unset_win():
    '''控制台重置'''
    global stdstr
    # 恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    # 结束窗口
    curses.endwin()


def main(LIMT=20, ):
    circle_progress = CircleProgress(title='Initialize loading')
    for i in range(1, 10):
        circle_progress.update(i)
        time.sleep(0.1)

    line_progress = LineProgress(title='Scan System Information')
    for i in range(1, 101):
        line_progress.update(i)
        time.sleep(0.02)

    line_progress = LineProgress(title='Scan Patch')
    for i in range(1, 101):
        line_progress.update(i)
        time.sleep(0.03)

    line_progress = LineProgress(title='Scan Model')
    for i in range(1, 101):
        line_progress.update(i)
        time.sleep(0.03)

    cpuuser = 0
    MODLENUM = 0
    FORMATS = 0
    STACKS = 0
    REGSS = 0
    RWS = 0
    TOTALNUM = 0
    FORMATN = 0
    STACKN = 0
    REGN = 0
    RWN = 0

    start = timeit.default_timer()
    set_win()
    display_info(" BJTU ZXY MAKARA ", 0, 0, 1)
    display_info(" Version: Beta 0.1 ", 17, 0, 2)
    display_info(" Gitee: https://gitee.com/zeroaone/makara \n", 36, 0, 3)
    str1 = (
        " __  __    _    _  __    _    ____      _\n"
        "|  \/  |  / \  | |/ /   / \  |  _ \    / \\\n"
        "| |\/| | / _ \ | ' /   / _ \ | |_) |  / _ \\\n"
        "| |  | |/ ___ \| . \  / ___ \|  _ <  / ___ \\\n"
        "|_|  |_/_/   \_\_|\_\/_/   \_\_| \_\/_/   \_\\\n"
        "\n"
    )
    display_info_flash(str1, 0, 1)
    display_info("[CPU:     %]", 0, 7, 4)
    display_info("[CPU-USER-TIME:          ]", 0, 8, 4)
    display_info("[MEM:     %]", 0, 9, 4)
    display_info("[ PROCESS TIMING ] \n", 0, 10, 1)
    display_info("TIMING LIMIT ：" + str(LIMT) + " MIN", 0, 11, 1)
    display_info("TIMING RUNING：", 0, 12, 1)
    display_info("[ SCAN BUG STEP  ] \n", 0, 13, 2)
    display_info("MODEL     NUM：", 0, 14, 4)
    display_info("FORMAT  STEPS：", 0, 15, 4)
    display_info("STACK   STEPS：", 0, 16, 4)
    display_info("REGS    STEPS：", 0, 17, 4)
    display_info("RW      STEPS：", 0, 18, 4)
    display_info("[ SCAN BUG NUM  ] \n", 0, 19, 2)
    display_info("TOTAL    NUMS：", 0, 20, 4)
    display_info("FORMAT   NUMS：", 0, 21, 4)
    display_info("STACK    NUMS：", 0, 22, 4)
    display_info("REGS     NUMS：", 0, 23, 4)
    display_info("RW       NUMS：", 0, 24, 4)
    display_info("[ SYSTEM  INFO  ] \n", 0, 25, 2)
    display_info("CPU      NAME：", 0, 26, 4)
    display_info("CPU      ARCH：", 0, 27, 4)
    display_info("IP     ADDRES：", 0, 28, 4)
    display_info("OS       INFO：", 0, 29, 4)
    display_info("[LOG INFO LATEST 10] \n", 0, 30, 2)

    try:
        while 1:
            FORMATS = FORMATS + random.randint(0, 10)
            STACKS = STACKS + random.randint(0, 20)
            REGSS = REGSS + random.randint(0, 20)
            RWS = RWS + random.randint(0, 20)
            MODLENUM = FORMATS + STACKS + REGSS + RWS
            #PROCESS TIMING
            FORMATN = FORMATN + random.randint(0, 2)
            STACKN = STACKN + random.randint(0, 2)
            REGN = REGN + random.randint(0, 2)
            RWN = RWN + random.randint(0, 2)
            TOTALNUM = FORMATN + STACKN + REGN + RWN

            end = timeit.default_timer()
            time.sleep(1.5)
            mem = random.randint(0, 100)
            cpu = random.randint(0, 100)
            cpuuser = cpuuser + 1
            #SCAN BUG STEP
            display_info(str(cpu), 6, 7, 5)
            display_info(str(cpuuser), 16, 8, 5)
            display_info(str(mem), 6, 9, 5)
            display_info(str(end - start), 14, 12, 5)
            #SYSTEM  INFO
            display_info(str(MODLENUM), 15, 14, 5)
            display_info(str(FORMATS), 15, 15, 5)
            display_info(str(STACKS), 15, 16, 5)
            display_info(str(REGSS), 15, 17, 5)
            display_info(str(RWS), 15, 18, 5)
            display_info(str(TOTALNUM), 15, 20, 5)
            display_info(str(FORMATN), 15, 21, 5)
            display_info(str(STACKN), 15, 22, 5)
            display_info(str(REGN), 15, 23, 5)
            display_info(str(RWN), 15, 24, 5)
            #SYSTEM  INFO
            display_info('Qualcomm Technologies, Inc SDM660', 15, 26, 5)
            display_info('ARM aarch64', 15, 27, 5)
            display_info('192.168.31.106', 15, 28, 5)
            display_info('Android 9', 15, 29, 5)
            #logINFO
            str1 = []
            str1.append("adasdasdasdasdasdasdasd")
            str1.append("sfasgea")
            str1.append("asasdasdasd")
            str1.append("ftrythfgh")
            str1.append("sadf34q")
            str1.append("vbvnvcbnbvnvb")
            str1.append("wrwersdf")
            str1.append("3454356ydh")
            str1.append("hdfhdfg")
            str1.append("eqwrsdfasdf")
            str1.append("cvbnvcb")
            str1.append("adhxcncvnvbxdfgsdgrsdrg")
            str1.append("fdsadfzxdvzxvd")
            str1.append("vzxcvzxcvzxcvzxvzxcvzxc")
            index = random.randint(0, 12)
            display_info(str1[index], 0, 31, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 32, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 33, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 34, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 35, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 36, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 37, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 38, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 39, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0, 40, 5)
            index = random.randint(0, 12)
            display_info(str1[index], 0 ,41, 5)

    except KeyboardInterrupt:
        unset_win()
    #except:
        #unset_win()


if __name__ == '__main__':
    main(20)
