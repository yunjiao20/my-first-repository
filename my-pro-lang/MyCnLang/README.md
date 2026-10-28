# MyCnLang

在阅读《[流程的Python(fluent python)](https://github.com/fluentpython)》的过程中
仿造 [Norvig lis.py](https://github.com/norvig/pytudes/blob/main/py/lis.py) 编写的句法器,
解析我自定义的MyCnLang句法，请查看[MyCnLang语法速查.txt](./MyCnLang语法速查.txt)查看MyCnLang语法
<hr>
此句法器编写环境为 Linux 6.18.12+kali-amd64 Python 3.13 ，不能保证其他环境下的使用效果
<br>
<br>
最新的句法器为 `mycnlang.py` ,其内容始终与最新日期的版本一致<br>
请下载`mycnlang.py`
<br>
<br>
文档仍在编写中

## 更新日志

- 2026/8/17 （文件`mycnlang20260817.py`）
  - 第一次提交，已经基本实现功能。提供了'输出'、'读取'、'数列'三个内置函数、

- 2026/8/19 （文件`mycnlang20260819.py`）
  - 为内置函数添加了提示信息
  - 新增了'整型'、'浮点型'、'字符串型'三个内置函数，用于转换数据类型
  - 源码新增了一个变量'MyCnLang'保存MyCnLang栈STACK的引用。在PythonEval和PythonExec执行Python语句时，
    可以使用"MyCnLang['MyCnLang变量名']"来访问MyCnLang变量（原先使用"STACK['MyCnLang变量名']"通过访问
    MyCnLang的栈获取MyCnLang中的变量，当然现在也可以这么做）。这在你插入Python代码拓展MyCnLang功能时或许会
    更加直观

- 2026/10/28 （文件`mycnlang20261028.py`）
  - 删去了一些不必要的`eval`和`exec`包裹，提高了每次调用函数的效率
  - ***修复了`-c`和`--help`参数不能识别的问题***
  - ***添加了库文件夹 mycnlang_lib ，拓展了一些功能，放到脚本目录下 import 即可。具体请查看
    [MyCnLang_Lib README](./mycnlang_lib)***。
  - 增添了`Shell`关键字，封装了Python`os.popen().read()`，允许你执行系统命令并获取信息，然后你可以使用
    mycnlang_lib中的`string.mcl`库处理信息
  - 增添了内置函数`f`（拼接字符串，以免你使用太多`+`拼接）、`len`（获取字符串、列表、字典长度）、`slice`（列表
    和字符串切片）
