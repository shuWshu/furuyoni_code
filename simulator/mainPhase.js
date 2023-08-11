// メインフェイズ処理
// 引数: プレイヤー
function mainPhase(players){
    // 手札を表示する
    let handText = "手札 ";
    players.cardListN.forEach((element, i) => {
        if(element[1] == 1){ 
            handText += i + ":" + element[0].name + " ";
        }
    });
    handText += "\n";
    console.log(handText);
    let unusedText = "切札 ";
    players.cardListS.forEach((element, i)  => {
        if(element[1] == 0){ 
            unusedText += i + ":" + element[0].name + " ";
        }
    });
    unusedText += "\n";
    console.log(unusedText);
    console.log("集中 \x1b[31m" + players.vigor + "\x1b[0m/2");
    while(true){ // コマンド待ち
        // TODO:選択操作実装
        break;
    }
}