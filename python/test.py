class Area:
    def __init__(self, val, max_val):
        self._val = val
        self._max = max_val
        self.func = None

    def setFunc(self, func):
        self.func = func

    @property
    def val(self):
        return self._val
    @val.setter
    def val(self, new_val):
        self._val = new_val
        if self.func:
            self.func()

class Player:
    def __init__(self, life, aura, flare):
        self.vigor = 0
        self.cardListN = []
        self.cardListS = []
        self.deck = [0, 1, 2, 3, 4, 5, 6]
        self.hand = []
        self.discard = []
        self._life = Area(life, life)

    @property
    def life(self):
        return self._life

def test():
    print("test")

# テスト
life = Area(5, 10)
life.setFunc(test)
player = Player(life, aura=0, flare=0)
print("初期 life:", player.life.val)
player.life.val = 8
print("変更後 life:", player.life.val)
player.life.val = 15  # 範囲外の値をセットしようとするとエラーが表示される

x = [1, 2]
z = [3, 4]
x = z
print(x)