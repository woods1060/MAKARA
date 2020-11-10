#危险函数列表，参考自: https://github.com/intel/safestringlib/wiki/SDL-List-of-Banned-Functions
danger_func = ["alloca","_alloca","scanf","wscanf","sscanf","swscanf","vscanf","vsscanf","strlen","wcslen","strtok","strtok_r","wcstok","strcat","strncat","wcscat","wcsncat","strcpy","strncpy","wcscpy","wcsncpy","memcpy","wmemcpy","stpcpy","stpncpy","wcpcpy","wcpncpy","memmove","wmemmove","memcmp","wmemcmp","memset","wmemset","gets","sprintf","vsprintf","swprintf","vswprintf","snprintf","vsnprintf","realpath","getwd","wctomb","wcrtomb","wcstombs","wcsrtombs","wcsnrtombs"]
#IDA解析的函数通常都会在最前面加上"_",所以在函数列表基础上还需要给每个函数最前面添加"_"
_danger_func = danger_func
s = '_'
for i in xrange(len(danger_func)):
    _danger_func[i] = s + danger_func[i]
total_danger_func = danger_func + _danger_func

#获取Functions列表，并匹配是否存在危险函数
for func in Functions():
    func_name = GetFunctionName(func)
    if func_name in total_danger_func:
#按指定格式输出危险函数定义位置
        print "danger_func_define: ".ljust(8),"\t", func_name.ljust(8), "\t", hex(func)[:-1]
#回溯并输出函数调用地址
        xrefs = CodeRefsTo(func, False)
        i=0
        for xref in xrefs:
#x86调用函数多使用call，而arm则多使用BL
            if GetMnem(xref).lower() == "call" or "BL":
                if func_name in total_danger_func:
                    i=i+1
                    print format(i,'>5.0f')+".","\t","danger_func_call:".ljust(8),"\t", func_name.ljust(8),"\t", hex(xref)[:-1].ljust(8),"\t", GetFuncOffset(xref)