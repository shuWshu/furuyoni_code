// 終了フェイズ処理
// 引数: 対象プレイヤー
function endPhase(players){
    let handList = [];
    players.cardListN.forEach((element, i) => {
        if(element[1] == 1){ handList.push(i); }
    });

    while(handList.length > 2){ // 手札3枚以上
        let handText = "伏せる札を選択 ";
        let count = 0; // 選択番号
        handList.forEach(id => {
            handText += count + ":" + players.cardListN[id][0].name + " ";
            count += 1;
        });
        handText += "\n";
        console.log(handText);
        
        while(true){ // 選択中止まる
            // TODO:選択操作実装
            let index = 0; // 削除インデックス
            players.moveCardN(handList[index], 3);
            handList.splice(index, 1);
            break;
        }        
    }
}