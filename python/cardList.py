import commonProcess as cp
import cardFunc

# クラス定義
class Card:
    # parameterはカードタイプによって変化
    # 攻撃:[[間合], [オーラダメージ, ライフダメージ]]
    # 行動:[]
    # 付与:[納]
    def __init__(self, Class, name, num, megami, megamiNo, version, mainType, subType, text, parameter, cost = 0, func=None) -> None:
        self.Class = Class # 通常:0, 切札:1
        self.name = name # カード名 string
        self.num = num # カードナンバー int
        self.megami = megami # 使用メガミ string
        self.megamiNo = megamiNo #女神ナンバー int
        self.version = version # メガミバージョン string
        self.mainType = mainType # メインタイプ 攻撃:0, 行動:1, 付与:2
        self.subType = subType # サブタイプ 無し:0, 対応:1, 全力:2
        self.text = text # テキスト string
        if(self.mainType == 0): # 攻撃札のみ
            self.dist = parameter[0] # 適正距離 int[]
            self.Damage = parameter[1] # ダメージ [オーラ, ライフ] [int, int] null可能 "-"は-1で表現 "X"は-2で表現
        if(self.mainType == 2): # 付与札のみ
            self.pay = parameter[0] # 納 int null可能
        if(self.Class == 1):
            self.cost = cost # フレアコスト int null可能

        # カードナンバーの文字列
        self.cardNo = f"NA_{str(self.megamiNo).zfill(2)}_{self.megami}_{self.version.upper()}_"
        if(self.Class == 0):
            self.cardNo += f"N_{self.num}"
        elif(self.Class == 1):
            self.cardNo += f"S_{self.num}"

        # カードの処理
        self.function = func
        if self.function is None and self.mainType == 0:
            def commonAttack(usePlayer, usedPlayer, areas):
                return cp.attack(usePlayer, usedPlayer, areas, self.dist, self.Damage)
            self.function = commonAttack
        
    def use(self, usePlayer, usedPlayer, areas):
        print(self.name + " を使用")
        return self.function(usePlayer, usedPlayer, areas)


# n字インデントを下げる関数
def indentText(text, num_spaces):
    spaces = " " * num_spaces
    return "\n".join(spaces + line for line in text.splitlines())

# テキスト用インデント下げ
def indentTextPipe(text, num_before, num_after):
    spaces_before = " " * num_before
    spaces_after = " " * num_after
    indented_text = "\n".join(spaces_before + "|"+ spaces_after + line for line in text.splitlines())
    return indented_text
  
# アウトプット
def outputCard(card, mono = False):
    cardType = ""
    paraData = ""
    if(card.Class == 0):
        cardType = "\n 通常札"
    elif(card.Class == 1):
        cardType = "\n 切札"

    if(card.mainType == 0):
        if(mono):
            cardType += " 攻撃"
        else:
            cardType += " \x1b[31m攻撃\x1b[0m"
        distMax = max(card.dist)
        distMin = min(card.dist)
        dist = ""
        if distMax == distMin:
            dist = str(distMax)
        else:
            dist = str(distMin) + "-" + str(distMax)
        auraDamage = str(card.Damage[0])
        lifeDamage = str(card.Damage[1])
        if auraDamage == "-1":
            auraDamage = "-"
        elif auraDamage == "-2":
            auraDamage = "X" 
        if lifeDamage == "-1":
            lifeDamage = "-"
        elif lifeDamage == "-2":
            lifeDamage = "X"
        paraData = f" 適正距離:{dist} ダメージ:{auraDamage}/{lifeDamage}"
    elif(card.mainType == 1):
        if(mono):
            cardType += " 行動"
        else:
            cardType += " \x1b[34m行動\x1b[0m"
    elif(card.mainType == 2):
        if(mono):
            cardType += " 付与"
        else:
            cardType += " \x1b[32m付与\x1b[0m"
        paraData = f" 納:{card.pay}"

    if(card.Class == 1):
        paraData += f" 消費:{card.cost}"
    if(card.text and paraData):
        paraData += "\n"

    if(card.subType == 1):
        if(mono):
            cardType += " 対応"
        else:
            cardType += " \x1b[35m対応\x1b[0m"
    elif(card.subType == 2):
        if(mono):
            cardType += " 全力"
        else:
            cardType += " \x1b[33m全力\x1b[0m"

    output = card.name + f" ({card.cardNo}){cardType}\n{paraData}{indentTextPipe(card.text, 1, 1)}"
    print(output)

def outputCardList(cardList):
    for card in cardList:
        outputCard(card)


