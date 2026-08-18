
#################### -自定义异常- ####################

class MyCnLangError(Exception):
    '''MyCnLang所有错误的父类'''
    def __init__(self, message):
        super().__init__(message)

class 变量未定义(MyCnLangError):
    '''访问未定义的变量'''
    def __init__(self, msg):  super().__init__(msg)

class 语法错误(MyCnLangError):
    '''MyCnLang语法错误'''
    def __init__(self, msg):  super().__init__(msg)

class 文件不存在(MyCnLangError):
    '''访问的文件不存在'''
    def __init__(self, msg):  super().__init__(msg)

class 类型错误(MyCnLangError):
    def __init__(self, msg):  super().__init__(msg)



class RETURN(BaseException):
    '''
    用于终止执行并传递返回值，请使用try-except RETURN as e捕获，再访问e.ret获取返回值

    这个错误继承自BaseException而不是MyCnError或Exception，是为了让我们捕获错误时不会影响
    到函数返回的行为
    '''
    def __init__(self, ret):
        self.ret = ret

#################### -作用域栈和函数- ####################

class Stack:
    '''虚拟的栈，保存函数的作用域'''
    def __init__(self):
        self._stack = []    # 虚拟的栈空间，保存作用域，_stack[-1]为栈顶

    def push(self, scope: dict = None):
        '''向栈中压入新的作用域。不提供参数，默认为空字典，用于开辟一个新的作用域'''
        self._stack.append(scope if scope else {})

    def pop(self) -> dict:
        '''弹出栈顶的作用域，如果栈中已经没有作用域，pop将会退出程序'''
        if self._stack:
            return self._stack.pop()
        else:
            import sys
            sys.exit()

    def __getitem__(self, key, error_sentence = None):
        '''
        使Stack可以使用stack[key]访问栈中的数据

        栈顶作用域（self._stack[-1]）中的值可以被访问，其他作用域只有函数MycnlangFunction可以被访问
        '''
        for scope in self._stack[::-1]:

            if scope is self._stack[-1]:  # 栈顶作用域
                if key in scope.keys():
                    return scope[key]

            else :    # 非栈顶作用域
                if (key in scope.keys()) \
                    and isinstance(scope[key], MycnlangFunction):

                    return scope[key]

        raise 变量未定义(f"变量 '{key}' 未定义")

    def __setitem__(self, key, value):
        '''
        允许使用 stack[key] = value 创建并修改当前作用域中的MyCnLang变量。
        只有栈顶（self._stack[-1]）的数据会被更改
        '''
        self._stack[-1][key] = value

    def __delitem__(self, key: str, error_sentence = None):
        '''
        允许使用 del stack[key] 删除栈顶（self._stack[-1]）的数据'''
        try:
            del self._stack[-1][key]
        except KeyError:  # 栈顶没有这个变量
            raise 变量未定义(f"栈顶不存在变量 '{key}'")

    def show(self, only_top: bool = False):
        '''格式化输出栈中所有信息。当 bool(only_top) == True 时，只输出栈顶信息'''
        if only_top:   # bool(only_top) == True，只显示栈顶
            print(f'scope {len(self._stack[-1]) - 1}:')
            for key in self._stack[-1].keys():
                print(f'{key}\t\t\t{self._stack[-1][key]}')
            return

        for index, scope in zip(
            range(len(self._stack)-1, -1, -1), self._stack[::-1]
        ):  # 显示整个栈
            print(f'scope {index}')
            print('{')
            for key in scope.keys():
                print(f'{key}\t{scope[key].__repr__()}')
            # 最后一个作用域后不用三个换行
            print('}\n\n\n') if (scope is not self._stack[0]) else print('}')


STACK = Stack()     # 创建MyCnLang的栈
STACK.push()        # 提供初始作用域

MyCnLang = STACK    # 保存STACK的引用，便于用户获取MyCnLang变量拓展程序



