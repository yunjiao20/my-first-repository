#!/bin/python
'''
基于Python3.12.4, 用于完成一些简单替换任务的脚本程序, 只用于不完整莫尔斯电码和不完整ASCLL码的替换
因为是在Windows上编写的, 您可能需要利用vim转变换行符以在Linux上运行
'''

morse_code = {
    'A' : '.-',
    'B' : '-...',
    'C' : '-.-.',
    'D' : '-..',
    'E' : '.',
    'F' : '..-.',
    'G' : '--.',
    'H' : '....',
    'I' : '..',
    'J' : '.---',
    'K' : '-.-',
    'L' : '.-..',
    'M' : '--',
    'N' : '-.',
    'O' : '---',
    'P' : '.--.',
    'Q' : '--.-',
    'R' : '.-.',
    'S' : '...',
    'T' : '-',
    'U' : '..-',
    'V' : '...-',
    'W' : '.--',
    'X' : '-..-',
    'Y' : '-.--',
    'Z' : '--..',
    '0' : '-----',
    '1' : '.----',
    '2' : '..---',
    '3' : '...--',
    '4' : '....-',
    '5' : '.....',
    '6' : '-....',
    '7' : '--...',
    '8' : '---..',
    '9' : '----.',
    '(' : '-.--.',
    ')' : '-.--.-',
}

ASCLL = {
    ' ' : '20',
    '0' : '30',
    '1' : '31',
    '2' : '32',
    '3' : '33',
    '4' : '34',
    '5' : '35',
    '6' : '36',
    '7' : '37',
    '8' : '38',
    '9' : '39',
    ':' : '3A',
    'A' : '41',
    'B' : '42',
    'C' : '43',
    'D' : '44',
    'E' : '45',
    'F' : '46',
    'G' : '47',
    'H' : '48',
    'I' : '49',
    'J' : '4A',
    'K' : '4B',
    'L' : '4C',
    'M' : '4D',
    'N' : '4E',
    'O' : '4F',
    'P' : '50',
    'Q' : '51',
    'R' : '52',
    'S' : '53',
    'T' : '54',
    'U' : '55',
    'V' : '56',
    'W' : '57',
    'X' : '58',
    'Y' : '59',
    'Z' : '5A',
    'a' : '61',
    'b' : '62',
    'c' : '63',
    'd' : '64',
    'e' : '65',
    'f' : '66',
    'g' : '67',
    'h' : '68',
    'i' : '69',
    'j' : '6A',
    'k' : '6B',
    'l' : '6C',
    'm' : '6D',
    'n' : '6E',
    'o' : '6F',
    'p' : '70',
    'q' : '71',
    'r' : '72',
    's' : '73',
    't' : '74',
    'u' : '75',
    'v' : '76',
    'w' : '77',
    'x' : '78',
    'y' : '79',
    'z' : '7A',
    '{' : '7B',
    '}' : '7D'
}



def start_page():
    '''打印开始界面'''
    print(r'  __    __                    __          _______   __________ ')
    print(r' |  |  |  |   __             /  \        /  ____ \  \___  ___/ ')
    print(r' |  |__|  |  |__|           /    \      /  /____\/     |  |    ')
    print(r' |   __   |  |  |   __     /  /\  \     \______  \     |  |    ')
    print(r' |  |  |  |  |  |  |__|   /  ____  \    /\____/  /     |  |    ')
    print(r' |__|  |__|  |__|    |/  /__/    \__\  /________/      |__|    ')
    print(r'-----------------------welcome to the AST-----------------------')
    print(r'Python programe AST.py 0.01 ...... You can include "h" in input message to watch help message')
    print('\n')

def print_version_message():
    '''输出版本信息'''
    print('基于Python 3.12.4   AST.py 0.01   2025/1/18 第一版')
    print('\n')

def print_help_message():
    '''打印帮助信息'''
    print('v    --print version message 输出版本信息')
    print('h    --print help message 输出帮助信息')
    print('m    --cleartext to morse code 将明文转换为莫尔斯电码,输入 q 退出该模式')
    print('M    --morse code to cleartext 将莫尔斯电码转换为明文,输入 q 退出该模式')
    print('a    --cleartext to ASCLL 将明文转换为ASCLL码,输入 q 退出该模式(16进制)')
    print('A    --ASCLL to cleartext 将ASCLL码转换为明文,输入 q 退出该模式')
    print('q    --end programe 终止程序')
    print('上键返回上次输入')

    print('\n')

