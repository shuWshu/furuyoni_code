// クラス定義
class Card{
    // parameterはカードタイプによって変化
    // 攻撃:[[間合], オーラダメージ, ライフダメージ]
    // 行動:[]
    // 付与:[納]
    constructor(Class, name, num, megami, megamiNo, version, mainType, subType, text, parameter, cost = 0){
        let count = 0
        this.class = Class; //通常:0, 切札:1
        this.name = name; //カード名 string
        this.num = num; //カードナンバー int
        this.megami = megami; //使用メガミ string
        this.megamiNo = megamiNo; //女神ナンバー int
        this.version = version; //メガミバージョン string
        this.mainType = mainType; //メインタイプ 攻撃:0, 行動:1, 付与:2
        this.subType = subType; //サブタイプ 無し:0, 対応:1, 全力:2
        this.text = text; //テキスト string
        if(this.mainType == 0){ //攻撃札のみ
            this.dist = parameter[0]; //適正距離 int[]
            this.auraDamage = parameter[1]; //オーラダメージ int null可能 "-"は-1で表現
            this.lifeDamage = parameter[2]; //ライフダメージ int null可能 "-"は-1で表現
            count += 3;
        }else{
            this.dist = null;
            this.auraDamage = null;
            this.lifeDamage = null;
        }
        if(this.mainType == 2){ //付与札のみ
            this.pay = parameter[0]; //納 int null可能
        }else{
            this.pay = null
        }
        if(this.class == 1){
            this.cost = cost; //フレアコスト int null可能
        }else{
            this.cost = null;
        }
    }
}
// n字インデントを下げる関数
function indentText(text, n) {
    if(!text){ return ""; }
    const lines = text.split('\n');
    const indent = ' '.repeat(n);
    const indentedText = lines.map(line => indent + line).join('\n');
    return indentedText;
}
// カードテキスト用
function indentTextCard(text) {
    if(!text){ return ""; }
    const lines = text.split('\n');
    const indent = " " + "|" + ' ';
    const indentedText = lines.map(line => indent + line).join('\n');
    return indentedText;
}
  
// アウトプット
function outputCard(card, mono = false){
    let cardNo, cardType, paraData;
    cardNo = "NA_" + ('00' + card.megamiNo).slice(-2) + "_" + card.megami + "_" + card.version.toUpperCase() + "_";
    if(card.class == 0){ cardNo += "N_" + card.num; cardType = "\n 通常札"; }
    else if(card.class == 0){ cardNo = "S_" + card.num; cardType = "\n 切札"; }

    if(card.mainType == 0){ 
        if(mono){ cardType += " 攻撃"; }
        else{ cardType += " \x1b[31m攻撃\x1b[0m"; }
        const distMax = Math.max.apply(null, card.dist);
        const distMin = Math.min.apply(null, card.dist); //古めの記法
        paraData = " " + distMin + "-" + distMax + " " + card.auraDamage + "/" + card.lifeDamage;
    }else if(card.mainType == 1){
        if(mono){ cardType += " 行動"; }
        else{ cardType += " \x1b[34m行動\x1b[0m"; }
        paraData = "";
    }else if(card.mainType == 2){
        if(mono){ cardType += " 付与"; }
        else{ cardType += " \x1b[32m付与\x1b[0m"; }
        paraData = " 納:" + card.pay;
    }
    if(card.cost){ paraData += " 消費:" + card.cost; }
    if(card.text && paraData){ paraData += "\n" }

    if(card.subType == 1){ 
        if(mono){ cardType += " 対応"; }
        else{ cardType += " \x1b[35m対応\x1b[0m"; }
    }else if(card.subType == 2){ 
        if(mono){ cardType += " 全力"; }
        else{ cardType += " \x1b[33m全力\x1b[0m"; }
    }

    const output = card.name + " (" + cardNo + ")" +
                   cardType + "\n" +
                   paraData + 
                   indentTextCard(card.text);
    console.log(output);
}

const card_UN1 = new Card(0, "投射", 1, "hajimari", 0, "a", 0, 0, "", [[5, 6, 7, 8, 9], 3, 1]);
const card_UN2 = new Card(0, "脇斬り", 2, "hajimari", 0, "a", 0, 0, "", [[2, 3], 2, 2]);
const card_UN3 = new Card(0, "牽制", 3, "hajimari", 0, "a", 0, 0, "", [[1, 2, 3], 2, 1]);
const card_UN4 = new Card(0, "背中刺し", 4, "hajimari", 0, "a", 0, 0, "", [[1], 3, 2]);
const card_UN5 = new Card(0, "二刀一閃", 5, "hajimari", 0, "a", 0, 2, "", [[2, 3], 4, 2]);
const card_UN6 = new Card(0, "歩法", 6, "hajimari", 0, "a", 1, 0, "集中力を1得る。\n間合 ←1→ ダスト", []);
const card_UN7 = new Card(0, "潜り", 7, "hajimari", 0, "a", 1, 1, "間合 →1→ ダスト", []);
const card_UN8 = new Card(0, "患い", 8, "hajimari", 0, "a", 1, 1, "対応した<攻撃>は-1/+0される。\n相手を萎縮させる。", []);
const card_UN9 = new Card(0, "陰の罠", 9, "hajimari", 0, "a", 2, 0, "隙\n【破棄時】攻撃「適正距離2-3、3/2、対応不可」を行う。", [2]);
const card_US1 = new Card(1, "数多ノ刃", 1, "hajimari", 0, "a", 0, 0, "", [[1, 2], 4, 3], 5);
const card_US2 = new Card(1, "闇凪ノ声", 2, "hajimari", 0, "a", 1, 0, "カードを2枚引く。", [], 4);
const card_US3 = new Card(1, "苦ノ外套", 3, "hajimari", 0, "a", 1, 1, "対応した《攻撃》は-2/+0となる。\n相オーラ →2→ ダスト", [], 3);
const card_US4 = new Card(1, "奪イノ茨", 4, "hajimari", 0, "a", 1, 2, "相手は手札を全て捨て札にし、集中力が0になる。\n再起:ダストが10以上である。", [], 1);
outputCard(card_UN1);
outputCard(card_UN2);
outputCard(card_UN3);
outputCard(card_UN4);
outputCard(card_UN5);
outputCard(card_UN6);
outputCard(card_UN7);
outputCard(card_UN8);
outputCard(card_UN9);
outputCard(card_US1);
outputCard(card_US2);
outputCard(card_US3);
outputCard(card_US4);