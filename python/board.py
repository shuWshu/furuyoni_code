# 領域関連
# 領域クラス
# 現在値(初期値)と最大値を格納
class Area:
    def __init__(self, val, max) -> None:
        self.val = val
        self.max = max

# 値を変化させる関数
# 返値：成功なら変更後の値，失敗なら-1
def chgAreaVal(area, n):
    area.val += n
    if(area.val < 0 or area.val > area.max):
        area.val -= n
        return -1
    return area.val

# 結晶をn個移動させる関数 A→n→B
# 返値：移動個数
def moveAreaVal(areaA, areaB, n):
    if(chgAreaVal(areaA, -n) == -1): # 失敗した場合
        return 0
    if(chgAreaVal(areaB, n) == -1): # 失敗した場合
        chgAreaVal(areaA, n)
        return 0
    return n

# 結晶を「できる限り」n個まで移動させる関数 A→n→B
# 返値：移動個数
def moveAreaValPoss(areaA, areaB, n):
    for i in range(n): # n回1つづつ移動
        if(moveAreaVal(areaA, areaB, 1) == 0):
            return i
    return n

# 表示関数
# 引数: [P0ライフ, P0オーラ, P0フレア, P1ライフ, P1オーラ, P1フレア, 間合, ダスト]
def outputBoard(board):
    output = f"""P0 ライフ:{board[0].val}
P0 オーラ:{board[1].val}
P0 フレア:{board[2].val}
P1 ライフ:{board[3].val}
P1 オーラ:{board[4].val}
P1 フレア:{board[5].val}
間合 　　:{board[6].val}
ダスト 　:{board[7].val}"""
    print(output)

# テスト
if __name__ == "__main__":
    # 変数定義例
    distance = Area(10, 10)
    dust = Area(0, 100)
    life_0 = Area(10, 100)
    aura_0 = Area(3, 5)
    flare_0 = Area(0, 100)
    life_1 = Area(10, 100)
    aura_1 = Area(3, 5)
    flare_1 = Area(0, 100)

    board = [life_0, aura_0, flare_0, life_1, aura_1, flare_1, distance, dust]

    outputBoard(board)
    print(moveAreaValPoss(distance, dust, 13))
    outputBoard(board)