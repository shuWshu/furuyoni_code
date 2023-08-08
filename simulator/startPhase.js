// 開始フェイズ処理
function startPhase(players, reshuffle = false){
    // 集中+1
    players.chgVigor(1);
    // 付与札処理
    // TODO:そのうち作る

    // 再構成
    if(reshuffle){
        console.log("再構成");
        moveAreaValPoss(players.life, players.flare, 1); // TODO:ダメージに置き換え
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