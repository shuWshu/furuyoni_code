import board as bd

# ----- 共通処理 -----
"""
# 元のダメージ関数
# 引数: プレイヤー, ダスト領域, 領域(文字列), 値
def damage(player, area, n, areas):
    if(area == "life"):
        ret = bd.moveAreaValPoss(player.life, player.flare, n)
        if(player.life.val <= 0):
            return lose(player)
        return ret
    elif(area == "aura"):
        return bd.moveAreaVal(player.aura, areas.dust, n)
    elif(area == "flare"):
        return bd.moveAreaVal(player.flare, areas.dust, n)
    return -1
"""

# ダメージ処理関数用クラス
# 使用前にsetConfigを使うこと!!
# 
class Damage:
    def __init__(self):
        self.dust = None
        self.loseFunc = None
    # 引数: ダスト領域, 負け時の処理
    def setConfig(self, dust, loseFunc):
        self.dust = dust
        self.loseFunc = loseFunc

    # ライフダメージ
    def life(self, player, n):
        if not self.dust:
            print("need setConfig")
            return -1
        ret = bd.moveAreaValPoss(player.life, player.flare, n)
        if(player.life.val <= 0):
            return self.loseFunc(player)
        return ret
     # オーラダメージ
    def aura(self, player, n):
        if not self.dust:
            print("need setConfig")
            return -1
        return bd.moveAreaVal(player.aura, self.dust, n)

# インポート関数定義
damage = Damage()

# 焦燥
def impatience(player):
    tokens = checkToken("[焦燥] どちらでダメージを受けますか?\nimpatience 0:オーラ 1:ライフ\n", ["impatience"], [[0, 1]])
    if tokens[1] == 0:
        damage.aura(player, 1)
    else:
        damage.life(player, 1)

# トークン照合 トークンが違うならループする
# 引数: 表示メッセージ, 正解命令リスト, 引数リストのリスト
# 返値: トークン(str), 引数(int 無しなら-1)
def checkToken(message, orderList, argListList):
    while(1):
        Input = input(message)
        token = Input.split()
        order = token[0]
        if order in orderList:
            index = orderList.index(order)
            if not argListList[index]: # 引数無しで良い場合
                return order, -1
            if len(token) != 2:
                print("\x1b[31mError:引数の数が正しくありません\x1b[0m")
            else:
                try: 
                    if int(token[1]) in argListList[index]:
                        return order, int(token[1])
                    else:
                        print("\x1b[31mError:引数の値が正しくありません\x1b[0m")
                except ValueError:
                    print("\x1b[31mError:引数が整数ではありません\x1b[0m")
        else:
            print("\x1b[31mError:命令が存在しません\x1b[0m")