def get_key_by_value(字典: dir, 查找值: str):
    '''
    通过值寻找键(查了一下, 竟然木有相关的函数, 只能自己写轮子了)\n
    接受一个字典和一个字符串, 遍历字典的值并返回相关的键
    '''
    for k, v in 字典.items():
        if v == 查找值:
            return(k)
    return('?')

def str_to_morse_code():
    '''封装一段行为, 返回一个命令行交互界面, 将明文翻译为莫尔斯电码'''
    print('\n\t将明文翻译为莫尔斯电码,请注意,莫尔斯电码不分大小写,您必须输入大写英文(请注意,替换列表并不完整)')
    while True:
        return_message = ''
        input_message = input('<AST/Morse_code> ')

        if input_message == 'q':    #当输入为q时, 终止循环
            break

        for i in input_message:
            # 遍历输入字符
            if i != ' ':
                try:
                    return_message += f'{morse_code[i]} '  #每代表一个字母的电码后面加一个空格
                except KeyError:
                    return_message += '!不可识别字符! '
            else:    #如果i为空, 返回3个空格
                return_message += '   '
        print(return_message)

def morse_code_to_str():
    '''封装一段行为, 返回一个命令行交互界面, 将莫尔斯电码翻译为明文'''
    print('\n\t将莫尔斯电码翻译为明文')
    print('\t遇到无法翻译的电码,将会返回 ? ,正常输出不含 ? ,即使莫尔斯电码中确实有 ?')

    while True:
        return_message = ''
        input_message = input('<AST/re_Morse_code> ')

        if input_message == 'q':    #当输入为q时, 终止循环
            break
        
        input_message_list = input_message.split() #按空格分割输入字符串, 返回一个list

        for i in input_message_list:
            return_message += get_key_by_value(morse_code, i)  #根据字典的值返回键
        print(return_message)


def 按2位分列表(input_str):
    '''将字符串每2位分开,制成列表, 以方便对用户输入的无分隔16进制信息的处理'''
    return_list = []
    a = ''
    for i in input_str:
        a += i
        if len(list(a)) >= 2:    # 当传入字符数为单数时, 会丢弃最后一个字符
            return_list.append(a)
            a = ''
    return(return_list)

def str_to_ASCLL():
    '''将明文翻译为ASCLL码'''
    print('\n\t将明文翻译为ASCLL码(16进制),请注意表单并不完善,所有未识别字符将以 ? 输出')
    while True:
        return_message = ''
        input_message = input('<AST/ASCLL> ')

        if input_message == 'q':
            break

        for i in input_message:
            try:
                return_message += ASCLL[i]
            except KeyError:
                return_message += '?'
        print(return_message)

def ASCLL_to_str():
    '''将ASCLL码翻译为明文'''
    print('\n\t将ASCLL码翻译为明文')
    while True:
        return_message = ''
        input_message = input('<AST/reASCLL> ')

        if input_message == 'q':
            break

        if ' ' in input_message:
            # 当输入中存在空格符时
            input_message_l = input_message.split()    # 按空格符分隔列表, 因此, 请不要在需要自动划分时传入空格符,
                                                       # 否则将导致错误划分列表从而无法转换
        else :
            input_message_l = 按2位分列表(input_message)
        
        for i in input_message_l:
            return_message += get_key_by_value(ASCLL, i)
        print(return_message)



def run():
    '''主函数,运行程序并调用处理函数'''
    start_page()
    while True:
        input_message = input('<AST> ')
        sign = True    # 指示是否输出帮助信息

        if input_message == 'q':
            print('Programe AST.py end\n')
            break    # 终止程序

        if 'v' in input_message:
            print_version_message()
            sign = False
        if 'h' in input_message:
            print_help_message()
            sign = False
        if 'm' in input_message:
            str_to_morse_code()
            sign = False
        if 'M' in input_message:
            morse_code_to_str()
            sign = False
        if 'a' in input_message:
            str_to_ASCLL()
            sign = False
        if 'A' in input_message:
            ASCLL_to_str()
            sign = False 

        if sign:      #当 sign 为 True 时,以上处理均未触发,输出帮助信息
            print('你可以在输入中包含 h 以打印帮助信息')


if __name__ == '__main__':    #当此程序被运行而非被调用时
    run()
