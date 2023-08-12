import board
import cardList
import player

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

board.outputBoard(gameBoard)
player.outputPlayersCard(players)