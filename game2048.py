from random import choice



class Game2048:

    def __init__(self) -> None:
        self.data = [
            [0, 0, 0, 0],  # x0
            [0, 0, 0, 0],  # x1
            [0, 0, 0, 0],  # x2
            [0, 0, 0, 0],  # x3
            #y0 y1 y2 y3
        ]

    def null_data_addrs(self) -> tuple[str]:
        '''返回一个包含self.data中0值坐标的元组，坐标以字符串表示，如'12' 
        表示self.data[1][2]'''
        addrs = []
        for x in range(4):
            for y in range(4):
                if self.data[x][y] == 0:
                    addrs.append(f'{x}{y}')
        return tuple(addrs)
    
    def add_2_and_check(self) -> None|str:
        '''随机选择一个数值为0的地址，修改其值为2，返回None 。同时检查游戏是否结束，
        当存在值2048时，返回字符串'Win' ,游戏失败，返回'Loss' '''
        for l in self.data:
            for v in l:
                if v >= 2048:
                    return 'Win'
        
        try :
            x, y = list(choice(self.null_data_addrs()))
        except :
            # 如果上式错误，表明玩家此次移动后没有地方为0，玩家失败
            return 'Loss'
        else :
            self.data[int(x)][int(y)] = 2
    

    def up_logic(self) -> None:
        '''向上移动的逻辑'''
        for _ in range(3):    # 重复操作三次
            for x in range(1, 4):  # 不必处理第x0行，以免需要处理错误
                for y in range(4):
                    if self.data[x][y] == self.data[x-1][y]:  # 此数据与上面数据相等，此数据为0，上面数据加此数据
                        self.data[x][y], self.data[x-1][y] = 0, self.data[x][y]+self.data[x-1][y]
                    if self.data[x][y]!=0 and self.data[x-1][y]==0: # 此数据不为0且上面数据为0，替换
                        self.data[x][y], self.data[x-1][y] = self.data[x-1][y], self.data[x][y]

    def down_logic(self) -> None:
        '''向下移动的逻辑'''
        for _ in range(3):    # 重复操作三次
            for x in range(2, -1, -1):  # [2, 1, 0], 不处理x4
                for y in range(4):
                    if self.data[x][y] == self.data[x+1][y]:  # 此数据与下面数据相等，此数据为0，下面数据加此数据
                        self.data[x][y], self.data[x+1][y] = 0, self.data[x][y]+self.data[x+1][y]
                    if self.data[x][y]!=0 and self.data[x+1][y]==0: # 此数据不为0且下面数据为0，替换
                        self.data[x][y], self.data[x+1][y] = self.data[x+1][y], self.data[x][y]

    def left_logic(self) -> None:
        '''向左移动的逻辑'''
        for _ in range(3):    # 重复操作三次
            for x in range(4):
                for y in range(1, 4):  # 不必处理y0列，以免需要处理错误
                    if self.data[x][y] == self.data[x][y-1]:  # 此数据与左边数据相等，此数据为0，左边数据加此数据
                        self.data[x][y], self.data[x][y-1] = 0, self.data[x][y]+self.data[x][y-1]
                    if self.data[x][y]!=0 and self.data[x][y-1]==0: # 此数据不为0且左边数据为0，替换
                        self.data[x][y], self.data[x][y-1] = self.data[x][y-1], self.data[x][y]

    def right_logic(self) -> None:
        '''向右移动的逻辑'''
        for _ in range(3):    # 重复操作三次
            for x in range(4):
                for y in range(2, -1, -1):  # [2, 1, 0]不必处理y3列，以免需要处理错误
                    if self.data[x][y] == self.data[x][y+1]:  # 此数据与右边数据相等，此数据为0，右边数据加此数据
                        self.data[x][y], self.data[x][y+1] = 0, self.data[x][y]+self.data[x][y+1]
                    if self.data[x][y]!=0 and self.data[x][y+1]==0: # 此数据不为0且右边数据为0，替换
                        self.data[x][y], self.data[x][y+1] = self.data[x][y+1], self.data[x][y]

    def command_line_display(self) -> None:
        '''在命令行格式化输出self.data'''
        print()  # 与上一个输出相隔
        sign = 0    # 标志第几次输出 '----+----+----'
        for l in self.data:
            print(f'\t{l[0]:^4}|{l[1]:^4}|{l[2]:^4}|{l[3]:^4}')
            sign += 1
            print( '\t----+----+----+----') if sign <= 3 else print()
        print('Input "wasd" to move.')
        print('w: up\ts: dowm\na: left\td: right')



game = Game2048()
def main(game = game) -> None:
    while True:
        game.command_line_display()
        match input('move> '):
            case 'W'|'w':  game.up_logic()
            case 'A'|'a':  game.left_logic()
            case 'S'|'s':  game.down_logic()
            case 'D'|'d':  game.right_logic()
            case 'backdoor': print(eval(input()))  # 用于调试，免得测试时要完整打一关，可以使用exec控制data
            case _ :       
                print('!!!Error input!!! Please cleck you input and try again.')
                input('Enter to Continue...')
                continue
        match game.add_2_and_check():
            case 'Win' : print('\nYou Win!'); input('Enter Quit'); break
            case 'Loss': print('\nYou Loss'); input('Enter Quit'); break

if __name__ == '__main__':
    main()