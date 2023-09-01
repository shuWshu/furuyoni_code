import board as bd
import cardList
import player as pl
import commonProcess as cp

import cardFunc # テスト用

# ---------- 関数定義 ----------
# ----- ゲームの流れ -----
# 開始フェイズ
# 引数: 対象プレイヤー
def startPhase(player):
    # 集中+1
    player.chgVigor(1)
    # 付与札処理
    # TODO:そのうち作る
    # 再構成
    tokens = cp.checkToken("[再構成] 行いますか?\nreshuffle 0:しない 1:する\n", ["reshuffle"], [[0, 1]])
    if(tokens[1] == 1):
        cp.inflictDamage.life(player, 1)
        player.reshuffle()
    # カードを2枚引く
    for i in range(2):
        if(player.drawCard() == -1):
            cp.impatience(player)
# 終了フェイズ
def endPhase(player):
    while(len(player.hand) > 2): # 手札が2枚より多い
        handText = "伏せる札を選択\ndiscard "
        for id in player.hand:
            handText += f"{id}:{player.cardListN[id][0].name} "
        handText += "\n"
        tokens = cp.checkToken(handText, ["discard"], [player.hand])
        player.moveCardN(tokens[1], 3)
# メインフェイズ
def mainPhase(player):
    while(1):
        message = "[メインフェイズ] 行動を選択"
        message += "\nuseNomal "
        for id in player.hand:
            message += f"{id}:{player.cardListN[id][0].name} "
        message += "\nuseSpecial "
        usableSpecial = []
        for id, card in enumerate(player.cardListS):
            if(card[1] == 0):
                message += f"{id}:{card[0].name} "
                usableSpecial.append(id)
        message += "\nbasicAction 0:前進 1:離脱 2:後退 3:纏い 4:宿し"
        message += "\nturnEnd\n"
        
        orderList = ["useNomal" , "useSpecial" , "basicAction"  , "turnEnd"]
        argListList = [player.hand, usableSpecial, [0, 1, 2, 3, 4], []]
        tokens = cp.checkToken(message, orderList, argListList)
        orderIndex = orderList.index(tokens[0])
        if orderIndex == 0:
            print(tokens)
        elif orderIndex == 1:
            print(tokens)
        elif orderIndex == 2:
            print(tokens)
        elif orderIndex == 3: # ターンエンド
            print(tokens)
            break
# 敗北処理
# TODO:ちゃんと作る
def lose(player): 
    print("lose")

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
    players[0].moveCardN(2, 1)
    players[0].moveCardN(3, 1)
    players[0].moveCardN(4, 1)
    players[0].moveCardN(5, 2)
    players[0].moveCardN(6, 3)
    players[0].chgCardS(1, -1)
    bd.outputBoard(areas)
    pl.outputPlayerCard(players[0])

    cp.attack(players[1], players[0], areas, [3, 4, 5, 10], [4, 11], noReaction=True)

    bd.outputBoard(areas)
    pl.outputPlayerCard(players[0])