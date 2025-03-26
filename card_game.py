'''一个类三国杀的单人游戏'''
# 我当时真是傻逼, 竟然把所有代码都塞到一个文件来, 注释不是很充足, 假期再改
# 使用Python3.12.4编写, 使用其他Python版本注意兼容问题(废话~)
# 存在一些逻辑bug和不充足交互提示问题, 有假期再改
# Linux请使用vim[:set ff=unix]修改换行符, 微软中文好用捏, 但Python支持真TM狗屎(痛苦面具ing)
from random import randint, choice

card_d = {     #创建一个字典,以便后面通过数字获取卡牌
    '1' : '1.杀',
    '2' : '2.闪',
    '3' : '3.桃',
    '4' : '4.兵临城下',
    '5' : '5.抽',
    '6' : '6.粮',
    '7' : '7.丰',
    '8' : '8.混战',
    '9' : '9.水',
    '10' : '10.火',
    '11' : '11.大动干戈',
    '12' : '12.釜底抽薪',
    '13' : '13.雷电',
    '14' : '14.命',
    '15' : '15.运',
}



class Player:
    '''定义玩家基本行为的类,以转为玩家和敌方的父类'''
    def __init__(self):
        '''定义基本信息及其默认值'''
        self.血量 = 4
        self.血量上限 = 4
        self.持有卡牌 = []
        self.每回合摸牌数 = 2
        
        # 字典推导式,返回一个键 0~99 ,值False 的字典
        self.回合 = {k: v
                   for k, v in zip(range(100), [False]*100)}
        self.回合数 = 0

    def 摸牌(self):
        '''定义摸牌行为'''
        a = randint(1, 100)

        if a <= 60:
            摸到的牌 = choice(['1.杀', '1.杀', '1.杀', '1.杀', '2.闪', '2.闪', '2.闪', '3.桃', '3.桃']) # 60%摸到基础牌
        elif a <= 90:
            摸到的牌 = choice(['4.兵临城下', '5.抽', '6.粮', '7.丰', '8.混战', '9.水', '10.火', '11.大动干戈', '12.釜底抽薪'])  # 30%摸到功能牌
        else :
            摸到的牌 = choice(['13.雷电', '14.命', '15.运']) # 10%摸到特殊牌

        self.持有卡牌.append(摸到的牌)  #将摸到的牌放入玩家卡槽

    def 此回合摸牌(self):
        '''摸取等同于 self.每回合摸牌数 的牌'''
        for _ in range(self.每回合摸牌数):
            self.摸牌()

    def 得牌(self, 卡牌: str):
        '''玩家得到特定手牌,为手牌 抽 功能的实现提供帮助'''
        self.持有卡牌.append(卡牌)

    def 输出玩家信息(self):
        '''按特定格式输出玩家信息'''
        # 玩家身份
        # 血量:  # # # #
        # 卡牌数 or 持有卡牌

    def 弃牌(self, 卡牌: str):
        '''从持有卡牌中弃掉特定卡牌,请输入例如  1.杀 2.闪 3.桃 '4.兵临城下', '5.抽', '6.粮', '7.丰', '8.混战', '9.水', '10.火', '11.大动干戈', '12.釜底抽薪''13.雷电', '14.命', '15.运' '''
        if 卡牌 in self.持有卡牌:
            self.持有卡牌.remove(卡牌)

    def 判定(self) -> bool:
        '''随机返回 True 或 False, 实现概率性功能'''
        return(choice([True, False]))
        
    def 血量改变(self, 改变量: int):
        '''实现血量的加减'''
        if self.血量 + 改变量 <= self.血量上限:
            self.血量 += 改变量

    def 是否死亡(self) -> bool:
        '''检查玩家是否死亡,血量小于等于1时返回True,否则返回False'''
        if self.血量 <= 0:
            return(True)
        return(False)
    
    

