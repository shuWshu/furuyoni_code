import board as bd
import cardList
import player as pl
import commonProcess as cp

# ---------- 関数定義 ----------
# ----- ゲームの流れ -----
# 開始フェイズ
# 引数: 対象プレイヤーid
def startPhase(turnID):
    turnPlayer = players[turnID]
    otherPlayer = players[(turnID + 1) % 2]
    # 集中+1
    turnPlayer.chgVigor(1)
    # 付与札処理 # TODO:そのうち作る
    # 再構成
    tokens = cp.checkToken("[再構成] 行いますか?\nreshuffle 0:しない 1:する\n", ["reshuffle"], [[0, 1]])
    if(tokens[1] == 1):
        cp.inflictDamage.life(turnPlayer, 1)
        turnPlayer.reshuffle()
    # カードを2枚引く
    for i in range(2):
        cp.draw(turnPlayer)
# 終了フェイズ
def endPhase(turnID):
    turnPlayer = players[turnID]
    otherPlayer = players[(turnID + 1) % 2]
    while(len(turnPlayer.hand) > 2): # 手札が2枚より多い
        handText = "伏せる札を選択\ndiscard "
        for id in turnPlayer.hand:
            handText += f"{id}:{turnPlayer.cardListN[id][0].name} "
        handText += "\n"
        tokens = cp.checkToken(handText, ["discard"], [turnPlayer.hand])
        turnPlayer.moveCardN(tokens[1], 3)
# メインフェイズ
def mainPhase(turnID):
    turnPlayer = players[turnID]
    otherPlayer = players[(turnID + 1) % 2]
    while(1):
        if turnPlayer.flagThroughout == True: # 全力札を使用した
            turnPlayer.flagThroughout = False
            print("ターンエンド")
            break

        message = "[メインフェイズ] 行動を選択"
        message += "\nuseNomal "
        for id in turnPlayer.hand:
            message += f"{id}:{turnPlayer.cardListN[id][0].name} "
        message += "\nuseSpecial "
        usableSpecial = []
        for id, card in enumerate(turnPlayer.cardListS):
            if(card[1] == 0):
                message += f"{id}:{card[0].name} "
                usableSpecial.append(id)
        message += "\nbasicAction 0:前進 1:離脱 2:後退 3:纏い 4:宿し"
        message += "\nturnEnd\n"
        
        orderList = ["useNomal" , "useSpecial" , "basicAction"  , "turnEnd"]
        argListList = [turnPlayer.hand, usableSpecial, [0, 1, 2, 3, 4], []]
        tokens = cp.checkToken(message, orderList, argListList)
        orderIndex = orderList.index(tokens[0])
        if orderIndex == 0: # 通常札使用
            cp.useCardNomal(turnPlayer, otherPlayer, areas, tokens[1])
        elif orderIndex == 1: # 切札使用
            cp.useCardSpecial(turnPlayer, otherPlayer, areas, tokens[1])
        elif orderIndex == 2: # 基本動作
            # コスト支払い
            if(not turnPlayer.hand and turnPlayer.vigor == 0): # コスト無し判定
                print("コストがありません")
            else:
                # TODO:コスト選択を同じ引数に入れたい気がする
                messageCost = "[基本動作コスト] コストを選択"
                messageCost += "\nchooseCost "
                for id in turnPlayer.hand:
                    messageCost += f"{id}:{turnPlayer.cardListN[id][0].name} "
                messageCost += f"7:集中力({turnPlayer.vigor}/2)\n"
                argListListCost = [turnPlayer.hand + [7]]
                tokensCost = cp.checkToken(messageCost, ["chooseCost"], argListListCost)
                cp.basicAction(turnPlayer, areas, tokens[1], tokensCost[1])
        elif orderIndex == 3: # ターンエンド
            print("ターンエンド")
            break
# 敗北処理
# TODO:ちゃんと作る
def lose(playerID): 
    print(f"player {playerID}: LOSE")

# ----- 定義 -----
# 結晶領域定義
areas = bd.Areas()
# プレイヤー定義
player_0 = pl.Player("プレイヤー0", areas.life_0, areas.aura_0, areas.flare_0)
player_0.setCardList(cardList.cardList_U)
player_1 = pl.Player("プレイヤー1", areas.life_1, areas.aura_1, areas.flare_1)
player_1.setCardList(cardList.cardList_H)
# プレイヤーグループ
players = [player_0, player_1]
# ゲーム全体の領域保存

# インポート関数定義
cp.inflictDamage.setConfig(areas.dust, lose)

if __name__ == "__main__":
    players[0].moveCardN(1, 1)
    players[0].moveCardN(2, 3)
    players[0].moveCardN(3, 2)
    players[0].moveCardN(4, 1)
    players[0].moveCardN(5, 1)
    players[0].moveCardN(6, 1)
    players[0].chgCardS(1, -1)
    bd.moveAreaVal(areas.distance, areas.flare_0, 8)
    bd.outputBoard(areas)
    pl.outputPlayerCard(players[0])

    mainPhase(0)

    # d = cp.useCardSpecial(players[0], players[1], areas, 1)
    # print(f"return:{d}")

    bd.outputBoard(areas)
    pl.outputPlayerCard(players[0])