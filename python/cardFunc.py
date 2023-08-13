import commonProcess as cp
import board as bd

class CardFunc:
    def __init__(self, func):
        self.function = func
    def func(self, usePlayer, usedPlayer, areas):
        self.function(usePlayer, usedPlayer, areas)

# カード処理の羅列
# 歩法
def Hohou(usePlayer, usedPlayer, areas):
    usePlayer.chgVigor(1) # 集中力を1得る。
    tokens = cp.checkToken("choose 0:間合→ダスト 1:ダスト→間合\n", ["choose"], [[0, 1]]) # 間合 ←1→ ダスト
    if tokens[1] == 0:
        bd.moveAreaValPoss(areas.distance, areas.dust, 1)
    else:
        bd.moveAreaValPoss(areas.dust, areas.distance, 1)
        