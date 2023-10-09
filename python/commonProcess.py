import board as bd
import MyPrint as myp

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
class InflictDamage:
    def __init__(self):
        self.dust = None # ダスト
        self.loseFunc = None # 敗北時処理
    # 引数: ダスト領域, 負け時の処理
    def setConfig(self, dust, loseFunc):
        self.dust = dust
        self.loseFunc = loseFunc

    # ライフダメージ
    def life(self, player, n):
        if not self.dust:
            myp.printError("need setConfig")
            return -1
        ret = bd.moveAreaValPoss(player.life, player.flare, n)
        if(player.life.val <= 0):
            return self.loseFunc(player)
        return ret
     # オーラダメージ
    def aura(self, player, n):
        if not self.dust:
            myp.printError("need setConfig")
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
# 引数: 表示メッセージ, 正解命令リスト, 引数リストのリスト(無しならNone)
# 返値: トークン(str), 引数(int 無しなら-1)
def checkToken(message, orderList, argListList):
    while(1):
        Input = input(message)
        token = Input.split()
        order = token[0]
        if order in orderList:
            index = orderList.index(order)
            if argListList[index] is None: # 引数無しで良い場合
                return order, -1
            elif not argListList[index]: # 引数が空
                myp.printError("その命令は選択できない")
            elif len(token) != 2: # 引数の数が正しくない
                myp.printError("引数の数が正しくない")
            else: # 引数有り
                try: 
                    if int(token[1]) in argListList[index]:
                        return order, int(token[1])
                    else:
                        myp.printError("引数の値が正しくない")
                except ValueError:
                    myp.printError("引数が整数ではない")
        else:
            myp.printError("命令が存在しない")

# 現在間合確認
# 引数: 現在間合の値, 適正距離配列
# 返値: 成功:1 失敗:-1
def checkDist(dist, cardDist):
    if dist in cardDist: # 当たった場合
        return 1
    else:
        return -1
    
# 攻撃情報オブジェクト
class AttackData:
    def __init__(self, Class, subType, dist, Damage, megami):
        self.Class = Class
        self.subType = subType
        self.dist = dist
        self.damage = Damage
        self.megami = megami
        self.canceled = False

# 攻撃処理
# 引数: 使用者, 被使用者, ボードデータ, 適正距離[], ダメージ[], 通常or切札, サブタイプ, メガミ名, 対応不可TF
# 返値: 成功時:1, 失敗時(打消,回避など):0, 不成立時:-1
def attack(usePlayer, usedPlayer, areas, cardDist, damage, cardClass, subType, megamiName, noReaction=False):
    # 攻撃オブジェクトの作成
    attackData = AttackData(cardClass, subType, cardDist, damage, megamiName)
    distMax = max(attackData.dist)
    distMin = min(attackData.dist)
    if distMax == distMin:
        dist = str(distMax)
    else:
        dist = str(distMin) + "-" + str(distMax)
    myp.printDebag(f"攻撃{dist} {attackData.damage[0]}/{attackData.damage[1]}を使用")
    # 間合確認
    if checkDist(areas.distance.val, attackData.dist) != 1: # 避けられた場合
        myp.printError("適正距離が不適合")
        return -1
    
    
    # 対応メッセージ作成
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

    while(1):
        # ダメージ選択 or 対応
        tokens = checkToken(message, orderList, argListList)
        orderIndex = orderList.index(tokens[0])

        # 対応使用
        if orderIndex == 0: # 対応しない
            break
        else: # 対応した
            if orderIndex == 1:
                reactionFunc = useCardNomal(usedPlayer, usePlayer, areas, tokens[1], reaction=True, attackData=attackData)
            elif orderIndex == 2:
                reactionFunc = useCardSpecial(usedPlayer, usePlayer, areas, tokens[1], reaction=True, attackData=attackData)
            if reactionFunc != -1: # 対応使用成功
                if attackData.canceled == True: # 打消
                    return 0
                # 間合確認
                if checkDist(areas.distance.val, attackData.dist) != 1: # 避けられた場合
                    myp.printDebag("適正距離が不適合(回避)")
                    return 0
                # ダメージ選択
                tokens = checkToken("[《攻撃》ダメージ選択 ]\ndamageBy 0:オーラ 1:ライフ\n", ["damageBy"], [[0, 1]])
                break
    
    # ダメージ処理
    if usedPlayer.aura.val < attackData.damage[0]: # オーラが少ない
        myp.printDebag("オーラが不足している")
        inflictDamage.life(usedPlayer, attackData.damage[1])
    elif attackData.damage[0] == -1: # オーラダメージが-
        myp.printDebag("オーラダメージが-")
        inflictDamage.life(usedPlayer, attackData.damage[1])
    elif attackData.damage[1] == -1: # ライフダメージが-
        myp.printDebag("ライフダメージが-")
        inflictDamage.life(usedPlayer, attackData.damage[0])
    else:
        if tokens[1] == 0:
            inflictDamage.aura(usedPlayer, attackData.damage[0])
        else:
            inflictDamage.life(usedPlayer, attackData.damage[1])
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
# カード使用の前後共通処理のみ
# 引数: 使用者, 被使用者, ボード情報, カードid, 対応フラグ, 対応時の攻撃情報
# 返値: 成功:1 不成立:-1 対応の場合
def useCardNomal(usePlayer, usedPlayer, areas, cardID, reaction = False, attackData = None):
    usingCard = usePlayer.cardListN[cardID][0]
    if usingCard.subType == 2 and (usePlayer.flagUsedCard or usePlayer.flagUsedBasic): # 全力札使用判定
        myp.printError("このターン中は全力札を使えない")
        return -1
    #カードの使用部分
    result = -1
    if reaction == False:
        result = usingCard.use(usePlayer, usedPlayer, areas) # カード使用
    else:
        if usingCard.subType != 1:
            myp.printError("そのカードは対応ではない")
            return -1
        result = usingCard.use(usePlayer, usedPlayer, areas, attackData = attackData) # 対応使用

    if result == -1: # 失敗時(間合不適合など)
        myp.printError("そのカードは使用出来ない")
        return -1
    else:
        usePlayer.moveCardN(cardID, 2) # 捨札へ移動
        usePlayer.flagUsedCard = True
        if usingCard.subType == 2:
            myp.printDebag("全力札を解決した")
            usePlayer.flagThroughout = True
        return 1
    