class MycnlangFunction:
    '''MyCnLang的函数'''

    def __init__(self, argv: list[str], body):
        self._argv = argv
        self._body = body

    def call(self, argvs: list):
        '''
        MyCnLang函数被调用

        call不负责处理参数，传入的参数应提前处理好，如
                func.call([evaluate(i) for i in argvs])
        '''
        STACK.push()    # 栈顶创建函数作用域

        # 在函数作用域绑定参数
        STACK['@argv'] = argvs
        for i in range(len(argvs)):
            exec(f"STACK['@{i+1}'] = argvs[{i}]")
        for i in range(min(len(self._argv), len(argvs))):
            exec(f"STACK[ self._argv[{i}] ] = argvs[{i}]")

        ret = None      # 如无return语句，默认返回None

        try:
            evaluate(self._body)
        except RETURN as RET:
            ret = RET.ret   # 获取返回值
        finally:    # 无论什么错误，保证函数作用域弹出
            STACK.pop()   # 删除函数作用域，清除局部变量

        STACK['@r'] = ret  # 允许使用@r获取返回值，就像sh的$?
        return ret

#################### -生成MyCnLang句法树- ####################
# 在这里，我们将生成MyCnLang句法树，这是一个很重要的功能。比如将
#     '如果 （年龄 >= 18）（输出（‘成年’））'
# 处理成
#     ['如果', ['年龄', '>=', '18'], ['输出', ['‘成年’']]]
# 只有这样才能让我们的求解器evaluate可以解析它。
#
# 而句法树的处理复杂与否取决于你设计的语法，为了给用户提供更高的灵活性（比如括号和引号可以跨越多
# 行和一些中文符号兼容），这里我的实现非常冗杂。不必太过关心这一块是如何实现的，这本可以更简单
def parse(s: str) -> list:
    '''
    整合split_tokens和abstract_syntax_tree，接受MyCnLang语句，处理成可解析的MyCnLang
    句法树。
    应当使用它来处理
    '''
    try:
        return abstract_syntax_tree(split_tokens(s))
    except ValueError:
        raise 语法错误('括号未闭合')

class String:
    '''一个便于后续处理字符串的类'''
    def __init__(self, s: str):
        self.string: str = s
        self.index : int = -1
        self.s_len : int = len(self.string)
    def nextchar(self) -> str:
        '''返回字符串最前面，即即将弹出的字符。当弹出完了，返回None'''
        return self.string[self.index+1] if self.index+1 < self.s_len else None
    def popchar(self) -> str|None:
        '''弹出字符串最前面的字符，全部弹完返回None'''
        self.index += 1
        try:
            return self.string[self.index]
        except IndexError:
            pass
    def popchars(self, num: int = 1) -> str|None:
        '''弹出字符串前面指定数量的字符串'''
        s = ''
        for _ in range(num):
            s += self.popchar()
        return s
    def popuntilbefor(self, until: str|tuple) -> str|None:
        '''弹出字符，直到遇到until中指定字符前一个字符(不弹出终止字符)'''
        s = ''
        while self.nextchar() and self.nextchar() not in until:  # 下一个不是指定终止字符
            char = self.popchar()
            if char:
                s += char
            else:   # 全部弹出结束
                break
        return s
    def popuntil(self, until: str|tuple) -> str|None:
        '''弹出字符，直到遇到指定字符(指定字符也会输出)'''
        return self.popuntilbefor(until) + (
                                    self.popchar() if self.nextchar() else ''
                                )

