# MAKARA

**魔羯**是一个基于符号执行的二进制动态分析框架

[Github]: https://github.com/ZERO-A-ONE/MAKARA
[Gitee]: https://gitee.com/zeroaone/makara

## 一、简介

> 魔羯座遇上双子座的是一种怎么样的体验呢，是一种怎么样的故事呢
>
> 这就是宿命吧，相信命运吧，能让魔羯相信直觉的人是一种怎么样的存在呢
>
> 喂喂喂，你在干嘛，这可是Git上的ReadMe啊

本项目脱胎于两位志趣相投，一个在南方，一个在北方的大学本科生在暑期专业实训中对于符号执行技术的研究

### （1）基本框架图

![](https://note-book.obs.cn-east-3.myhuaweicloud.com/MAKARA/ReadMe/Beta/1/%E6%9E%B6%E6%9E%84%E5%9B%BE.png)

### （2）模块



### （3）功能

#### ①自动漏洞挖掘

通过符号执行、Fuzz模糊测试、污染分析的动态二进制分析方法，进行自动化漏洞挖掘，拟支持的漏洞类型

- 缓冲区溢出漏洞
- 格式化字符串漏洞
- Use After Free
- Double Free
- 任意地址读写
- 寄存器错误
- Tcache利用

#### ② 基础数据库

如框架图所示主要用户基础信息展示

#### ③ WEB

可以本地部署的浏览器后台访问接口，可以上传程序，并管理程序，查看分析情况和更多插件功能

#### ④ 外部安全工具

可以导入外部安全工具的分析数据加入数据库，也可以从基础数据库导出数据至外部安全工具分析，例如IDA或者Ghidra

#### ⑤ 监听器

这个功能主要用于CTF的线下AD模式，自动检测网络环境生成的主机，调用基础数据库里的Exploit，可以自行编写Exploit执行策略，自动回收Flag，自动提交

### （4）阶段目标

目前2020年结束前完成第一阶段的内容开发，在2021年步入第二阶段

#### ① 第一阶段

SMT求解器设置为Angr，漏洞挖掘脚本基于Angr开发，WEB与基础数据库基本雏形完成

#### ② 第二阶段

包括IDA、Ghidra插件，支持包括RISC-V在内的更多架构



## 二、数据库设计

### 基本表



## 三、安装和使用

预计提供包括Docker、PIP包在内的多种安装方式

### Docker

目前提供Docker直接的环境部署

## 四、开发进度

#### 特点

目前开发致力于基于国产计算平台环境

- CPU：Huawei Kunpeng 920 2.6GHz
- OS：OpenEuler 20.03 64bit with ARM
- DB：Huawei GaussDB

### （1）针对鲲鹏架构的优化

#### ① Angr

我们可以发现Angr的Python依赖库，得到依赖列表

```python
(angr) root@ecs-kc1-large-2-linux-20201025105424:~/CUI/Model# pip3 show angr
Name: angr
Version: 9.0.4495
Summary: A multi-architecture binary analysis toolkit, with the ability to perform dynamic symbolic execution and various static analyses on binaries
Home-page: https://github.com/angr/angr
Author: None
Author-email: None
License: UNKNOWN
Location: /root/.environments/angr/lib/python3.6/site-packages
Requires: dpkt, protobuf, CppHeaderParser, ailment, mulpyplexer, claripy, pycparser, itanium-demangler, sortedcontainers, unicorn, GitPython, psutil, networkx, progressbar2, rpyc, pyvex, cachetools, archinfo, capstone, cle, cffi
Required-by: 
```

在安装过程中我们可以发现claripy、unicorn、psutil库是需要重新编译的，

## 五、Tips

下面记录了一些在开发过程遇到的问题

### （1）关于Python的并行化处理问题

​	在Python中，没有办法利用多个线程，因为它使用了所谓的GIL或全局解释器锁，这意味着一次只有一个线程可以运行Python代码

​	GIL 的全称为 Global Interpreter Lock ，意即全局解释器锁。在 Python 语言的主流实现 CPython 中，GIL 是一个货真价实的全局线程锁，在解释器解释执行任何 Python 代码时，都需要先获得这把锁才行，在遇到 I/O 操作时会释放这把锁。如果是纯计算的程序，没有 I/O 操作，解释器会每隔 100 次操作就释放这把锁，让别的线程有机会执行（这个次数可以通过sys.setcheckinterval 来调整）。所以虽然 CPython 的线程库直接封装操作系统的原生线程，但 CPython 进程做为一个整体，同一时间只会有一个获得了 GIL 的线程在跑，其它的线程都处于等待状态等着 GIL 的释放。这也就解释了我们上面的实验结果：虽然有两个死循环的线程，而且有两个物理 CPU 内核，但因为 GIL 的限制，两个线程只是做着分时切换，总的 CPU 占用率还略低于 50％

​	需要真正的并发性，可以考虑使用**多处理**，因为它是基于进程的，并产生一个新的Python解释器，因此绕过了GIL

## 六、依赖

- angr：https://github.com/angr/angr

## 七、版本记录

- 2020/8/10 **Beta 0.1** ：混沌初开
  - 完成了项目框架的构思

## 八、参考论文

1.  Shao SH, Gao Q, Ma S, Duan FY, Ma X, Zhang SK, Hu JH. Progress in research on buffer overflow vulnerability analysis technologies. Ruan Jian Xue Bao/Journal of Software, 2018,29(5):1179−1198 (in Chinese)
2. 黄宁, 黄曙光, 潘祖烈, et al. 多模块ROP碎片化自动布局方法[J]. 国防科技大学学报, 42(3):22.
3. Manh-Dung Nguyen,Sébastien Bardin,Richard Bonichon. Binary-level Directed Fuzzing for Use-After-Free Vulnerabilities
4. 黄钊, 黄曙光, 邓兆琨, 黄晖. 格式化字符串漏洞自动检测与测试用例生成[J/OL]. 2019, 36(9). [2018-05-24]. 
5. 方皓, 吴礼发, 吴志勇. 基于符号执行的Return-to-dl-resolve利用代码自动生成方法[J]. 计算机科学, 2019.
6. 黄宁，黄曙光，黄钊．基于符号执行的 S.E.H 覆写攻击自动检测方法[J/OL]．吉 林大学学报(工学版).
7. 张超，潘祖烈，樊靖．基于符号执行的堆溢出 fastbin 攻击检测方法．计算机 工程.
8. 李超, 胡建伟, 崔艳鹏. 基于符号执行的缓冲区溢出漏洞自动化利用[J]. 计算机应用与软件, 2019, 036(009):327-333.
9. 张超，潘祖烈，樊靖．面向堆内存漏洞的 double free 攻击方法检测[J]. 计算机应用研究, 2020, 037(009):275-278.
10. 鲍铁匀, 高凤娟, 周严, 李游, 王林章, 李宣东,基于目标制导符号执行的静态缓冲区溢出警报自动确认技术[TP].信息安全学报,2016,1(2):46-60
11. 王田园. 符号执行的路径爆炸及约束求解问题研究[D].
12. 许珂磊. 符号执行循环和递归制导技术研究[D]. 2019.
13. 靳宪龙, 徐世伟, 黄雅娟. 基于Crash的漏洞利用自动生成系统[J]. 现代计算机, 2020, No.686(14):95-100.
14. 董齐兴. 基于动态符号执行的测试用例生成技术研究[D]. 中国科学技术大学, 2014.
15. 张小松, 陈厅, 吉小丽,等. 基于全局超级块支配图的动态符号执行方法:, 2015.
16. 黄宁, 黄曙光, 黄晖,等. 基于符号执行的高危unlink漏洞判定[C]// 中国计算机学会, 2017.
17. 黄宁, 黄曙光, 黄钊. 基于符号执行的异常处理结构体覆写攻击自动检测方法[J]. 吉林大学学报(工学版), 2020, v.50;No.209(03):265-271.
18. 曹琰.面向软件脆弱性分析的并行符号执行技术研究[D].解放军信息工程大学,2013.
19. 叶志斌, 姜鑫, 史大伟. 一种面向二进制的控制流图混合恢复方法[J/OL]. [2017-07-27].
20. 李曈,丁国富.一种支持多线程程序的符号执行技术[J].计算机与现代化,2020,06:60-67
21. 黄桦烽, 王嘉捷, 杨轶,等. 有限资源条件下的软件漏洞自动挖掘与利用[J]. 计算机研究与发展, 2019, 056(011):2299-2314.