card_UN1 = Card(0, "投射", 1, "hajimari", 0, "a", 0, 0, "", [[5, 6, 7, 8, 9], [3, 1]])
card_UN2 = Card(0, "脇斬り", 2, "hajimari", 0, "a", 0, 0, "", [[2, 3], [2, 2]])
card_UN3 = Card(0, "牽制", 3, "hajimari", 0, "a", 0, 0, "", [[1, 2, 3], [2, 1]])
card_UN4 = Card(0, "背中刺し", 4, "hajimari", 0, "a", 0, 0, "", [[1], [3, 2]])
card_UN5 = Card(0, "二刀一閃", 5, "hajimari", 0, "a", 0, 2, "", [[2, 3], [4, 2]])
card_UN6 = Card(0, "歩法", 6, "hajimari", 0, "a", 1, 0, "集中力を1得る。\n間合 ←1→ ダスト", [], func=cardFunc.Hohou)
card_UN7 = Card(0, "潜り", 7, "hajimari", 0, "a", 1, 1, "間合 →1→ ダスト", [], func=cardFunc.Moguri)
card_UN8 = Card(0, "患い", 8, "hajimari", 0, "a", 1, 1, "対応した<攻撃>は-1/+0される。\n相手を萎縮させる。", [])
card_UN9 = Card(0, "陰の罠", 9, "hajimari", 0, "a", 2, 0, "隙\n【破棄時】攻撃「適正距離2-3、3/2、対応不可」を行う。", [2])
card_US1 = Card(1, "数多ノ刃", 1, "hajimari", 0, "a", 0, 0, "", [[1, 2], [4, 3]], 5)
card_US2 = Card(1, "闇凪ノ声", 2, "hajimari", 0, "a", 1, 0, "カードを2枚引く。", [], 4, func=cardFunc.YaminagiNoKoe)
card_US3 = Card(1, "苦ノ外套", 3, "hajimari", 0, "a", 1, 1, "対応した《攻撃》は-2/+0となる。\n相オーラ →2→ ダスト", [], 3, func=cardFunc.KuNoGaito)
card_US4 = Card(1, "奪イノ茨", 4, "hajimari", 0, "a", 1, 2, "相手は手札を全て捨て札にし、集中力が0になる。\n再起:ダストが10以上である。", [], 1)
card_HN1 = Card(0, "花弁刃", 1, "hajimari", 0, "b", 0, 0, "", [[4, 5], [-1, 1]])
card_HN2 = Card(0, "桜刀", 2, "hajimari", 0, "b", 0, 0, "", [[3, 4], [3, 1]])
card_HN3 = Card(0, "瞬霊式", 3, "hajimari", 0, "b", 0, 0, "対応不可", [[5], [3, 2]])
card_HN4 = Card(0, "返し斬り", 4, "hajimari", 0, "b", 0, 1, "【攻撃後】このカードを対応で使用したならば ダスト →1→ 自オーラ", [[3, 4], [2, 1]])
card_HN5 = Card(0, "歩法", 5, "hajimari", 0, "b", 1, 0, "集中力を1得る。\n間合 ←1→ ダスト", [])
card_HN6 = Card(0, "桜寄せ", 6, "hajimari", 0, "b", 1, 1, "相オーラ →1→ 自オーラ", [])
card_HN7 = Card(0, "光輝収束", 7, "hajimari", 0, "b", 1, 2, "ダスト →2→ 自オーラ\nダスト →1→ 自フレア", [])
card_HN8 = Card(0, "光の刃", 8, "hajimari", 0, "b", 0, 0, "超克\n【常時】Xはあなたのフレアに等しい。", [[3, 4, 5], [-2, 1]])
card_HN9 = Card(0, "精霊連携", 9, "hajimari", 0, "b", 2, 2, "【展開中】あなたの《攻撃》は+1/+0となる。", [3])
card_HS1 = Card(1, "光満ちる一刀", 1, "hajimari", 0, "b", 0, 0, "", [[3, 4], [4, 3]], 5)
card_HS2 = Card(1, "花吹雪の景色", 2, "hajimari", 0, "b", 1, 0, "相オーラ →2→ ダスト", [], 4)
card_HS3 = Card(1, "精霊たちの風", 3, "hajimari", 0, "b", 1, 1, "対応した切札でない《攻撃》を打ち消す。\nカードを1枚引く。", [], 3)
card_HS4 = Card(1, "煌めきの乱舞", 4, "hajimari", 0, "b", 0, 0, "即再起:あなたが2以上のライフへのダメージを受ける", [[3, 4, 5], [2, 2]], 2)

cardPool_U = [card_UN1, card_UN2, card_UN3, card_UN4, card_UN5, card_UN6, card_UN7, card_UN8, card_UN9,
              card_US1, card_US2, card_US3, card_US4]

cardList_U = [card_UN1, card_UN2, card_UN3, card_UN4, card_UN5, card_UN6, card_UN7,
              card_US1, card_US2, card_US3]

cardPool_H = [card_HN1, card_HN2, card_HN3, card_HN4, card_HN5, card_HN6, card_HN7, card_HN8, card_HN9,
              card_HS1, card_HS2, card_HS3, card_HS4]

cardList_H = [card_HN1, card_HN2, card_HN3, card_HN4, card_HN5, card_HN6, card_HN7,
              card_HS1, card_HS2, card_HS3]

# テスト
if __name__ == "__main__":
    outputCardList(cardPool_U)
    outputCardList(cardPool_H)