def split_tokens(string: str) -> list[str]:
    '''将各个最低语法元素区分开来'''
    tokens = []    # 保存语法元素
    token  = ''    # 临时保存语法元素
    in_str = False # 标志是否被引号包裹，既是否在处理字符串
    quo_mark   = ''  # 保存起始引号，通过起始引号确定反引号，以正确关闭字符串
    quo_mark_d = {"'": "'", '"': '"', '‘': '’', '“': '”'}  # 引号对应的反引号
    string = String(
                    string.replace('\\\n', ' ').replace('》》\n', ' ')
                   )  # '\' 和 '》》' 后的换行符被忽略

    def submit_and_clear_token():
        '''当token内存在信息时，将token追加到tokens中，清空token的值。这段代码复用率很高'''
        nonlocal token, tokens
        if token:
            tokens.append(token)
            token = ''

    loop = True
    while loop:
        char = string.popchar()

        ##### -字符串读取完毕- #####
        if char == None:
            # 字符串读取完毕
            submit_and_clear_token()
            loop = False  # 终止循环

        ##### -引号外，MyCnLang语句- #####
        elif (in_str is False) and char in '()[]|（）【】{},，:：':
            # 字符串外，分隔出括号、逗号等语法元素
            submit_and_clear_token()
            C_to_E_sign = {'（': '(', '）': ')', '【': '[', '】': ']',
                           '，': ',', '：': ':'}
            if char in C_to_E_sign.keys():  # 中文字符统一转化成英文字符
                tokens.append(C_to_E_sign[char])
            else:
                tokens.append(char)
        elif  (in_str is False) and char in '+-*/':
            # +-*/
            submit_and_clear_token()
            tokens.append(char)
        elif (in_str is False) and char in '><!=':
            # >、<、>=、<=、=、==、!=
            submit_and_clear_token()
            if string.nextchar() == '=':  # >=、<=、==、!=
                tokens.append(char + string.popchar())
            else :    # =、>、<
                tokens.append(char)
        elif (in_str is False) and char == '#':
            # 注释，'#'后面的字符全部抛弃，直到换行符
            submit_and_clear_token()
            string.popuntil('\n')
        elif (in_str is False) and char in '\n;；':
            # MyCnLang使用 换行符'\n' 和 分号';；' 划分语句，这里统一转化为';'
            submit_and_clear_token()
            tokens.append(';')
        elif (in_str is False) and char == ' ':
            # 空格区分各语法元素
            submit_and_clear_token()

        elif (in_str is False) and char in quo_mark_d.keys():
            # 引号外遇到引号，后面是字符串
            submit_and_clear_token()
            in_str = True   # 我们进入字符串
            quo_mark = char # 保存正引号，将通过它确认反引号
            token += "'"    # 无论这个字符串是使用什么引号引起，我们都使用英文半角单引号
                            # 标记这个字符串

        ##### -引号内，MyCnLang字符串- #####
        elif (in_str is True) and char == quo_mark_d[quo_mark]:
            # 字符串内遇到对应的反引号，字符串结束
            token += "'"    # 字符串前后统一为英文半角单引号
            submit_and_clear_token()
            in_str = False  # 字符串终止，后面的内容不在字符串里
        elif (in_str is True) and char in '\\《':
            # 识别转义字符
            if string.nextchar() in 'nrtbfva':  # 转义字符
                token += dict(zip('nrtbfva', '\n\r\t\b\f\v\a'))[string.popchar()]
                # 使用dict(zip())创建一个字典，当'\'下一个字符为n时，返回'\n'，以此类推
            else :    # 不是专门的转义字符，后面的字符直接放到字符串中，以实现'\"'、'\\'等
                token += string.popchar()

        ##### -一般字符- #####
        else :  # 一般字符加入token
            token += char

    else:
        return tokens

def abstract_syntax_tree(tokens: list) -> list:
    '''将split_tkens分割出来的语法元素处理成抽象句法树'''
    tree = []
    sentence = []

    while True:
        if tokens:  # 检查，防止报错
            token = tokens.pop(0)
        else:
            if sentence:
                tree.append(sentence)
            return tree[0] if len(tree) == 1 else tree # tokens弹出完，只返回tree。
                                                       # 如果列表中只有一个列表，解嵌套
        if token == ';':
            if sentence:
                tree.append(sentence)
                sentence = []
        elif token == '(':
            ret, tokens = abstract_syntax_tree(tokens)  # 递归处理
            sentence.append(ret)
        elif token == ')':
            if sentence:
                tree.append(sentence)
            tree = tree[0] if len(tree) == 1 else tree  # [['a']] -> ['a']防止单语句过多列表嵌套
            return tree, tokens
        else:
            sentence.append(token)

def split_list_by_comma(l: list[str|list]) -> list[str|list]:
    '''
    根据列表中的','来分隔列表，如['a',  ',',  'b', 'c',  ',',  'd'] -> ['a', ['b', 'c'], 'd']
    用于处理MyCnLang函数的传参等需要使用','来分隔元素的情况
    '''
    splited_l = []
    tokens    = []

    for token in l:
        if (tokens.count('[') != tokens.count(']') or\
            tokens.count('{') != tokens.count('}')
        ):  # 列表和字典中的逗号应该保存
            tokens.append(token)
        elif token == ',':
            if tokens:
                splited_l.append(tokens if len(tokens) > 1 else tokens[0])
                tokens = []
            else :
                splited_l.append(None)  # 允许通过', ,'连续两个逗号的方式传递空值
        else :
            tokens.append(token)
    else :  # 保证最后一个元素压入splited_l中
        if tokens:
                splited_l.append(tokens if len(tokens) > 1 else tokens[0])

    return splited_l
