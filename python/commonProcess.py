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
class InflictDamage:
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
inflictDamage = InflictDamage()

# 焦燥
def impatience(player):
    tokens = checkToken("[焦燥] どちらでダメージを受けますか?\nimpatience 0:オーラ 1:ライフ\n", ["impatience"], [[0, 1]])
    if tokens[1] == 0:
        inflictDamage.aura(player, 1)
    else:
        inflictDamage.life(player, 1)

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

# 現在間合確認
# 引数: 現在間合の値, 適正距離配列
# 返値: 成功:1 失敗:-1
def checkDist(dist, cardDist):
    if dist in cardDist: # 当たった場合
        return 1
    else:
        print("適正距離不適合")
        return -1

# 攻撃処理
# 引数: 使用者, 被使用者, ボードデータ, 適正距離[], ダメージ[], 対応不可TF
# 返値: 成功時:1, 失敗時(打消,回避など):0, 不成立時:-1
def attack(usePlayer, usedPlayer, areas, cardDist, damage, noReaction=False):
    # 間合確認
    if checkDist(areas.distance.val, cardDist) != 1: # 避けられた場合
        return -1
    
    # ダメージ選択 or 対応
    message = "[《攻撃》への対応 ] 行動を選択"
    message += "\ndamageBy 0:オーラ 1:ライフ"
    orderList = ["damageBy"]
    argListList = [[0, 1]]
    if not noReaction: # 対応可能の場合
        message += "\nreactionNomal "
        for id in usedPlayer.hand:
            message += f"{id}:{usedPlayer.cardListN[id][0].name} "
        message += "\nreactionSpecial "
        usableSpecial = []
        for id, card in enumerate(usedPlayer.cardListS):
            if(card[1] == 0):
                message += f"{id}:{card[0].name} "
                usableSpecial.append(id)
        orderList = ["damageBy" , "reactionNomal" , "reactionSpecial"]
        argListList = [[0, 1], usedPlayer.hand, usableSpecial]
    message += "\n"
    tokens = checkToken(message, orderList, argListList)
    orderIndex = orderList.index(tokens[0])

    # 対応使用
    if orderIndex != 0:
        if orderIndex == 1:
            # TODO:カードの使用
            print(tokens)
        elif orderIndex == 2:
            # TODO:カードの使用
            print(tokens)

        # 間合確認
        if checkDist(areas.distance.val, cardDist) != 1: # 避けられた場合
            return 0
        # ダメージ選択
        argListList = [[0, 1], usedPlayer.hand, usableSpecial]
        tokens = checkToken("[《攻撃》ダメージ選択 ]\ndamageBy 0:オーラ 1:ライフ\n", ["damageBy"], [[0, 1]])
    # ダメージ処理
    if usedPlayer.aura.val < damage[0] or damage[0] == -1: # オーラが少ない or オーラダメージが-
        inflictDamage.life(usedPlayer, damage[1])
    elif damage[1] == -1: # ライフダメージが-
        inflictDamage.life(usedPlayer, damage[0])
    else:
        if tokens[1] == 0:
            inflictDamage.aura(usedPlayer, damage[0])
        else:
            inflictDamage.life(usedPlayer, damage[1])
    return 1
        
# ドロー処理
# 引数: プレイヤー
# 返値: 成功:1 失敗(焦燥):-1
def draw(player):
    if(player.drawCard() == -1):
        impatience(player)
        return -1
    return 1

# 通常札の使用
# カード使用の前後処理のみ
# 引数: 使用者, 被使用者, ボード情報, カードid
# 返値: 成功:1 不成立:-1
def useCardNomal(usePlayer, usedPlayer, areas, cardID):
    result = usePlayer.cardListN[cardID][0].use(usePlayer, usedPlayer, areas)
    if result == -1: # 失敗時(間合不適合など)
        print("カード使用が出来ない")
        return -1
    else:
        usePlayer.moveCardN(cardID, 2) # 捨札へ移動
        return 1
    
# 切札の使用
# カード使用の前後処理のみ
# 引数: 使用者, 被使用者, ボード情報, カードid
# 返値: 成功:1 不成立:-1
def useCardSpecial(usePlayer, usedPlayer, areas, cardID):
    # フレア支払い
    cost =  usePlayer.cardListS[cardID][0].cost
    
    if bd.moveAreaVal(usePlayer.flare, areas.dust, cost) == -1:
        print("フレア不足")
        return -1        
    
    result = usePlayer.cardListS[cardID][0].use(usePlayer, usedPlayer, areas)
    if result == -1: # 失敗時(間合不適合など)
        print("カード使用が出来ない")
        return -1
    else:
        usePlayer.chgCardS(cardID, 1) # 使用済へ変更
        return 1