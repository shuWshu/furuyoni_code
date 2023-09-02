# 領域関連
# 領域クラス
# 現在値(初期値)と最大値を格納
class Area:
    def __init__(self, name, val, max) -> None:
        self.name = name # 領域名
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
def moveAreaVal(areaA, areaB, n, log=True):
    if(chgAreaVal(areaA, -n) == -1): # 失敗した場合
        return 0
    if(chgAreaVal(areaB, n) == -1): # 失敗した場合
        chgAreaVal(areaA, n)
        return 0
    if log == True:
        print(f"{areaA.name} →{n}→ {areaB.name}")
    return n

# 結晶を「できる限り」n個まで移動させる関数 A→n→B
# 返値：移動個数
def moveAreaValPoss(areaA, areaB, n):
    for i in range(n): # n回1つづつ移動
        if(moveAreaVal(areaA, areaB, 1, log=False) == 0):
            print(f"{areaA.name} →{i}→ {areaB.name}")
            return i
    print(f"{areaA.name} →{n}→ {areaB.name}") 
    return n

# 表示関数
# 引数: [P0ライフ, P0オーラ, P0フレア, P1ライフ, P1オーラ, P1フレア, 間合, ダスト]
def outputBoard(areas):
    output = f"""P0 ライフ:{areas.life_0.val}
P0 オーラ:{areas.aura_0.val}
P0 フレア:{areas.flare_0.val}
P1 ライフ:{areas.life_1.val}
P1 オーラ:{areas.aura_1.val}
P1 フレア:{areas.flare_1.val}
間合 　　:{areas.distance.val}
ダスト 　:{areas.dust.val}"""
    print(output)

class Areas:
    def __init__(self) -> None:
        self.distance = Area("間合", 10, 10)
        self.dust = Area("ダスト", 0, 100)
        self.life_0 = Area("ライフP0", 10, 100)
        self.aura_0 = Area("オーラP0", 3, 5)
        self.flare_0 = Area("フレアP0", 0, 100)
        self.life_1 = Area("ライフP0", 10, 100)
        self.aura_1 = Area("オーラP0", 3, 5)
        self.flare_1 = Area("フレアP0", 0, 100)

# テスト
if __name__ == "__main__":
    # 変数定義例
    areas = Areas()

    outputBoard(areas)
    print(moveAreaValPoss(areas.distance, areas.dust, 13))
    outputBoard(areas)