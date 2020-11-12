from datetime import datetime
def WrLog(str2):
    dt = datetime.now()
    str1 = dt.strftime('%Y-%m-%d %H:%M:%S %f')
    str1 = str1 + "  " + str2 + "\n"
    with open('log.txt', 'a') as f:
        f.writelines(str1)

def ReadLog():
    pass