import random
import board as bd
import cardList as cl
import cardFunc as cf
import player as pl
import commonProcess as cp
import MyPrint as myp

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
    
    # フラグリセット
    turnPlayer.flagThroughout = False
    turnPlayer.flagUsedBasic = False
    turnPlayer.flagUsedCard = False

# メインフェイズ
def mainPhase(turnID):
    turnPlayer = players[turnID]
    otherPlayer = players[(turnID + 1) % 2]
    while(1):
        bd.outputBoard(areas)

        if turnPlayer.flagThroughout == True: # 全力札を使用した
            myp.printLog("ターンエンド")
            break

        message = "[メインフェイズ] 行動を選択"
        message += "\nuseNomal "
        useableCard = ""
        for id in turnPlayer.hand:
            useableCard += f"{id}:{turnPlayer.cardListN[id][0].name} "
        message += useableCard
        message += "\nuseSpecial "
        usableSpecial = []
        for id, card in enumerate(turnPlayer.cardListS):
            if(card[1] == 0):
                message += f"{id}:{card[0].name} "
                usableSpecial.append(id)
        message += f"\nbasicAction {useableCard}7:集中力({turnPlayer.vigor}/2)"
        message += "\nturnEnd\n"
        
        orderList = ["useNomal" , "useSpecial" , "basicAction"  , "turnEnd"]
        argListList = [turnPlayer.hand, usableSpecial, turnPlayer.hand + [7], None]
        tokens = cp.checkToken(message, orderList, argListList)
        orderIndex = orderList.index(tokens[0])
        if orderIndex == 0: # 通常札使用
            cp.useCardNomal(turnPlayer, otherPlayer, areas, tokens[1])
        elif orderIndex == 1: # 切札使用
            cp.useCardSpecial(turnPlayer, otherPlayer, areas, tokens[1])
        elif orderIndex == 2: # 基本動作
            # 集中力があるかの確認
            if tokens[1] == 7 and turnPlayer.vigor == 0:
                myp.printError("集中力がない")
            else:
                tokensAction = cp.checkToken("[基本動作] 行う動作を選択\nchooseAction 0:前進 1:離脱 2:後退 3:纏い 4:宿し\n", ["chooseAction"], [[0, 1, 2, 3, 4]])
                cp.basicAction(turnPlayer, areas, tokensAction[1], tokens[1])
        elif orderIndex == 3: # ターンエンド
            myp.printLog("ターンエンド")
            break
# 敗北処理
def lose(playerID):
    myp.printLog(f"player {playerID}: LOSE")
    exit()

# ----- 定義 -----
# 結晶領域定義
areas = bd.Areas()
# プレイヤー定義
player_0 = pl.Player("プレイヤー0", areas.life_0, areas.aura_0, areas.flare_0)
player_0.setCardList(cl.cardList_U)
player_1 = pl.Player("プレイヤー1", areas.life_1, areas.aura_1, areas.flare_1)
player_1.setCardList(cl.cardList_H)
# プレイヤーグループ
players = [player_0, player_1]
# ゲーム全体の領域保存

# カード処理の登録
cl.card_UN1.setFunc(cf.MakeAttack(cl.card_UN1))
cl.card_UN2.setFunc(cf.MakeAttack(cl.card_UN2))
cl.card_UN3.setFunc(cf.MakeAttack(cl.card_UN3))
cl.card_UN4.setFunc(cf.MakeAttack(cl.card_UN4))
cl.card_UN5.setFunc(cf.MakeAttack(cl.card_UN5))
cl.card_UN6.setFunc(cf.Hohou)
cl.card_UN7.setFunc(cf.Moguri)
cl.card_US1.setFunc(cf.MakeAttack(cl.card_US1))
cl.card_US2.setFunc(cf.YaminagiNoKoe)
cl.card_US3.setFunc(cf.KuNoGaito)

cl.card_HN1.setFunc(cf.MakeAttack(cl.card_HN1))
cl.card_HN2.setFunc(cf.MakeAttack(cl.card_HN2))
cl.card_HN3.setFunc(cf.MakeNoReaction(cl.card_HN3))
cl.card_HN4.setFunc(cf.MakeKaeshigiri(cl.card_HN4))
cl.card_HN5.setFunc(cf.Hohou)
cl.card_HN6.setFunc(cf.Sakurayose)
cl.card_HN7.setFunc(cf.Koukishusoku)
cl.card_HS1.setFunc(cf.MakeAttack(cl.card_HS1))
cl.card_HS2.setFunc(cf.SakurahubukiNoKeshiki)
cl.card_HS3.setFunc(cf.SeireitatiNoKaze)

# インポート関数定義
cp.inflictDamage.setConfig(areas.dust, lose)

# ゲーム全体処理
def overallProcessing(firstID = None, tutorial = False):
    # デッキ設計
    if tutorial:
        player_0.deck = [0, 3, 6, 4, 5, 1, 2]
        player_1.deck = [0, 2, 4, 1, 3, 5, 6]
        firstID = 0
    else:
        player_0.reshuffle()
        player_1.reshuffle()
        if firstID is None:
            firstID = random.randint(0, 1)
    secondID = (firstID + 1) % 2

    # 手札と集中
    # for i in range(3):
    #     player_0.drawCard()
    #     player_1.drawCard()
    players[secondID].chgVigor(1)

    bd.outputBoard(areas)
    
    turnCount = 1
    # 先手最初のターン
    myp.printDebag(f"先攻{turnCount}ターン目")
    mainPhase(firstID)
    endPhase(firstID)
    myp.printDebag(f"後攻{turnCount}ターン目")
    mainPhase(secondID)
    endPhase(secondID)
    while(1):
        turnCount += 1
        # 先手ターン
        myp.printDebag(f"先攻{turnCount}ターン目")
        startPhase(firstID)
        mainPhase(firstID)
        endPhase(firstID)
        # 後手ターン
        myp.printDebag(f"後攻{turnCount}ターン目")
        startPhase(secondID)
        mainPhase(secondID)
        endPhase(secondID)

def testCode():
    players[0].moveCardN(0, 1)
    players[0].moveCardN(1, 0)
    players[0].moveCardN(2, 3)
    players[0].moveCardN(3, 2)
    players[0].moveCardN(4, 1)
    players[0].moveCardN(5, 1)
    players[0].moveCardN(6, 1)
    players[0].chgCardS(1, 0)
    players[0].chgCardS(1, -1)
    players[1].moveCardN(0, 1)
    players[1].moveCardN(1, 1)
    players[1].moveCardN(2, 1)
    players[1].moveCardN(3, 1)
    bd.moveAreaVal(areas.distance, areas.flare_0, 7)
    bd.moveAreaVal(areas.flare_0, areas.dust, 6)
    bd.outputBoard(areas)
    pl.outputPlayerCard(players[0])

    mainPhase(0)

    # d = cp.useCardSpecial(players[0], players[1], areas, 1)
    # print(f"return:{d}")

    bd.outputBoard(areas)
    pl.outputPlayerCard(players[0])

if __name__ == "__main__":
    overallProcessing(tutorial=True)