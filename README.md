# my-first-repository
## AST.py

### 1.请注意, 这里并不建议您在任何情况中直接使用这个漏洞百出的工具, 它的出现只是因为一个个人临时的需要. 而如果您因为一些原因需要使用或自定义它, 下面的内容可能会给你一些帮助
     
### 2.AST.py的使用
  
- AST.py使用Python3.12.4编写, 请注意版本兼容问题. 这个小小的脚本不值得使用虚拟环境     

- 如果你使用 Windows系统, 您可以在AST.py所处当前目录使用命令[python3 AST.py]使用它    
- 如果你使用 Linux系统, 您依然可以使用以上命令. 而您若想使用 ./ 直接运行它, 您需要使用 vim[:set ff=unix]命令改变其文件格式, 因为它是在 Windows系统上编写的    

- 示例:
  - 成功运行AST.py之后, 您应该能看到以下输出:    

         __    __                    __          _______   __________ 
        |  |  |  |   __             /  \        /  ____ \  \___  ___/ 
        |  |__|  |  |__|           /    \      /  /____\/     |  |
        |   __   |  |  |   __     /  /\  \     \______  \     |  |
        |  |  |  |  |  |  |__|   /  ____  \    /\____/  /     |  |
        |__|  |__|  |__|    |/  /__/    \__\  /________/      |__|
        -----------------------welcome to the AST-----------------------
        Python programe AST.py 0.01 ...... You can include "h" in input message to watch help message
        Please watch document https://github.com/yunjiao20/my-first-repository if you need

        <AST>
  - 输入错误的命令, 您将会看到帮助:
    
          <AST> k
          你可以在输入中包含 h 以打印帮助信息
          <AST>
  - 输入 'h' :
    
          <AST> h
          v    --print version message 输出版本信息
          h    --print help message 输出帮助信息
          m    --cleartext to morse code 将明文转换为莫尔斯电码,输入 q 退出该模式
          M    --morse code to cleartext 将莫尔斯电码转换为明文,输入 q 退出该模式
          a    --cleartext to ASCLL 将明文转换为ASCLL码,输入 q 退出该模式(16进制)
          A    --ASCLL to cleartext 将ASCLL码转换为明文,输入 q 退出该模式
          q    --end programe 终止程序

          <AST>

  - 这边假设您需要使用m功能:
    
          <AST> m
                  将明文翻译为莫尔斯电码,请注意,莫尔斯电码不分大小写,您必须输入大写英文(请注意,替换列表并不完整)
          <AST/Morse_code>
     

  - 根据提示输入字符:
     
          <AST/Morse_code> HELLO WORLD
          .... . .-.. .-.. ---    .-- --- .-. .-.. -.. 
          <AST/Morse_code> HHH!
          .... .... .... !不可识别字符! 
          <AST/Morse_code>

  - 输入 q 退出该模式:
    
          <AST/Morse_code> q
          <AST> 

  - 在<AST>下输入 q 终止程序:
    
          <AST> q
          Programe AST.py end

          PS C:\Users\Unknown\Desktop> 

### 3.如果您需要在实际生活中使用, 须知:
- 翻译字典并不完整, 如您需要使用这个工具的话, 您可能需要手动补全所需字典内容   
- 在 M模式下, 不包含在翻译字典中的字符将会返回'?', 翻译字典中不含'?',即使莫尔斯电码中确实有'?'的编码同时, 哪怕您输入了三个空格符, M 也不会返回一个空格符以符合莫尔斯电码的标准, 这是因为程序在这里是使    用.split()来处理您的输入
- 在 A模式下, 如果您的输入不包含空格符, 程序将会自动按每2位为一个 ASCLL码翻译, 此时, 如您输入的字符串数为单数, 您的最后一个字符将会被丢弃    
  如您的输入中包含空格符, 将会使用.split()来处理您的输入, 如果这个空格符是不小心混进去的, 它将会导致程序将您的一长段输入当成一个字符翻译, 最终导致无法返回任何有价值的信息    
  
### 4.自定义AST:        
- 程序的翻译行为依靠morse_code和 ASCLL两个字典, 您将可以通过更改这两个字典来借用 AST的替换功能    
- 如您在morse_code字典中添加了 ?字符的莫尔斯码, 您可以在AST.py源码的第 158行(函数 get_key_by_value()的return语句)修改 M模式的查找失败返回信息    
- 如果您需要改变 M模式无法将三个空格符替换为一个空格符的问题, 请修改 morse_code_to_str()函数, 编写一个处理函数并插入到源码193行. 或者如果有人会关注这个项目的话(当然这有点不太可能) , 我可能会尝试编写一个复杂又难懂的函数来尝试解决它      

## card_game.py
  . 施工中...
