// 各プレイヤー紐付け情報
class Players{
    constructor(life, aura, flare){
        this.vigor = 0; // 集中力
        this.cardListN = []; // 通常札リスト&所在
        this.cardListS = []; // 切札リスト&使用済
        this.deck = [0, 1, 2, 3, 4, 5, 6]; // 山札順番管理
        this.discard = []; // 捨札&伏せ札の順番管理
        this.life = life;
        this.aura = aura;
        this.flare = flare;
    }
    // カードリストの登録
    setCardList(cardList){
        this.cardListN = []; // リセット
        this.cardListS = []; // リセット
        cardList.forEach((card, i) => {
            if(i < 7){
                this.cardListN.push([card, 0]); // [カード内容, 場所] 山札:0, 手札:1, 捨札:2, 伏札:3, 付与札:4
            }else{
                this.cardListS.push([card, 0]); // [カード内容, 使用状況] 未使用:0, 使用済:1
            }
        });
    }
    // 集中力増減
    // 返値: 成功なら変更後値, 失敗なら-1を返す．
    chgVigor(n){ 
        this.vigor += n;
        if(this.vigor > 2 || this.vigor < 0){
            this.vigor -= n;
            return -1; 
        }
        return this.vigor;
    }
    // 再構成
    reshuffle(){
        this.cardListN.forEach((element, i) => {
            if(element[1] == 2 || element[1] == 3){ // 捨札伏札にある
                element[1] = 0;
                this.deck.push(i);
            }
        });
        this.discard = [];
        shuffleArray(this.deck);
    }
    // カードの移動
    // 引数: カードid, 移動後
    moveCardN(id, area){
        const prevArea = this.cardListN[id][1];
        // 移動前
        if(prevArea == 0){ // 山札
            const index = this.deck.indexOf(id);
            this.deck.splice(index, 1);
        }else if(prevArea == 2 || prevArea == 3){ // 捨伏札にある
            const index = this.discard.indexOf(id);
            this.discard.splice(index, 1);
        }
        // 移動後
        if(area == 0){ // 山札
            this.deck.push(id);
        }else if(area == 2 || area == 3){ // 捨伏札にある
            this.discard.push(id);
        }
        this.cardListN[id][1] = area;
    }
    // 切札状態変更
    // 引数: カードid, 状態
    chgCardS(id, state = -1){
        if(state == -1){ this.cardListS[id][1] = (this.cardListS[id][1] + 1) % 2; }
        else{ this.cardListS[id][1] = state; }
    }
}
// シャッフル関数
function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}
// 各領域カード表示
function outputPlayersCard(players, player_name = ""){
    let deckText = "山札(上　下): ";
    players.deck.forEach(id => {
        deckText += players.cardListN[id][0].name + ", "
    });
    deckText += "\n";

    let handText = "手札(順序無): ";
    players.cardListN.forEach(element => {
        if(element[1] == 1){ handText += element[0].name + ", "; }
    });
    handText += "\n";

    let discText = "捨札(先　後): ";
    let laidText = "伏札(順序無): ";
    players.discard.forEach(id => {
        if(players.cardListN[id][1] == 2){ discText += players.cardListN[id][0].name + ", "}
        else{ laidText += players.cardListN[id][0].name + ", " }
    });
    discText += "\n";
    laidText += "\n";
    
    let unusedText = "切札(未使用): ";
    let usedText = "切札(使用済): "
    players.cardListS.forEach(element => {
        if(element[1] == 0){ unusedText += element[0].name + ", ";}
        else{ usedText += element[0].name + ", "; }
    })
    unusedText += "\n";
    usedText += "\n";

    let nameText = "";
    if(player_name){ nameText += player_name + "\n"; }
    output = nameText + deckText + handText + discText + laidText + unusedText + usedText;
    console.log(output);
}
// 各プレイヤーカード表示
function outputBothCard(){
    outputPlayersCard(players_0, "プレイヤー0");
    outputPlayersCard(players_1, "プレイヤー1");
}

const players_0 = new Players(life_0, aura_0, flare_0);
players_0.setCardList(cardList_U);
const players_1 = new Players(life_1, aura_1, flare_1);
players_1.setCardList(cardList_H)