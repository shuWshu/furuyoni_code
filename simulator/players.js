// 各プレイヤー紐付け情報
class Players{
    constructor(cardList){
        this.vigor = 0; // 集中力
        this.cardListN = []; // 通常札リスト&所在
        this.cardListS = []; // 切札リスト&使用済
        cardList.forEach((card, i) => {
            if(i < 7){
                this.cardListN.push([card, 0]); // [カード内容, 場所] 山札:0, 手札:1, 捨札:2, 伏札:3
            }else{
                this.cardListS.push([card, 0]); // [カード内容, 使用状況] 未使用:0, 使用済:1
            }
        });
        this.deck = [0, 1, 2, 3, 4, 5, 6]; // 山札順番管理
        this.discard = []; // 捨札&伏せ札の順番管理
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
}

const Players_0 = new Players(cardList_U);
const Players_1 = new Players(cardList_H);