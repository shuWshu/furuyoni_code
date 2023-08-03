// ----- 領域の定義 ----- start
// 各領域クラス
class  Life{
    constructor(){
        this.val = 10;
        this.max = 100;
    }
}
class Aura{
    constructor(){
        this.val = 3;
        this.max = 5;
    }
}
class Flare{
    constructor(){
        this.val = 0;
        this.max = 100;
    }
}
class Distance{
    constructor(){
        this.val = 10;
        this.max = 10;
    }
}
class Dust{
    constructor(){
        this.val = 0;
        this.max = 100;
    }
}
class playersArea{
    constructor(){
        this.life = new Life();
        this.aura = new Aura();
        this.flare = new Flare();
    }
}
// 定義
const distance = new Distance();
const dust = new Dust();
const areaP0 = new playersArea();
const areaP1 = new playersArea();
// 値を変化させる関数
// 返値：成功なら変更後の値，失敗なら-1
function chgAreaVal(area, n){
    area.val += n;
    if(area.val < 0 || area.val > area.max){
        area.val -= n;
        return -1;
    }
    return area.val;
}
// 表示関数
function outputBoard(){
    const output = 
            "P0 ライフ:" + areaP0.life.val +
            "\nP0 オーラ:" + areaP0.aura.val +
            "\nP0 フレア:" + areaP0.flare.val +
            "\nP1 ライフ:" + areaP1.life.val +
            "\nP1 オーラ:" + areaP1.aura.val +
            "\nP1 フレア:" + areaP1.flare.val +
            "\n間合 　　:" + distance.val +
            "\nダスト 　:" + dust.val;
    console.log(output);
}
// ----- 領域定義 ----- end

// -----  -----

// ----- コードテスト -----
console.log(chgAreaVal(areaP0.flare, 6));
console.log(chgAreaVal(distance, -3));
console.log(chgAreaVal(areaP1.aura, 3));
console.log(chgAreaVal(areaP1.life, -11));
outputBoard();