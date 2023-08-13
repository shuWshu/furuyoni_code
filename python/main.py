import board
import cardList
import player

# ---------- 関数定義 ----------
# ----- 共通処理 -----
# ダメージ
# 引数: プレイヤー, ダスト領域, 領域(文字列), 値
def damage(player, area, n):
    if(area == "life"):
        return board.moveAreaValPoss(player.life, player.flare, n)
    elif(area == "aura"):
        return board.moveAreaVal(player.aura, dust, n)
    elif(area == "flare"):
        return board.moveAreaVal(player.flare, dust, n)
    return -1
# 焦燥
def impatience(player):
    token = checkToken("[焦燥]どちらでダメージを受けますか?\nimpatience 0:オーラ 1:ライフ\n", ["impatience"], ["0", "1"])
    if token.split()[1] == "0":
        damage(player, "aura", 1)
    else:
        damage(player, "life", 1)
# トークン照合 トークンが違うならループする
# 引数: 表示メッセージ, 正解トークンリスト, 引数リスト
def checkToken(message, tokenList, argList):
    while(1):
        Input = input(message)
        token = Input.split()
        if token[0] in tokenList:
            if len(token) != 2:
                print("\x1b[31mError:引数の数が正しくありません\x1b[0m")
            else:
                if token[1] in argList:
                    return Input
                print("\x1b[31mError:引数の値が正しくありません\x1b[0m")
        else:
            print("\x1b[31mError:トークンが合致しません\x1b[0m")

# ----- ゲームの流れ -----
# 開始フェイズ処理
# 引数: 対象プレイヤー
def startPhase(player):
    # 集中+1
    player.chgVigor(1)
    # 付与札処理
    # TODO:そのうち作る
    # 再構成
    token = checkToken("[再構成]行いますか?\nreshuffle 0:しない 1:する\n", ["reshuffle"], ["0", "1"])
    if(token.split()[1] == "1"):
        damage(player, "life", 1)
        player.reshuffle()
    # カードを2枚引く
    for i in range(2):
        if(player.drawCard() == -1):
            impatience(player)

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
player_0 = player.Player(life_0, aura_0, flare_0)
player_0.setCardList(cardList.cardList_U)
player_1 = player.Player(life_1, aura_1, flare_1)
player_1.setCardList(cardList.cardList_H)
players = [player_0, player_1]

if __name__ == "__main__":
    player_0.moveCardN(1, 1)
    player_0.moveCardN(2, 2)
    player_0.moveCardN(3, 3)
    player_0.moveCardN(4, 1)
    player_0.moveCardN(5, 2)
    player_0.moveCardN(6, 3)
    board.outputBoard(gameBoard)
    player.outputPlayerCard(player_0)

    startPhase(player_0)
    board.outputBoard(gameBoard)
    player.outputPlayerCard(player_0)