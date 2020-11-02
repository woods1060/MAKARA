# MAKARA

**魔羯**是一个基于符号执行的二进制动态分析框架

[Github]: https://github.com/ZERO-A-ONE/MAKARA
[Gitee]: https://gitee.com/zeroaone/makara

## 简介

> 魔羯座遇上双子座的是一种怎么样的体验呢，是一种怎么样的故事呢
>
> 这就是宿命吧，相信命运吧，能让魔羯相信直觉的人是一种怎么样的存在呢
>
> 喂喂喂，你在干嘛，这可是Git上的ReadMe啊

本项目脱胎于两位志趣相投，一个在南方，一个在北方的大学本科生在暑期专业实训中对于符号执行技术的研究

### 基本框架图

![]([README.assets/架构图.png](https://note-book.obs.cn-east-3.myhuaweicloud.com/MAKARA/ReadMe/Beta/1/%E6%9E%B6%E6%9E%84%E5%9B%BE.png))

### 功能

#### 自动漏洞挖掘

通过符号执行、Fuzz模糊测试、污染分析的动态二进制分析方法，进行自动化漏洞挖掘，拟支持的漏洞类型

- 缓冲区溢出漏洞
- 格式化字符串漏洞
- Use After Free
- Double Free
- 任意地址读写
- 寄存器错误
- Tcache利用

#### 基础数据库

如框架图所示主要用户基础信息展示

#### WEB

可以本地部署的浏览器后台访问接口，可以上传程序，并管理程序，查看分析情况和更多插件功能

#### 外部安全工具

可以导入外部安全工具的分析数据加入数据库，也可以从基础数据库导出数据至外部安全工具分析，例如IDA或者Ghidra

#### 监听器

这个功能主要用于CTF的线下AD模式，自动检测网络环境生成的主机，调用基础数据库里的Exploit，可以自行编写Exploit执行策略，自动回收Flag，自动提交

### 阶段目标

目前2020年结束前完成第一阶段的内容开发，在2021年步入第二阶段

#### 第一阶段

SMT求解器设置为Angr，漏洞挖掘脚本基于Angr开发，WEB与基础数据库基本雏形完成

#### 第二阶段

包括IDA、Ghidra插件，支持包括RISC-V在内的更多架构

## 安装和使用

预计提供包括Docker、PIP包在内的多种安装方式

### Docker

目前提供Docker直接的环境部署

## 开发进度

#### 开发环境

目前开发致力于基于国产计算平台环境

- CPU：Huawei Kunpeng 920 2.6GHz
- OS：openEuler 20.03 64bit with ARM

## 依赖

- angr：https://github.com/angr/angr

## 版本记录

- 2020/8/10 **Beta 0.1** ：混沌初开
  - 完成了项目框架的构思