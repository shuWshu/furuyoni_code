import board
import cardList
import player as pl

# ---------- 関数定義 ----------
# ----- 共通処理 -----
# ダメージ
# 引数: プレイヤー, ダスト領域, 領域(文字列), 値
def damage(player, area, n):
    if(area == "life"):
        ret = board.moveAreaValPoss(player.life, player.flare, n)
        if(player.life.val <= 0):
            return lose(player)
        return ret
    elif(area == "aura"):
        return board.moveAreaVal(player.aura, dust, n)
    elif(area == "flare"):
        return board.moveAreaVal(player.flare, dust, n)
    return -1
# 焦燥
def impatience(player):
    tokens = checkToken("[焦燥] どちらでダメージを受けますか?\nimpatience 0:オーラ 1:ライフ\n", ["impatience"], [[0, 1]])
    if tokens[1] == 0:
        damage(player, "aura", 1)
    else:
        damage(player, "life", 1)
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

            

# ----- ゲームの流れ -----
# 開始フェイズ
# 引数: 対象プレイヤー
def startPhase(player):
    # 集中+1
    player.chgVigor(1)
    # 付与札処理
    # TODO:そのうち作る
    # 再構成
    tokens = checkToken("[再構成] 行いますか?\nreshuffle 0:しない 1:する\n", ["reshuffle"], [[0, 1]])
    if(tokens[1] == 1):
        damage(player, "life", 1)
        player.reshuffle()
    # カードを2枚引く
    for i in range(2):
        if(player.drawCard() == -1):
            impatience(player)
# 終了フェイズ
def endPhase(player):
    while(len(player.hand) > 2): # 手札が2枚より多い
        handText = "伏せる札を選択\ndiscard "
        for id in player.hand:
            handText += f"{id}:{player.cardListN[id][0].name} "
        handText += "\n"
        tokens = checkToken(handText, ["discard"], [player.hand])
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
        tokens = checkToken(message, orderList, argListList)
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
# 領域定義
distance = board.Area(10, 10)
dust = board.Area(0, 100)
life_0 = board.Area(10, 100)
aura_0 = board.Area(3, 5)
flare_0 = board.Area(0, 100)
life_1 = board.Area(10, 100)
aura_1 = board.Area(3, 5)
flare_1 = board.Area(0, 100)
gameBoard = [life_0, aura_0, flare_0, life_1, aura_1, flare_1, distance, dust]
# プレイヤー定義
player_0 = pl.Player(life_0, aura_0, flare_0)
player_0.setCardList(cardList.cardList_U)
player_1 = pl.Player(life_1, aura_1, flare_1)
player_1.setCardList(cardList.cardList_H)
players = [player_0, player_1]

if __name__ == "__main__":
    player_0.moveCardN(1, 1)
    player_0.moveCardN(2, 1)
    player_0.moveCardN(3, 1)
    player_0.moveCardN(4, 1)
    player_0.moveCardN(5, 2)
    player_0.moveCardN(6, 3)
    player_0.chgCardS(1, -1)
    board.outputBoard(gameBoard)
    pl.outputPlayerCard(player_0)

    mainPhase(player_0)

    damage(player_0, "life", 6)
    damage(player_0, "life", 6)

    board.outputBoard(gameBoard)
    pl.outputPlayerCard(player_0)