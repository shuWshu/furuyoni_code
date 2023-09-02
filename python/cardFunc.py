import commonProcess as cp
import board as bd

# これ何???
# 多分テストコード
class CardFunc:
    def __init__(self, func):
        self.function = func
    def func(self, usePlayer, usedPlayer, areas):
        self.function(usePlayer, usedPlayer, areas)

# カード処理の羅列
# 引数: 使用者, 被使用者, ボード情報
# 返値: 成功;1 何らかの理由で不成立:-1
# 歩法
def Hohou(usePlayer, usedPlayer, areas):
    usePlayer.chgVigor(1) # 集中力を1得る。
    # 間合 ←1→ ダスト
    tokens = cp.checkToken("choose 0:間合→ダスト 1:ダスト→間合\n", ["choose"], [[0, 1]])
    if tokens[1] == 0:
        bd.moveAreaValPoss(areas.distance, areas.dust, 1)
    else:
        bd.moveAreaValPoss(areas.dust, areas.distance, 1)
    return 1

# 潜り
def Moguri(usePlayer, usedPlayer, areas):
    # 間合 →1→ ダスト
    bd.moveAreaValPoss(areas.distance, areas.dust, 1)
    return 1

# 闇凪の声
def YaminagiNoKoe(usePlayer, usedPlayer, areas):
    # カードを2枚引く。
    for i in range(2):
        cp.draw(usePlayer)
    return 1

# 苦の外套
def KuNoGaito():
    # TODO:対応による減算処理どうしよう
    return 1