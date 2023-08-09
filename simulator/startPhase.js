// ダメージ処理
// 引数: プレイヤー, 領域(文字列), 値
function damage(players, area, n){
    if(area == "life"){
        return moveAreaValPoss(players[area], players.flare, n);
    }else if(area == "aura"){
        return moveAreaVal(players[area], dust, n);
    }else if(area == "flare"){
        return moveAreaVal(players[area], dust, n);
    }
    return -1;
}

// 開始フェイズ処理
// 引数: 対象プレイヤー, 再構成の有無
function startPhase(players, reshuffle = false){
    // 集中+1
    players.chgVigor(1);
    // 付与札処理
    // TODO:そのうち作る

    // 再構成
    if(reshuffle){
        console.log("再構成");
        damage(players, "life", 1);
        players.reshuffle();
    }
    // カードを2枚引く
    for(let i = 0; i < 2; ++i){
        if(players.draw() == -1){
            console.log("焦燥");
            moveAreaValPoss(players.aura, dust, 1); // TODO:焦燥に置き換え
        }
    }
}