# 切札の使用
# カード使用の前後処理のみ
# 引数: 使用者, 被使用者, ボード情報, カードid, 対応フラグ, 対応時の攻撃情報
# 返値: 成功:1 不成立:-1
def useCardSpecial(usePlayer, usedPlayer, areas, cardID, reaction = False, attackData = None):
    usingCard = usePlayer.cardListS[cardID][0]
    if usingCard.subType == 2 and (usePlayer.flagUsedCard or usePlayer.flagUsedBasic):
        myp.printError("このターン中は全力札を使えない")
        return -1
    # フレア支払い
    cost =  usingCard.cost
    if bd.moveAreaVal(usePlayer.flare, areas.dust, cost) == -1:
        myp.printError("フレアが不足している")
        return -1        
    
    #カードの使用部分
    result = -1
    if reaction == False:
        result = usingCard.use(usePlayer, usedPlayer, areas) # カード使用
    else:
        if usingCard.subType != 1:
            myp.printError("そのカードは対応ではない")
            return -1
        result = usingCard.use(usePlayer, usedPlayer, areas, attackData = attackData) # 対応使用

    if result == -1: # 失敗時(間合不適合など)
        myp.printError("そのカードは使用出来ない")
        return -1
    else: # 成功or攻撃打消など
        usePlayer.chgCardS(cardID, 1) # 使用済へ変更
        usePlayer.flagUsedCard = True
        if usingCard.subType == 2:
            myp.printDebag("全力札を解決した")
            usePlayer.flagThroughout = True
        return 1

# 基本動作
# 引数: 使用者, ボード情報, アクションID, コスト
# アクションID: 0:前進 1:離脱 2:後退 3:纏い 4:宿し
# 返値: 成功:1 失敗:-1
def basicAction(usePlayer, areas, actionID, costID):
    # 動作の中身
    done = 0
    if actionID == 0: # 前進
        if areas.distance.val <= 2:
            myp.printError("達人の間合以内である")
            return -1
        done = bd.moveAreaVal(areas.distance, usePlayer.aura, 1)
    elif actionID == 1: # 離脱
        if areas.distance.val > 2:
            myp.printError("達人の間合より遠い")
            return -1
        done = bd.moveAreaVal(areas.dust, areas.distance, 1)
    elif actionID == 2: # 後退
        done = bd.moveAreaVal(usePlayer.aura, areas.distance, 1)
    elif actionID == 3: # 纏い
        done = bd.moveAreaVal(areas.dust, usePlayer.aura, 1)
    elif actionID == 4: # 宿し
        done = bd.moveAreaVal(usePlayer.aura, usePlayer.flare, 1)
    
    if done == -1: # 処理できなかった
        myp.printError("結晶の移動が不可能")
        return -1

    # 消費を払う
    if costID == 7:
        usePlayer.chgVigor(-1)
    else:
        usePlayer.moveCardN(costID, 3) # 伏札へ移動
    usePlayer.flagUsedBasic = True
    return 1

# ダメージ補正処理
# 引数: ダメージ配列, 補正配列
def damageCorrection(damage, correction):
    damageBefore = f"{damage[0]}/{damage[1]}"
    for i in range(2):
        if damage[i] >= 0:
            damage[i] += correction[i]
            if damage[i] < 0:
                damage[i] = 0
    myp.printDebag(f"{damageBefore} →({correction[0]}/{correction[1]})→ {damage[0]}/{damage[1]}")
    return damage

    