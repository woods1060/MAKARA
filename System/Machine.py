from __future__ import print_function
from collections import OrderedDict
from collections import OrderedDict
import pprint

class machine:
    LinuxKernel = ""
    MEMORY = ""
    Distro = ""
    IP_Address = ""
    CPU_INFO = ""
    CPU_ARCH = ""

    def GetCPU(self):
        '''
        CPUinfo[proc0]=Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz
        CPUinfo[proc1]=Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz
        CPUinfo[proc2]=Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz
        CPUinfo[proc3]=Intel(R) Core(TM) i5-3230M CPU @ 2.60GHz
        print('CPUinfo[{0}]={1}'.format(processor,CPUinfo[processor]['model name']))
        :return:
        '''
        CPUinfo = OrderedDict()
        procinfo = OrderedDict()
        nprocs = 0
        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    # end of one processor
                    CPUinfo['proc%s                       nnnnnnn  n' % nprocs] = procinfo
                    nprocs = nprocs + 1
                    # Reset
                    procinfo = OrderedDict()
                else:
                    if len(line.split(':')) == 2:
                        procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        procinfo[line.split(':')[0].strip()] = ''
        return CPUinfo

    def GetMEM(self):
        '''
        Total memory:3593316 kB
        Free memory:2113712 kB
        :return:
        print("Total memory:{0}".format(meminfo['MemTotal']))
        print("Free memory:{0}".format(meminfo['MemFree']))
        '''
        meminfo = OrderedDict()
        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        return meminfo


    def __init__(self):
        CPUinfo = self.GetCPU()
        self.CPU_INFO = CPUinfo
        MEMinfo = self.GetMEM()
        self.MEMORY = MEMinfo

if __name__ == '__main__':
    c1 = machine()
    print(c1.CPU_INFO)
    print(c1.MEMORY)
