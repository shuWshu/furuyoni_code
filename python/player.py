# プレイヤー関連
import random
import board
import cardList

# 各プレイヤー紐付け情報
class Player:
    def __init__(self, life, aura, flare):
        self.vigor = 0 # 集中力
        self.cardListN = [] # 通常札リスト&所在
        self.cardListS = [] # 切札リスト&使用済
        self.deck = [0, 1, 2, 3, 4, 5, 6] # 山札順番管理
        self.hand = [] # 手札管理
        self.discard = [] # 捨札&伏せ札の順番管理
        self.life = life
        self.aura = aura
        self.flare = flare
    # カードリストの登録
    def setCardList(self, cardList):
        self.cardListN.clear() # リセット
        self.cardListS.clear() # リセット
        for i, card in enumerate(cardList):
            if(i < 7):
                self.cardListN.append([card, 0]) # [カード内容, 場所] 山札:0, 手札:1, 捨札:2, 伏札:3, 付与札:4
            else:
                self.cardListS.append([card, 0]) # [カード内容, 使用状況] 未使用:0, 使用済:1

    # 集中力増減
    # 返値: 成功なら変更後値, 失敗なら-1を返す．
    def chgVigor(self, n):
        self.vigor += n
        if(self.vigor > 2 or self.vigor < 0):
            self.vigor -= n
            return -1; 
        return self.vigor
    # 再構成
    def reshuffle(self):
        for i, card in enumerate(self.cardListN):
            if(card[1] == 2 or card[1] == 3):
                card[1] = 0
                self.deck.append(i)
        self.discard = []
        random.shuffle(self.deck)
    # カードの移動
    # 引数: カードid, 移動後
    def moveCardN(self, id, area):
        prevArea = self.cardListN[id][1]
        # 移動前
        if(prevArea == 0): # 山札
            index = self.deck.index(id) 
            self.deck.pop(index) # 山札リストから削除
        elif(prevArea == 1): # 手札
            index = self.hand.index(id) 
            self.hand.pop(index) 
        elif(prevArea == 2 or prevArea == 3): # 捨伏札にある
            index = self.discard.index(id)
            self.discard.pop(index) # 捨伏リストから削除
        # 移動後
        if(area == 0): # 山札
            self.deck.append(id) # 山札リストへ追加
        elif(area == 1): # 山札
            self.hand.append(id) # 山札リストへ追加
        elif(area == 2 or area == 3): # 捨伏札にある
            self.discard.append(id) # 捨伏リストへ追加
        self.cardListN[id][1] = area
    # 切札状態変更
    # 引数: カードid, 状態(-1なら逆にする, 0or1で指定)
    def chgCardS(self, id, state = -1):
        if(state == -1):
            self.cardListS[id][1] = (self.cardListS[id][1] + 1) % 2
        else:
            self.cardListS[id][1] = state
    # ドロー処理
    # 返値: 成功なら引いたカードid, 失敗なら-1
    def drawCard(self):
        if not self.deck:
            return -1
        drawn = self.deck.pop(0)
        self.cardListN[drawn][1] = 1
        self.hand.append(drawn)
        return drawn

# 各領域カード表示
def outputPlayerCard(player, player_name = ""):
    deckText = "山札(上　下): "
    for id in player.deck:
        deckText += player.cardListN[id][0].name + ", "
    deckText += "\n"

    handText = "手札(順序無): "
    for id in player.hand:
        handText += player.cardListN[id][0].name + ", "
    handText += "\n"

    discText = "捨札(先　後): "
    laidText = "伏札(順序無): "
    for id in player.discard:
        if(player.cardListN[id][1] == 2):
            discText += player.cardListN[id][0].name + ", "
        else:
            laidText += player.cardListN[id][0].name + ", "
    discText += "\n"
    laidText += "\n"
    
    unusedText = "切札(未使用): "
    usedText = "切札(使用済): "
    for card in player.cardListS:
        if(card[1] == 0):
            unusedText += card[0].name + ", "
        else:
            usedText += card[0].name + ", "
    unusedText += "\n"

    nameText = ""
    if(player_name):
        nameText += player_name + "\n"
    output = nameText + deckText + handText + discText + laidText + unusedText + usedText
    print(output)

# 各プレイヤーカード表示
def outputPlayersCard(players, playersName = ["プレイヤー0", "プレイヤー1"]):
    outputPlayerCard(players[0], playersName[0])
    outputPlayerCard(players[1], playersName[1])

# テスト
if __name__ == "__main__":
    # プレイヤー定義
    player_0 = Player(board.life_0, board.aura_0, board.flare_0)
    player_0.setCardList(cardList.cardList_U)
    player_1 = Player(board.life_1, board.aura_1, board.flare_1)
    player_1.setCardList(cardList.cardList_H)
    players = [player_0, player_1]
