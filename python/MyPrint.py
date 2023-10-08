# メッセージ出力特殊形式

# ゲームログ用 青
# ユーザへ見せる
# TODO:csvへ記録する機能を付ける
def printLog(text):
    print(f"\x1b[34m{text}\x1b[0m")

# デバッグ用 灰色
# ユーザには基本見せない
def printDebag(text):
    # 38;2;r;g;bm で色指定
    print(f"\033[38;2;128;128;128m{text}\033[0m")

# 自動的な動作のログ 緑
# カードや結晶の移動など
def printMove(text):
    print(f"\x1b[32m{text}\x1b[0m")

# エラーメッセージ 赤
# システム，ゲームルール的なエラー
# 再起的に処理される部分
# 丁寧に記述する？
def printError(text):
    print(f"\x1b[31m{text}\x1b[0m")

if __name__ == "__main__":
    printLog("Hello")
    printDebag("Hello")
    printMove("Hello")
    printError("Hello")
