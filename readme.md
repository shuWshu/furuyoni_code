# ファイル一覧

# 設計

# コマンド

## 汎用

-   impatience
    焦燥ダメージ選択
    引数: 0:オーラ 1:ライフ

## 開始フェイズ

-   reshuffle
    再構成をする
    引数: 0:しない 1:する

## 終了フェイズ

-   discard
    手札を伏せる
    引数: カード id

## メインフェイズ

-   useNomal
    通常札を使う
    引数: カード id
-   useSpecial
    切札を使う
    引数: カード id
-   basicAction
    基本動作をする
    引数: 0:前進 1:離脱 2:後退 3:纏い 4:宿し
    -   chooseCost
        基本動作コストを選択
        引数: カード id, 7:集中力
-   turnEnd
    ターン終了
    引数: なし

## 攻撃された時

-   reactionNomal
    通常札対応
    引数: カード id
-   reactionSpecial
    切札対応
    引数: カード id
-   damageBy
    オーラダメージかライフダメージか選択
    引数: オーラ

## カードの使用時

-   choose
    何らかの選択をする
    引数: 数字

# 変更候補

-   基本動作時にコストから指定する? 済
-   オーラで受けられない際に選択できないように
-   手札が無い場合バグる 「このターン中は全力札を使えない」と出る 済
    -   引数無しと同じ扱い -1(通常札 7 枚目)が使用される
-   再構成直前にデッキ枚数を表示 済
-   札使用済フラグのリセット忘れ 済
    -   リセットしきれていないっぽい?