# 将两方的卡牌行为合并起来太难实现了,直接分别定义两方行为算了
class 我方(Player):
    '''定义玩家的行为和出牌'''
    def __init__(self):
        super().__init__()    # super()函数调用了父类的 __init__ 方法,使继承父类属性

    def 输出玩家信息(self):
        print('\t我方状态: ')
        print(f'\t\t血量: {'# ' * self.血量}')
        print(f'\t\t卡牌: {self.持有卡牌}')

    def 杀(self, 承受者: Player):
        '''定义玩家出 杀 时敌方的行为: 出闪,桃,运, 否则扣一点血'''
        if self.回合[self.回合数]:    #如果本回合为 True ,
            print('\t每回合只能出 杀 一次')
            return    # 退出函数
        
        if '1.杀' in self.持有卡牌:   #当玩家手牌中有杀时
            self.弃牌('1.杀')
            self.回合[self.回合数] = True   #将本回合改为 True 
                                            #记得在结束本回合时让 回合数+=1
            if '2.闪' in 承受者.持有卡牌:
                承受者.弃牌('2.闪')
                print('\t敌方应对> 闪')
            elif '3.桃' in 承受者.持有卡牌:
                承受者.弃牌('3.桃')
                print('\t敌方应对> 桃')
            elif '15.运' in 承受者.持有卡牌:
                print('\t敌方应对> 运')
                if 承受者.判定():     # 如果判定返回 True
                    print('\t\t判定结果: True')
                else:
                    print('\t\t判定结果: False')
                    承受者.血量改变(-1)
                    print('\t敌方血量 -1')
                    if 承受者.是否死亡():
                        print('敌方死亡,游戏结束')
            else:
                承受者.血量改变(-1)
                print('\t敌方血量 -1')
                if 承受者.是否死亡():
                    print('敌方死亡,游戏结束')
        else:
            print('\t你没有这张牌')
    
    def 桃(self):
        '''定义玩家使用 桃 时的行为:  血量+1'''
        if '3.桃' in self.持有卡牌:
            if self.血量 < self.血量上限:
                self.血量 += 1
                self.弃牌('3.桃')
            else:
                print('\t你的血量已达上限')
        else:
            print('\t你没有这张牌')

    def 兵临城下(self, 承受者: Player):
        '''定义玩家使用 兵临城下 时的行为'''
        if '4.兵临城下' in self.持有卡牌:
            self.弃牌('4.兵临城下')
            if '1.杀' in 承受者.持有卡牌:
                承受者.弃牌('1.杀')
                print('\t敌方应对> 杀')
            elif '3.桃' in 承受者.持有卡牌:
                承受者.弃牌('3.桃')
                print('\t敌方应对> 桃')
            elif '15.运' in 承受者.持有卡牌:
                print('\t敌方应对> 运')
                if 承受者.判定():     # 如果判定返回 True
                    print('\t\t判定结果: True')
                else:
                    print('\t\t判定结果: False')
                    承受者.血量改变(-1)
                    print('\t敌方血量 -1')
                    if 承受者.是否死亡():
                        print('敌方死亡,游戏结束')
            else:
                承受者.血量改变(-1)
                print('\t敌方血量 -1')
                if 承受者.是否死亡():
                    print('敌方死亡,游戏结束')
        else:
            print('\t你没有这张牌')

    def 抽(self, 承受者: Player):
        '''定义玩家使用 抽 时的行为,随机抽取敌方一张卡牌'''
        if '5.抽' in self.持有卡牌:
            if len(承受者.持有卡牌):   #如果承受者卡牌数不等于0
                self.弃牌('5.抽')
                被抽取卡牌 = choice(承受者.持有卡牌)
                承受者.弃牌(被抽取卡牌)
                self.得牌(被抽取卡牌)
            else:
                print('敌方没有卡牌')
        else:
            print('你没有这张牌')

    def 粮(self):
        '''定义玩家使用 粮 时的行为,获得两张卡牌'''
        if '6.粮' in self.持有卡牌:
            self.弃牌('6.粮')
            for _ in range(2):
                self.摸牌()
        else:
            print('你没有这张牌')

    def 丰(self, 承受者: Player):
        '''定义玩家使用 丰 时的行为,两方均摸取一张牌'''
        if '7.丰' in self.持有卡牌:
            self.弃牌('7.丰')
            self.摸牌()
            承受者.摸牌()
        else:
            print('你没有这张牌')

    def 混战(self, 承受者: Player):
        '''定义玩家使用 混战 时的行为,两方均须出一张杀,否则扣一滴血'''
        if '8.混战' in self.持有卡牌:
            self.弃牌('8.混战')

            print('请出一张杀,桃,或运')
            while True:  #我方应对
                出牌 = input('我方应对> ')
                if 出牌 == 'h':   #获取帮助
                    print('1, 3, 15  --出杀, 闪, 桃')
                    print('m  --查看我方信息')
                    print('p  --输出敌方信息')
                    print('q  --放弃出牌')
                elif 出牌 == 'm':   #查看我方信息
                    self.输出玩家信息()
                elif 出牌 == 'p':   #查看敌方信息
                    承受者.输出玩家信息()
                elif 出牌 == '1':   #出杀
                    if '1.杀' in self.持有卡牌:
                        self.弃牌('1.杀')
                        break
                    else:
                        print('你没有这张牌')
                elif 出牌 == '3':   #出桃
                    if '3.桃' in self.持有卡牌:
                        self.弃牌('3.桃')
                        break
                    else:
                        print('你没有这张牌')
                elif 出牌 == '15':   #出运
                    if '15.运' in self.持有卡牌:
                        self.弃牌('15.运')
                        if self.判定():
                            print('判定结果为: True')
                            break
                        else:
                            print('判定结果为: False')
                    else:
                        print('你没有这张牌')
                elif 出牌 == 'q':   #放弃出牌,扣一滴血
                    self.血量改变(-1)
                    print('你的血量 -1')
                    if self.是否死亡():
                        print('你已死亡,游戏结束')
                    break
                else:
                    print('你可以输入 h 获取帮助')
            #敌方应对
            if '1.杀' in 承受者.持有卡牌:
                承受者.弃牌('1.杀')
                print('\t敌方应对> 杀')
            elif '3.桃' in 承受者.持有卡牌:
                承受者.弃牌('3.桃')
                print('\t敌方应对> 桃')
            elif '15.运' in 承受者.持有卡牌:
                print('\t敌方应对> 运')
                if 承受者.判定():     # 如果判定返回 True
                    print('\t\t判定结果: True')
                else:
                    print('\t\t判定结果: False')
                    承受者.血量改变(-1)
                    print('\t敌方血量 -1')
                    if 承受者.是否死亡():
                        print('敌方死亡,游戏结束')
            else:
                承受者.血量改变(-1)
                print('\t敌方血量 -1')
                if 承受者.是否死亡():
                    print('敌方死亡,游戏结束')
        else:
            print('\t你没有这张牌')

    def 水(self, 承受者: Player):
        '''定义玩家出 水 时敌方的行为: 等同于两张杀, 但可以被一张火或运防住'''
        if '9.水' in self.持有卡牌:   #当玩家手牌中有水时
            self.弃牌('9.水')

            if '10.火' in 承受者.持有卡牌:   #用火抵消
                    承受者.弃牌('10.火')
                    print('\t敌方应对> 火')
                    return   #使用return终止函数,防止继续运行后面代码
            if '15.运' in 承受者.持有卡牌: #
                    print('\t敌方应对> 运')
                    if 承受者.判定():     # 如果判定返回 True
                        print('\t\t判定结果: True')
                        return    #终止函数
                    else:
                        print('\t\t判定结果: False')
                        承受者.血量改变(-1)
                        print('\t敌方血量 -1')    
                        if 承受者.是否死亡():
                            print('敌方死亡,游戏结束')

            for _ in range(2):        #循环运行两遍
                if '2.闪' in 承受者.持有卡牌:
                    承受者.弃牌('2.闪')
                    print('\t敌方应对> 闪')
                elif '3.桃' in 承受者.持有卡牌:
                    承受者.弃牌('3.桃')
                    print('\t敌方应对> 桃')
                else:
                    承受者.血量改变(-1)
                    print('\t敌方血量 -1')
                    if 承受者.是否死亡():
                        print('敌方死亡,游戏结束')
        else:
            print('\t你没有这张牌')

    def 火(self, 承受者: Player):   #基本照搬 水 的代码
        '''定义玩家出 火 时敌方的行为: 等同于两张杀, 但可以被一张水或运防住'''
        if '10.火' in self.持有卡牌:   #当玩家手牌中有火时
            self.弃牌('10.火')

            if '9.水' in 承受者.持有卡牌:   #用火抵消
                    承受者.弃牌('9.水')
                    print('\t敌方应对> 水')
                    return   #使用return终止函数,防止继续运行后面代码
            if '15.运' in 承受者.持有卡牌: #
                    print('\t敌方应对> 运')
                    if 承受者.判定():     # 如果判定返回 True
                        print('\t\t判定结果: True')
                        return    #终止函数
                    else:
                        print('\t\t判定结果: False')
                        承受者.血量改变(-1)
                        print('\t敌方血量 -1')    
                        if 承受者.是否死亡():
                            print('敌方死亡,游戏结束')

            for _ in range(2):        #循环运行两遍
                if '2.闪' in 承受者.持有卡牌:
                    承受者.弃牌('2.闪')
                    print('\t敌方应对> 闪')
                elif '3.桃' in 承受者.持有卡牌:
                    承受者.弃牌('3.桃')
                    print('\t敌方应对> 桃')
                else:
                    承受者.血量改变(-1)
                    print('\t敌方血量 -1')
                    if 承受者.是否死亡():
                        print('敌方死亡,游戏结束')
        else:
            print('\t你没有这张牌')

    def 大动干戈(self, 承受者: Player):
        '''定义玩家出 大动干戈 时敌方的行为: 可使用其在一回合内打出多张杀'''
        if '11.大动干戈' in self.持有卡牌:   #当玩家手牌中有火时
            self.弃牌('11.大动干戈')

            while True:
                出牌 = input('请出牌> ')
                if 出牌 == 'h':
                    print('1  --杀')
                    print('h  --输出帮助信息')
                    print('m  --输出我方信息')
                    print('p  --输出敌方信息')
                    print('q  --退出')
                elif 出牌 == '1':
                    self.回合[self.回合数] = False   # 将本回合改为 True ,以免无法出杀
                    self.杀(承受者)
                elif 出牌 == 'm':
                    self.输出玩家信息()
                elif 出牌 == 'p':
                    承受者.输出玩家信息()
                elif 出牌 == 'q':
                    break
                else:
                    print('输入h以查看帮助信息')

        else:
            print('\t你没有这张牌')

    def 釜底抽薪(self, 承受者: Player):
        '''定义玩家出 釜底抽薪 时敌方的行为: 弃掉所有卡牌,否则扣一滴血'''
        if '12.釜底抽薪' in self.持有卡牌:   #当玩家手牌中有釜底抽薪时
            self.弃牌('12.釜底抽薪')

            if len(承受者.持有卡牌) == 0:    # 当敌方没有卡牌时
                承受者.血量改变(-1)
                print('\t敌方血量 -1')
                if 承受者.是否死亡():
                    print('敌方死亡,游戏结束')
            elif '桃' in 承受者.持有卡牌:    # 当敌方卡牌中有桃时
                承受者.弃牌('3.桃')
                print('\t敌方应对> 桃')
            elif len(承受者.持有卡牌) == 1:  # 当不满足上述情况且卡牌为1时
                承受者.持有卡牌 == []    # 清空敌方卡牌
                print('\t敌方弃掉 1 张卡牌')
            else :
                承受者.血量改变(-1)
                print('\t敌方血量 -1')
                if 承受者.是否死亡():
                    print('敌方死亡,游戏结束')
        else :
            print('\t你没有这张牌')

    def 雷电(self, 承受者: Player):
        '''定义玩家出 雷电 时的行为: 判定3次,如3次判定结果相等,扣除敌方4滴血'''
        if '13.雷电' in self.持有卡牌:   #当玩家手牌中有雷电时
            self.弃牌('13.雷电')

            检验数 : bool
            for x in range(1, 4):
                i = 承受者.判定()
                print(f'\t\t第{x}次: {i}')
                if x == 1:    # 第一次判定时确认 检验值
                    检验数 = i
                else :    # 第2, 3次判定时与检验值比对
                    if 检验数 != i:   #如果第2,3次结果与第1次不同
                        print('判定失败')
                        return    # 终止行为

            扣血数 = -4

            for _ in range(3):    # 循环3次,使敌方打出所拥有的最多3张桃
                if '3.桃' in 承受者.持有卡牌:
                    承受者.弃牌('3.桃')
                    print('\t敌方应对> 桃')
                    扣血数 += 1    # 少扣一滴血

            承受者.血量改变(扣血数)
            print(f'\t敌方血量 {扣血数}')
            if 承受者.是否死亡():
                print('敌方死亡,游戏结束')

        else :
            print('\t你没有这张牌')

    def 命(self, 承受者: Player):
        '''定义玩家出 命 时的行为: 无视闪桃运,在本回合扣敌方一滴血'''
        if '14.命' in self.持有卡牌:   #当玩家手牌中有雷电时
            self.弃牌('14.命')

            承受者.血量改变(-1)
            print('\t敌方血量 -1')
            if 承受者.是否死亡():
                print('敌方死亡,游戏结束')

        else :
            print('\t你没有这张牌')

    def 我方回合(self, 承受者: Player):###费弃,无法在敌方未实例化时使用攻击性卡牌
        '''整合我方行为,实现我方回合总控制台'''
        while True:
            i = input('我方回合> ')

            if i == 'h':
                print('\th  --查看帮助信息')
                print('\tm  --查看我方信息')
                print('\tp  --查看敌方信息')
                print('\t1 ~ 15  --出牌')
                print('\tq  --结束我方回合')
            elif i == 'm':
                self.输出玩家信息()
            elif i == 'p':
                承受者.输出玩家信息()
            elif i == '1':
                self.杀()
            elif i == '3':    # 闪, 运等 无法在我方回合使用
                self.桃()
#            elif



class 敌方(Player):
    '''定义敌方的行为和出牌'''
    def __init__(self):
        super().__init__()    # super()函数调用了父类的 __init__ 方法,使继承父类属性

    def 输出玩家信息(self):
        print('\t敌方状态: ')
        print(f'\t\t血量: {'# ' * self.血量}')
        print(f'\t\t卡牌数: {len(self.持有卡牌)}')

    def 杀(self, cs承受者: Player):
            '''我方出闪,桃,运, 否则扣一点血, 这里不设限制, 后面在不把其判定加入循环中'''
            self.弃牌('1.杀')
            print('敌方回合> 杀')
            while True:
                i = input('\t我方应对> ')
                if i == 'h':
                    print('\t\th  --输出帮助信息')
                    print('\t\tm  --输出我方信息')
                    print('\t\tp  --输出敌方信息')
                    print('\t\tq  --放弃应对')
                elif i == 'm':
                    cs承受者.输出玩家信息()    # 敌人视角中,我方为承受者,敌方为self
                elif i == 'p':
                    self.输出玩家信息()
                elif i == '2':    # 出闪
                    if '2.闪' in cs承受者.持有卡牌:
                        cs承受者.弃牌('2.闪')
                        break
                    else :
                        print('你没有这张牌')
                elif i == '3':    # 出桃
                    if '3.桃' in cs承受者.持有卡牌:
                        cs承受者.弃牌('3.桃')
                        break
                    else :
                        print('你没有这张牌')
                elif i == '15':    #出运
                    if '15.运' in cs承受者.持有卡牌:
                        cs承受者.弃牌('15.运')
                        if cs承受者.判定():
                            print('\t\t判定结果: True')
                            break
                        else:
                            print('判定结果: False')
                    else :
                        print('你没有这张牌')
                elif i == 'q':    # 放弃
                    cs承受者.血量改变(-1)
                    print('\t我方血量 -1')
                    if cs承受者.是否死亡():
                        print('你已死亡,游戏结束')
                    break
                else :
                    print('输入 h 以查看帮助')

    def 桃(self):
        '''定义玩家使用 桃 时的行为:  血量+1, 调用前记得 if 血量不等于上限'''
        self.弃牌('3.桃')
        print('敌方回合> 桃')
        self.血量 += 1
        print('敌方血量 +1')

    def 兵临城下(self, cs承受者: Player):
        '''定义敌方出 兵临城下 时我方的面板: 出杀, 否则扣一点血'''
        self.弃牌('4.兵临城下')
        print('敌方回合> 兵临城下')
        while True:
            i = input('\t我方应对> ')
            if i == 'h':
                print('\t\th  --输出帮助信息')
                print('\t\tm  --输出我方信息')
                print('\t\tp  --输出敌方信息')
                print('\t\tq  --放弃应对')
            elif i == 'm':
                cs承受者.输出玩家信息()
            elif i == 'p':
                self.输出玩家信息()
            elif i == '1':    # 出杀
                if '1.杀' in cs承受者.持有卡牌:
                    cs承受者.弃牌('1.杀')
                    break
                else :
                    print('你没有这张牌')
            elif i == '3':    # 出桃
                if '3.桃' in cs承受者.持有卡牌:
                    cs承受者.弃牌('3.桃')
                    break
                else :
                    print('你没有这张牌')
            elif i == '15':    #出运
                if '15.运' in cs承受者.持有卡牌:
                    cs承受者.弃牌('15.运')
                    if cs承受者.判定():
                        print('\t\t判定结果: True')
                        break
                    else:
                        print('判定结果: False')
                else :
                        print('你没有这张牌')
            elif i == 'q':    # 放弃
                cs承受者.血量改变(-1)
                print('\t我方血量 -1')
                if cs承受者.是否死亡():
                    print('你已死亡,游戏结束')
                break
            else :
                    print('输入 h 以查看帮助')

    def 抽(self, cs承受者: Player):
        '''抽取我方一张牌'''
        self.弃牌('5.抽')
        if len(cs承受者.持有卡牌) > 0:
            self.弃牌('5.抽')
            print('敌方回合> 抽')
            i = choice(cs承受者.持有卡牌)
            cs承受者.弃牌(i)
            self.持有卡牌.append(i)
        else:
            pass

    def 粮(self):
        '''摸两张牌'''
        self.弃牌('6.粮')
        print('敌方回合> 粮')
        self.摸牌()
        self.摸牌()

    def 丰(self, cs承受者: Player):
        '''每人摸一张牌'''
        self.弃牌('7.丰')
        print('敌方回合> 丰')
        self.摸牌()
        cs承受者.摸牌()

    def 混战(self, cs承受者: Player):
        '''每人出一张杀,否则扣一滴血'''
        self.弃牌('8.混战')
        print('敌方回合> 混战')
        self.弃牌('1.杀')
        print('\t敌方应对> 杀')

        while True:
            i = input('\t我方应对> ')
            if i == 'h':
                print('\t\th  --输出帮助信息')
                print('\t\tm  --输出我方信息')
                print('\t\tp  --输出敌方信息')
                print('\t\tq  --放弃应对')
            elif i == 'm':
                cs承受者.输出玩家信息()
            elif i == 'p':
                self.输出玩家信息()
            elif i == '1':    # 出杀
                if '1.杀' in cs承受者.持有卡牌:
                    cs承受者.弃牌('1.杀')
                    break
                else :
                    print('你没有这张牌')
            elif i == '3':    # 出桃
                if '3.桃' in cs承受者.持有卡牌:
                    cs承受者.弃牌('3.桃')
                    break
                else :
                    print('你没有这张牌')
            elif i == '15':    #出运
                if '15.运' in cs承受者.持有卡牌:
                    cs承受者.弃牌('15.运')
                    if cs承受者.判定():
                        print('\t\t判定结果: True')
                        break
                    else:
                        print('判定结果: False')
                else :
                        print('你没有这张牌')
            elif i == 'q':    # 放弃
                cs承受者.血量改变(-1)
                print('\t我方血量 -1')
                if cs承受者.是否死亡():
                    print('你已死亡,游戏结束')
                break
            else :
                    print('输入 h 以查看帮助')
    
    def 水(self, cs承受者: Player):
        '''出1张火,运或两张闪,桃'''
        self.弃牌('9.水')
        print('敌方回合> 水')

        while True:
            i = input('\t我方应对> ')
            if i == 'h':
                print('\t\th  --输出帮助信息')
                print('\t\tm  --输出我方信息')
                print('\t\tp  --输出敌方信息')
                print('\t\tq  --放弃应对')
            elif i == 'm':
                cs承受者.输出玩家信息()
            elif i == 'p':
                self.输出玩家信息()
            elif i == '2':    # 出闪
                if '2.闪' in cs承受者.持有卡牌:
                    cs承受者.弃牌('2.闪')
                    while True:
                        a = input('\t请再出一张闪')
                        if a == '2':
                            if '2.闪' in cs承受者.持有卡牌:
                                cs承受者.弃牌('2.闪')
                                return
                            else:
                                print('你没有这张牌')
                        elif a == 'q':
                            cs承受者.持有卡牌.append('2.闪')
                            break
                        elif a == 'h':
                            print('请再出一张闪,输入 q 退出')
                else :
                    print('你没有这张牌')
            elif i == '3':    # 出桃
                if '3.桃' in cs承受者.持有卡牌:
                    cs承受者.弃牌('3.桃')
                    while True:
                        x = input('是否再出一张桃以完全减免伤害(y/n): ')
                        if x == 'y':
                            if '3.桃' in cs承受者.持有卡牌:
                                cs承受者.弃牌('3.桃')
                                return
                            else:
                                print('你没有这张牌')
                        if x == 'n':
                            cs承受者.血量改变(-1)
                            print('\t我方血量 -1')
                            if cs承受者.是否死亡():
                                print('你已死亡,游戏结束')
                            return
                        else:
                            pass
                else :
                    print('你没有这张牌')
            elif i == '10':
                if '10.火' in cs承受者.持有卡牌:
                    cs承受者.弃牌('10.火')
                    break
                else:
                    print('你没有这张牌')
            elif i == '15':    #出运
                if '15.运' in cs承受者.持有卡牌:
                    cs承受者.弃牌('15.运')
                    if cs承受者.判定():
                        print('\t\t判定结果: True')
                        break
                    else:
                        print('判定结果: False')
                else :
                        print('你没有这张牌')
            elif i == 'q':    # 放弃
                cs承受者.血量改变(-2)
                print('\t我方血量 -2')
                if cs承受者.是否死亡():
                    print('你已死亡,游戏结束')
                break
            else :
                    print('输入 h 以查看帮助')

    def 火(self, cs承受者: Player):
        '''出1张水,运或两张闪,桃'''
        self.弃牌('10.火')
        print('敌方回合> 火')

        while True:
            i = input('\t我方应对> ')
            if i == 'h':
                print('\t\th  --输出帮助信息')
                print('\t\tm  --输出我方信息')
                print('\t\tp  --输出敌方信息')
                print('\t\tq  --放弃应对')
            elif i == 'm':
                cs承受者.输出玩家信息()
            elif i == 'p':
                self.输出玩家信息()
            elif i == '2':    # 出闪
                if '2.闪' in cs承受者.持有卡牌:
                    cs承受者.弃牌('2.闪')
                    while True:
                        a = input('\t请再出一张闪')
                        if a == '2':
                            if '2.闪' in cs承受者.持有卡牌:
                                cs承受者.弃牌('2.闪')
                                return
                            else:
                                print('你没有这张牌')
                        elif a == 'q':
                            cs承受者.持有卡牌.append('2.闪')
                            break
                        elif a == 'h':
                            print('请再出一张闪,输入 q 退出')
                else :
                    print('你没有这张牌')
            elif i == '3':    # 出桃
                if '3.桃' in cs承受者.持有卡牌:
                    cs承受者.弃牌('3.桃')
                    while True:
                        x = input('是否再出一张桃以完全减免伤害(y/n): ')
                        if x == 'y':
                            if '3.桃' in cs承受者.持有卡牌:
                                cs承受者.弃牌('3.桃')
                                return
                            else:
                                print('你没有这张牌')
                        if x == 'n':
                            cs承受者.血量改变(-1)
                            print('\t我方血量 -1')
                            if cs承受者.是否死亡():
                                print('你已死亡,游戏结束')
                            return
                        else:
                            pass
                else :
                    print('你没有这张牌')
            elif i == '9':
                if '9.水' in cs承受者.持有卡牌:
                    cs承受者.弃牌('9.水')
                    break
                else:
                    print('你没有这张牌')
            elif i == '15':    #出运
                if '15.运' in cs承受者.持有卡牌:
                    cs承受者.弃牌('15.运')
                    if cs承受者.判定():
                        print('\t\t判定结果: True')
                        break
                    else:
                        print('判定结果: False')
                else :
                        print('你没有这张牌')
            elif i == 'q':    # 放弃
                cs承受者.血量改变(-2)
                print('\t我方血量 -2')
                if cs承受者.是否死亡():
                    print('你已死亡,游戏结束')
                break
            else :
                    print('输入 h 以查看帮助')

    def 大动干戈(self, cs承受者: Player):
        '''打出手中所有的杀'''
        if '1.杀' in self.持有卡牌:
            self.弃牌('11.大动干戈')
            print('敌方回合> 大动干戈')
            while '1.杀' in self.持有卡牌:
                self.弃牌('1.杀')
                print('\t敌方回合> 杀')

                while True:    # 直接复制了杀的代码
                    i = input('\t我方应对> ')
                    if i == 'h':
                        print('\t\th  --输出帮助信息')
                        print('\t\tm  --输出我方信息')
                        print('\t\tp  --输出敌方信息')
                        print('\t\tq  --放弃应对')
                    elif i == 'm':
                        cs承受者.输出玩家信息()    # 敌人视角中,我方为承受者,敌方为self
                    elif i == 'p':
                        self.输出玩家信息()
                    elif i == '2':    # 出闪
                        if '2.闪' in cs承受者.持有卡牌:
                            cs承受者.弃牌('2.闪')
                            break
                        else :
                            print('你没有这张牌')
                    elif i == '3':    # 出桃
                        if '3.桃' in cs承受者.持有卡牌:
                            cs承受者.弃牌('3.桃')
                            break
                        else :
                            print('你没有这张牌')
                    elif i == '15':    #出运
                        if '15.运' in cs承受者.持有卡牌:
                            cs承受者.弃牌('15.运')
                            if cs承受者.判定():
                                print('\t\t判定结果: True')
                                break
                            else:
                                print('判定结果: False')
                        else :
                            print('你没有这张牌')
                    elif i == 'q':    # 放弃
                        cs承受者.血量改变(-1)
                        print('\t我方血量 -1')
                        if cs承受者.是否死亡():
                            print('你已死亡,游戏结束')
                        break
                    else :
                        print('输入 h 以查看帮助')

    def 釜底抽薪(self, cs承受者: Player):
        '''弃掉所有手牌,否则扣一滴血'''
        self.弃牌('12.釜底抽薪')
        print('敌方回合> 釜底抽薪')

        while True:
            i = input('\t我方应对> ')
            if i == 'h':
                print('\t\th  --输出帮助信息')
                print('\t\tm  --输出我方信息')
                print('\t\tp  --输出敌方信息')
                print('\t\tx  --弃掉所有卡牌')
                print('\t\tq  --放弃应对')
            elif i == 'm':
                cs承受者.输出玩家信息()
            elif i == 'p':
                self.输出玩家信息()
            elif i == 'x':
                if cs承受者.持有卡牌:#卡牌数不为0
                    cs承受者.持有卡牌 = []
                    return
                else:
                    print('你没有卡牌,无法弃牌')
            elif i == '3':    # 出桃
                if '3.桃' in cs承受者.持有卡牌:
                    cs承受者.弃牌('3.桃')
                    break
                else :
                    print('你没有这张牌')
            elif i == '15':    #出运
                if '15.运' in cs承受者.持有卡牌:
                    cs承受者.弃牌('15.运')
                    if cs承受者.判定():
                        print('\t\t判定结果: True')
                        break
                    else:
                        print('判定结果: False')
                else :
                        print('你没有这张牌')
            elif i == 'q':    # 放弃
                cs承受者.血量改变(-1)
                print('\t我方血量 -1')
                if cs承受者.是否死亡():
                    print('你已死亡,游戏结束')
                break
            else :
                    print('输入 h 以查看帮助')

    def 雷电(self, cs承受者: Player):
        '''判定3次,结果相同则受4点伤害'''
        self.弃牌('13.雷电')
        print('敌方回合> 雷电')

        检验数 : bool
        for x in range(1, 4):
            i = cs承受者.判定()
            print(f'\t\t第{x}次: {i}')
            if x == 1:    # 第一次判定时确认 检验值
                检验数 = i
            else :    # 第2, 3次判定时与检验值比对
                if 检验数 != i:   #如果第2,3次结果与第1次不同
                    print('\t\t判定失败')
                    return    # 终止行为

        扣血数 = -4

        while True:
            i = input(f'\t我方应对<扣血: {扣血数}>> ')
            if i == 'h':
                print('\t\th  --输出帮助信息')
                print('\t\tm  --输出我方信息')
                print('\t\tp  --输出敌方信息')
                print('\t\tq  --放弃应对')
            elif i == 'm':
                cs承受者.输出玩家信息()
            elif i == 'p':
                self.输出玩家信息()
            elif i == '3':    # 出桃
                if '3.桃' in cs承受者.持有卡牌:
                    cs承受者.弃牌('3.桃')
                    扣血数 += 1    # 减免一点伤害
                else :
                    print('你没有这张牌')
            elif i == '15':    #出运
                if '15.运' in cs承受者.持有卡牌:
                    cs承受者.弃牌('15.运')
                    if cs承受者.判定():
                        print('\t\t判定结果: True')
                        break
                    else:
                        print('判定结果: False')
                else :
                        print('你没有这张牌')
            elif i == 'q':    # 放弃
                cs承受者.血量改变(扣血数)
                print(f'\t我方血量 {扣血数}')
                if cs承受者.是否死亡():
                    print('你已死亡,游戏结束')
                break
            else :
                    print('输入 h 以查看帮助')

    def 命(self, cs承受者: Player):
        '''对方受一点伤害'''
        self.弃牌('14.命')
        print('敌方回合> 命')
        cs承受者.血量改变(-1)
        print('\t我方血量 -1')
        if cs承受者.是否死亡():
            print('你已死亡,游戏结束')



w我方Player = 我方()
d敌方Player = 敌方()

def 输出卡牌帮助():
    print('每到自己回合自动摸取2张牌')
    print('杀        --使对方扣一点血,每回合限出一次')
    print('闪        --防住杀')
    print('桃        --回一点血,亦可用于阻挡一点伤害')
    print('兵临城下  --出一张杀,否则受一点伤害')
    print('抽        --抽取对方一张牌')
    print('粮        --额外摸取2张牌')
    print('丰        --每人各摸取一张牌')
    print('混战      --每人均需出一张杀,否则受一点伤害')
    print('水        --造成2点伤害,可被火或2张闪抵挡')
    print('火        --造成2点伤害,可被水或2张闪抵挡')
    print('大动干戈  --帮助你在同一回合多次出杀')
    print('釜底抽薪  --对方需弃掉所有卡牌,否则受到一点伤害')
    print('雷电      --连续进行3次判定,判定结果相等则对方受到4点伤害')
    print('命        --使对方收到一点无法阻挡的伤害')
    print('运        --进行一次判定,结果为 True 则免去此次伤害')

def 我方回合():
    w我方Player.此回合摸牌()
    while True:
        i = input('我方回合> ')

        if i == 'h':
            print('\th  --查看帮助信息')
            print('\thp  --查看卡牌作用')
            print('\tm  --查看我方信息')
            print('\tp  --查看敌方信息')
            print('\t1 ~ 15  --出牌')
            print('\tx  --弃牌')
            print('\tq  --结束我方回合')
        elif i == 'hp':
            输出卡牌帮助()
        elif i == 'm':
            w我方Player.输出玩家信息()
        elif i == 'p':
            d敌方Player.输出玩家信息()
        elif i == 'x':
            while True:
                a = input('弃牌<q 停止>> ')
                if a == 'q':
                    break
                if a not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', ]:
                    print('无效字符')
                    continue
                if card_d[a] in w我方Player.持有卡牌:
                    w我方Player.弃牌(card_d[a])
                else:
                    print('你没有这张牌')
        elif i == '1':
            w我方Player.杀(d敌方Player)
        elif i == '3':    # 闪, 运等 无法在我方回合使用
            w我方Player.桃()
        elif i == '4':
            w我方Player.兵临城下(d敌方Player)
        elif i == '5':
            w我方Player.抽(d敌方Player)
        elif i == '6':
            w我方Player.粮()
        elif i == '7':
            w我方Player.丰(d敌方Player)
        elif i == '8':
            w我方Player.混战(d敌方Player)
        elif i == '9':
            w我方Player.水(d敌方Player)
        elif i == '10':
            w我方Player.火(d敌方Player)
        elif i == '11':
            w我方Player.大动干戈(d敌方Player)
        elif i == '12':
            w我方Player.釜底抽薪(d敌方Player)
        elif i == '13':
            w我方Player.雷电(d敌方Player)
        elif i == '14':
            w我方Player.命(d敌方Player)
        elif i == 'q':
            print('结束我方回合')
            w我方Player.回合数 += 1
            break
        else:
            print('输入 h 以查看帮助')

def 敌方回合():
        ''''''
        d敌方Player.此回合摸牌()
        if '1.杀' in d敌方Player.持有卡牌:
            d敌方Player.杀(w我方Player)    # 杀的判断在循环外面
        
        for _ in range(2):
            if '3.桃' in d敌方Player.持有卡牌:
                if d敌方Player.血量 < d敌方Player.血量上限:
                    d敌方Player.桃()
            if '4.兵临城下' in d敌方Player.持有卡牌:
                d敌方Player.兵临城下(w我方Player)
            if '5.抽' in d敌方Player.持有卡牌:
                d敌方Player.抽(w我方Player)
            if '6.粮' in d敌方Player.持有卡牌:
                d敌方Player.粮()
            if '7.丰' in d敌方Player.持有卡牌:
                d敌方Player.丰(w我方Player)
            if '8.混战' in d敌方Player.持有卡牌:
                d敌方Player.混战(w我方Player)
            if '9.水' in d敌方Player.持有卡牌:
                d敌方Player.水(w我方Player)
            if '10.火' in d敌方Player.持有卡牌:
                d敌方Player.火(w我方Player)
            if '11.大动干戈' in d敌方Player.持有卡牌:
                d敌方Player.大动干戈(w我方Player)
            if '12.釜底抽薪' in d敌方Player.持有卡牌:
                d敌方Player.釜底抽薪(w我方Player)
            if '13.雷电' in d敌方Player.持有卡牌:
                d敌方Player.雷电(w我方Player)
            if '14.命' in d敌方Player.持有卡牌:
                d敌方Player.命(w我方Player)
        print('结束敌方回合')



def 游戏开始():
    w我方Player.此回合摸牌()
    d敌方Player.此回合摸牌()
    while True:
        我方回合()
        敌方回合()

if __name__ == '__main__':
    游戏开始()