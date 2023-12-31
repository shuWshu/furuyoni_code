import commonProcess as cp
import board as bd
import cardList as cl

# これ何???
# 多分テストコード
class CardFunc:
    def __init__(self, func):
        self.function = func
    def func(self, usePlayer, usedPlayer, areas):
        self.function(usePlayer, usedPlayer, areas)

# カード処理の羅列
# 引数: 使用者, 被使用者, ボード情報, (対応のみ)対応使用か否か
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
def Moguri(usePlayer, usedPlayer, areas, attackData=None):
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
def KuNoGaito(usePlayer, usedPlayer, areas, attackData=None):
    # 対応した《攻撃》は-2/+0となる。
    if attackData is not None:
        cp.damageCorrection(attackData.damage, [-2, 0])
    # 相オーラ →2→ ダスト
    bd.moveAreaValPoss(usedPlayer.aura, areas.dust, 2)
    return 1

# 桜寄せ
def Sakurayose(usePlayer, usedPlayer, areas, attackData=None):
    # 相オーラ →1→ 自オーラ
    bd.moveAreaValPoss(usedPlayer.aura, usePlayer.aura, 1)
    return 1

# 光輝収束
def Koukishusoku(usePlayer, usedPlayer, areas):
    # ダスト →2→ 自オーラ
    bd.moveAreaValPoss(areas.dust, usePlayer.aura, 2)
    # ダスト →1→ 自フレア
    bd.moveAreaValPoss(areas.dust, usePlayer.flare, 1)
    return 1

# 桜吹雪の景色
def SakurahubukiNoKeshiki(usePlayer, usedPlayer, areas):
    # 相オーラ →2→ 間合
    bd.moveAreaValPoss(usedPlayer.aura, areas.distance, 2)
    return 1

# 精霊たちの風
def SeireitatiNoKaze(usePlayer, usedPlayer, areas, attackData=None):
    if attackData is not None:
        # 対応した切札でない《攻撃》を打ち消す。
        if attackData.Class != 1:
            attackData.canceled = True
    # カードを1枚引く。
    cp.draw(usePlayer)
    return 1

# 引数にカード情報を得て処理を登録する場合
# 攻撃に関わるものが主
# 攻撃汎用
def MakeAttack(card):
    def Attack(usePlayer, usedPlayer, areas):
        return cp.attack(usePlayer, usedPlayer, areas, card.dist, card.Damage, card.Class, card.subType, card.megami)
    return Attack

# 対応不可攻撃汎用
def MakeNoReaction(card):
    def NoReaction(usePlayer, usedPlayer, areas):
        return cp.attack(usePlayer, usedPlayer, areas, card.dist, card.Damage, card.Class, card.subType, card.megami, noReaction=True)
    return NoReaction

# 返し斬り
def MakeKaeshigiri(card):
    def Kaeshigiri(usePlayer, usedPlayer, areas, attackData=None):
        result = cp.attack(usePlayer, usedPlayer, areas, card.dist, card.Damage, card.Class, card.subType, card.megami)
        if result == 1:
            #【攻撃後】このカードを対応で使用したならば ダスト →1→ 自オーラ
            if attackData is not None:
                bd.moveAreaValPoss(areas.dust, usePlayer.aura, 1)
        return result
    return Kaeshigiri
                