#################### -MyCnLang求解器- ####################
def evaluate(expression: list, STACK = STACK):
    '''MyCnLang的求解器，求解MyCnLang表达式'''
    match expression:

        # 赋值语句
        case [n, '='|'为', *v] if v:    #  赋值
            # 年龄 为 18 ;    年龄 = 18
            STACK[n] = evaluate(v)
        case ['STACK', '[', scope_level, ']', ':', n, '='|'为', *v] if v: # 跨作用域赋值
            # 修改任意层级作用域的变量，scope_level应为数字（建议为负数）
            # STACK[-2]:age = 18 ;   STACK[-2]：年龄 为 18    # -2 修改上层作用域
            scope_level = evaluate(scope_level)
            if isinstance(scope_level, int):
                STACK._stack[scope_level][n] = evaluate(v)
            else:
                raise 语法错误(f'STACK[n]中，n应该是整型')
        case [str(n), '[', i, ']', '='|'为', *v]|[str(n), ':', i, '='|'为', *v]\
                if v and isinstance(STACK[n], (list, dict)):  # 字典、列表元素修改
            # 学生列表[2] = '小红'    学生字典['小明'] = 13
            STACK[n][evaluate(i)] = evaluate(v)
        case [*names, '='|'为', values]\
                if names and values and all([isinstance(n, str) for n in names]): # 多变量赋值
            # a, b, c = ([1, 2, 3])    或者    a  b  c = ([1, 2, 3])
            # 值得一提的是，逗号','将会被扔掉，不影响行为，使用空格分隔完全可以
            names = [n for n in names if n != ',']  # 抛弃','
            the_names = ''
            for n in names:  # 生成命令
                the_names += f'STACK["{n}"],'
            exec(f'{the_names}=evaluate(values)')
            del names, the_names

        # 上层作用域变量，放在这里是为了防止被当作函数解析
        case ['STACK', '[', scope_level, ']', ':', n]:    # 查看上层作用域的变量
            # STACK[0]:stu_name    STACK[(-2)]:age
            scope_level = evaluate(scope_level)
            if isinstance(scope_level, int):
                return STACK._stack[scope_level][n]
            else:
                raise 语法错误(f'STACK[n]中，n应该是整型')

        # 条件语句
        case ['if'|'如'|'如果', condition, cmd1, 'else'|'否则', *cmd2]|\
             [*cmd1, 'if'|'如'|'如果', condition, 'else'|'否则', cmd2] if cmd1 and cmd2:
            # if-else语句（如果/如-否则），亦可以使用‘else if’来作为elif使用
            evaluate(cmd1) if evaluate(condition) else evaluate(cmd2)
        case ['if'|'如'|'如果', condition1, cmd1, 'elif'|'又如果', *other] if other:
            # if-elif-...-elif-else 语句（如果-又如果-...-又如果-否则）
            if evaluate(condition1):
                evaluate(cmd1)
            else :
                evaluate( ['如果'] + other )  # 将elif拼接成if-else语句
        case ['if'|'如'|'如果', *condition, cmds]|\
             [*cmds, 'if'|'如'|'如果', condition] if cmds and condition:
            # 如果 （年龄 >= 18）（输出（‘成年’））
            # 输出（‘成年’） 如果 （年龄 >= 18）
            if evaluate(condition):
                evaluate(cmds)

        # 循环语句
        case [n, 'in'|'属于', *v, list(cmd)]|\
             [*cmd, n, 'in'|'属于', v] if v and cmd:  # for
            # for循环
            # 学生 属于 学生列表（输出（学生））    单句循环：  输出（学生） 学生 属于 学生列表
            for STACK[n] in evaluate(v):
                evaluate(cmd)
        case ['while'|'当', *condition, cmd]|\
             [cmd, 'while'|'当', *condition] if condition:  # while
            # while当型循环语句，允许while后置
            # 当 年龄 < 18（输出（‘未成年’）； 年龄 = 年龄 + 1）
            while evaluate(condition):
                evaluate(cmd)

        # 错误处理
        case ['try'|'尝试', cmd, 'except'|'如报错', if_err]:
            # 捕获所有Exception错误
            try:
                evaluate(cmd)
            except Exception:
                evaluate(if_err)
        case ['try'|'尝试', cmd, 'except'|'如报错', e, if_err]:
            # 单个错误捕获
            # 尝试（输出（a））如报错 变量未定义（输出（‘错误’））
            try:
                evaluate(cmd)
            except eval(e): # 使用eval获取要捕获的错误
                evaluate(if_err)
        case ['try'|'尝试', cmd, 'except'|'如报错', e, if_err, 'except'|'如报错', *other]\
                                                                        if other:
            # 同时捕获多个错误
            try:
                evaluate(cmd)
            except eval(e):
                evaluate(if_err)
            except :  # 不是这个错误，构建语句继续运行捕获
                evaluate( ['尝试', cmd, '如报错'] + other )

        # 一些关键字
        case ['import'|'导入', *files] if files:  # 导入文件
            files = [f for f in files if f != ',']  # 忽略','
            for f in files:
                run_file(f)
            del files

        case ['System', *cmd] if cmd:  # 系统命令
            import os
            os.system(evaluate(cmd))
        case ['PythonExec', *cmd] if cmd:  # exec()
            exec(evaluate(cmd))
        case ['PythonEval', *cmd] if cmd:  # eval()
            return eval(evaluate(cmd))
        case ['eval'|'解析', *cmd] if cmd:  # 解析MyCnLang语句
            # 解析 ‘a’  # 变量        解析 ‘输出（“你好”）’  # 语句
            return evaluate(parse(evaluate(c)))

        case ['watch'|'help'|'查看', n]:
            if isinstance(STACK[n], MycnlangFunction):
                print(STACK[n]._body[0])
            else :
                print(STACK[n].__repr__)
        case ['free'|'del'|'释放', *n] if n:    # 删除变量
            # 释放 a, b
            for i in [a for a in n if a != ',']:
                del STACK[i]
        case ['have'|'存在', *n] if n:   # 检查一个变量是否存在
            # 如果变量全部存在，返回True，否则返回False
            n = [i for i in n if (i != ',' and isinstance(i, str))]
            try:
                for i in n:
                    STACK[i]
            except 变量未定义:
                return False
            else :
                return True
        case ['return'|'返回', *r]:   # 函数返回，没有提供则为None
            raise RETURN(evaluate(r) if r else None)
        case ['raise'|'报错', e, *msg]:  # 提起异常
            raise eval(e)(evaluate(msg) if msg else '')
        case ['call'|'调用', func]:   # 函数无参调用
            return evaluate([func, []])
        case ['exit'|'quit'|'终止']:  # 终止程序
            from sys import exit
            exit()

        case ['stack_push', *d]:
            STACK.push(evaluate(d) if d else {})
        case ['stack_pop'] :
            STACK['@r'] = STACK.pop()
            return STACK['@r']
        case ['stack_show']:
            STACK.show()

        # 数学运算 和 条件判断
        case [*a, str(operators), b] if (operators in '+-*/') and a:
            return eval(f'evaluate(a) {operators} evaluate(b)')

        case ['!'|'！'|'not'|'非', *n] if n:
            return not evaluate(n)
        case [*test1, 'and'|'与'|'和'|'且', test2] if test1:
            # test1捕获更多是为了保证 ...and...and...and...中，第一个and会先执行
            # 实际每一个条件应该使用括号括起，下面的or同理
            return evaluate(test1) and evaluate(test2)
        case [*test1, 'or'|'或', test2] if test1:
            return evaluate(test1) or evaluate(test2)
        case [n1, '=='|'等于', n2]:
            return evaluate(n1) == evaluate(n2)
        case [n1, '!='|'不等于', n2]:
            return evaluate(n1) != evaluate(n2)
        case [n1, '>'|'大于', n2]:
            return evaluate(n1) > evaluate(n2)
        case [n1, '<'|'小于', n2]:
            return evaluate(n1) < evaluate(n2)
        case [n1, '>='|'大于等于', n2]:
            return evaluate(n1) >= evaluate(n2)
        case [n1, '<='|'小于等于', n2]:
            return evaluate(n1) <= evaluate(n2)

        case [n1, 'in'|'属于', *n2] if n2:   # 'a' in ['a', 'b', 'c']
            return evaluate(n1) in evaluate(n2)

        # 数字、字符串、列表、字典、bool
        case int(n)|float(n) | [int(n)]|[float(n)]:   # 括号中的数字给予保留
            return n
        case str(n)|[str(n)] if n and n[0] in '0123456789.':   # int和float
            # 以'0123456789.'其中一个字符为开头的是数字，就像Python一样
            from ast import literal_eval
            try:
                return literal_eval(n)
            except ValueError:
                raise 语法错误(f"'{n}'不是一个合法的整型或浮点型")
        case ['-', *n] if n:    # 负数
            return - evaluate(n)

        case str(s)|[str(s)] if s[0]=="'" and s[-1]=="'": # 字符串
            # 字符串，及前后都被引号引起的元素
            return s[1:-1]    # 丢弃前后的引号

        case ['list'|'列表', *l]:   # 列表
            # 列表 1 2 3 4    # 不需要逗号
            return [evaluate(i) for i in l]
        case ['[', *l, ']']:   # 列表
            # [1, 2, 3, 4]   # 需要逗号分隔
            return [evaluate(i) for i in split_list_by_comma(l)]

        case ['dict'|'字典', k, v]:   # 字典
            # dict 'a' 13
            # 字典  （['a', 'b', 'c']） （[1, 2, 3]）
            return dict(zip(evaluate(k), evaluate(v)))
        case ['{', *items, '}']:     # 字典
            # { a=1, b=2, c -> '3', d -> [1, 2, 3], e->range(8)}
            d = {}
            items = split_list_by_comma(items)
            for item in items:
                match item:
                    case [str(k), '-', '>', *v]|[str(k), '='|':', *v] if v:
                        d[k] = evaluate(v)
                    case _:
                        raise 语法错误(f'\n\t{item}\n字典定义语句不合法')
            return d

        case [str(n), '[', i, ']']|[str(n), ':', i]\
                if isinstance(STACK[n], (list, dict)): # 字典、列表元素读取
            # 通过索引访问列表元素，当需要访问-1、-2时，要使用括号括起，如（-2），这当然可以
            # 使用 *i 避免，这事为了与 STACK[(-1)] 相同

            # 学生列表[2]    学生列表：1    学生列表[(-1)]    学生列表：（-1）
            # 同样可以以这种方法读取字典的值，如 学生字典['小明']
            return STACK[n][evaluate(i)]

        case '真'|['真']|'True'|['True']   | True|[True]:
            return True
        case '假'|['假']|'False'|['False'] | False|[False]:
            return False
        case '空'|['空']|'None'|['None']   | None|[None]:
            return None

        # 函数
        case ['def'|'函数', func, list(argv), list(body)]:  # 函数定义
            # 函数 相加（a, b）（返回 a+b）
            if all([isinstance(a, str) for a in argv]) is False:
                raise 语法错误(f'\n\t{expression}\n参数名不合法')
            STACK[func] = MycnlangFunction(
                argv=[a for a in argv if a != ','],  body=body
            )
        case [str(func), list(argvs)]\
                if isinstance(STACK[func], MycnlangFunction): # 函数调用
            # 相加（1, 2）
            if isinstance(STACK[func], MycnlangFunction):  # 函数
                argvs = split_list_by_comma(argvs)
                return STACK[func].call([evaluate(argv) for argv in argvs])
            else :    # 不是函数
                raise 类型错误(f'\n\t{expression}\n{func}是一个{STACK[func].__class__.__name__}值，不是MyCnLang函数')
        case [str(func), *argvs]\
                if argvs and isinstance(STACK[func], MycnlangFunction): # 函数调用
            # 相加 1 2    # 不用逗号分隔参数，每个参数必须是但个元素
            if isinstance(STACK[func], MycnlangFunction):
                return STACK[func].call([evaluate(argv) for argv in argvs])
            else :    # 不是函数
                raise 类型错误(f'\n\t{expression}\n{func}是一个{STACK[func].__class__.__name__}值，不是MyCnLang函数')

        # 变量
        case str(n)|[str(n)]:   # 变量
            return STACK[n]

        # 不符合上述MyCnLang语法
        case [*exprs] if all([isinstance(expr, list) for expr in exprs]):
            # 括号中的多行语句，依次执行
            if len(exprs) == 1:   # 当仅有一条语句时，可能是过多嵌套的语句，应返回其结果
                return evaluate(exprs[0])
            for expr in exprs:
                evaluate(expr)

        case _:
            raise 语法错误(f'\n\t{expression}\n无效语法')


