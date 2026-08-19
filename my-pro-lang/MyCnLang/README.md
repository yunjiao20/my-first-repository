# MyCnLang

在阅读《[流程的Python(fluent python)](https://github.com/fluentpython)》的过程中
仿造 [Norvig lis.py](https://github.com/norvig/pytudes/blob/main/py/lis.py) 编写的句法器,
解析我自定义的MyCnLang句法，请查看[MyCnLang语法速查.txt](./MyCnLang语法速查.txt)查看MyCnLang语法
<hr>
此句法器编写环境为 Linux 6.18.12+kali-amd64 Python 3.13 ，不能保证其他环境下的使用效果
<br>
<br>
最新的句法器为 `mycnlang.py` ,在最新的句法器提交后，旧的句法器会更名，在后面添加旧句法器的日期，如 mycnlang20260817.py.<br>
请下载`mycnlang.py`
<br>
<br>
文档仍在编写中

## 更新日志

- 2026/8/17 （文件`mycnlang20260817.py`）
  - 第一次提交，已经基本实现功能。提供了'输出'、'读取'、'数列'三个内置函数、

- 2026/8/19 （文件`mycnlang.py`）
  - 为内置函数添加了提示信息
  - 新增了'整型'、'浮点型'、'字符串型'三个内置函数，用于转换数据类型
  - 源码新增了一个变量'MyCnLang'保存MyCnLang栈STACK的引用。在PythonEval和PythonExec执行Python语句时，
    可以使用"MyCnLang['MyCnLang变量名']"来访问MyCnLang变量（原先使用"STACK['MyCnLang变量名']"通过访问
    MyCnLang的栈获取MyCnLang中的变量，当然现在也可以这么做）。这在你插入Python代码拓展MyCnLang功能时或许会
    更加直观