#################### -repl 和 MyCnLang文件运行- ####################
def repl():
    '''MyCnLang的 read-evaluate-print loop（读取-求值-输出 循环）'''
    print('''\
MyCnLang  2026/8/19  (Python 3.13 in Linux)

MyCnLang repl( read-evaluate-print loop（读取-求值-输出 循环） )
解释运行我自定义的MyCnLang语法，支持中文关键字和中文符号。编写于
Linux 6.18.12+kali-amd64 Python 3.13。2026/8/19最后一次修改

程序地址：
https://github.com/yunjiao20/my-first-repository/tree/main/my-pro-lang/MyCnLang

Ctrl+C终止repl，或在repl键入`exit`、`quit`、`终止`指令终止程序''')

    loop = True
    while loop:

        try:
            i = split_tokens(input('MyCnLang > '))  # 先将元素区分开来

            while i.count('(') != i.count(')'):  # 语句不完整（括号没闭合），继续获取输入
                i += split_tokens('\n' + input('.......... '))

            output = evaluate(abstract_syntax_tree(i)) # 前面只将tokens区分开来了
        except KeyboardInterrupt:  # Ctrl+C终止程序
            import sys
            sys.exit()
        except Exception as e:     # 显示报错信息
            print(f'{e.__class__.__name__}: {e.__str__()}')
        else :
            if output != None:
                print(output.__repr__())

def run_file(filename: str):
    '''运行MyCnLang文件'''
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            evaluate(parse(f.read()))
    except FileNotFoundError:
        raise 文件不存在(f'MyCnLang没有发现文件 {filename}')

def main():
    '''当没有提供参数时，打开repl；提供了文件名时，运行MyCnLang文件'''
    from sys import argv

    STACK['@argv'] = argv
    for i in range(len(argv)):
        exec(f'STACK["@{i}"] = argv[{i}]')

    match argv:

        case a if len(argv) == 1:    # 没有提供参数
            repl()

        case ['-c', *cmd]:
            if cmd:
                evaluate(cmd)
            else :
                print('你没有提供MyCnLang指令，运行`mycnlang -h`查看帮助')

        case ['-h'|'--help']:
            print('''\
mycnlang
        -c [cmd]        运行MyCnLang代码
        -h / --help     查看此帮助信息
        [mycnlang文件]   解释运行mycnlang文件''')

        case _:    # 依次运行文件
            for f in argv[1:]:
                run_file(f)


#################### -MyCnLang初始环境(内置函数)- ####################
# 定义一些内置函数
evaluate(parse('''
函数 输出（）（
    “将你提供的所有参数打印到终端”
    PythonExec “print(STACK['s'], end='')” s 属于 @argv
    PythonExec “print()”
）
函数 读取（s）（
    “输出参数s，并暂停程序等待用户输入，用户输入以字符串形式返回”
    如果 （存在 s）（
        返回 PythonEval ‘input(STACK['s'])’
    ）否则 （
        返回 PythonEval ‘input()’
    ）
）

函数 数列（）（
    “Python range()”
    如果 @argv（
        a 为 PythonEval '[str(n) for n in STACK["@argv"]]'
        range_argv_s 为 PythonEval ‘','.join(STACK['a'])’
        返回 PythonEval ‘list(range(’ + range_argv_s + ‘))’
    ）否则（
        报错 类型错误 ‘函数'数列'（range）缺少参数’
    ）
）

函数 整型（n）（
    “接受一个参数，尝试将其转换为整型并返回”
    尝试（
        返回 PythonEval “int(MyCnLang['n'])”  # 原来只允许用户使用'STACK[]'访问栈获取MyCnLang变量，
    ）如报错 ValueError（                      # 现在‘MyCnLang’也持有‘STACK’的引用，使用‘MyCnLang[]’
        报错 类型错误 字符串型（n）+ ‘ 不能转换成整型’        # 获取MyCnLang变量或许会更好理解一点
    ）如报错 变量未定义（
        报错 变量未定义 ‘你没有给函数'整型'提供参数’
    ）
）
函数 浮点型（n）（
    “接受一个参数，尝试将其转换为浮点型并返回”
    尝试（
        返回 PythonEval “float(MyCnLang['n'])”
    ）如报错 ValueError（
        报错 类型错误 字符串型（n）+ ‘ 不能转换为整型’
    ）如报错 变量未定义（
        报错 变量未定义 ‘你没有给函数'浮点型'提供参数’
    ）
）
函数 字符串型（s）（
    “接受一个参数，返回其字符串形式”
    尝试（
        返回 PythonEval “str(MyCnLang['s'])”
    ）如报错 变量未定义（
        报错 变量未定义 ‘你没有给函数'整型'提供参数’
    ）
）





print = 输出
input = 读取
range = 数列
int   = 整型
float = 浮点型
str   = 字符串型
'''))



#################### -main- ####################
if __name__ == '__main__':
    main()
