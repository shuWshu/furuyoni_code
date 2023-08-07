outputCardList(cardList_U);
outputCardList(cardList_H);
// ----- コードテスト -----
console.log(moveAreaValPoss(distance, dust, 8));
console.log(moveAreaValPoss(distance, dust, 7));
outputBoard();

players_0.moveCardN(1, 1);
players_0.moveCardN(2, 2);
players_0.moveCardN(3, 3);
outputPlayersCard(players_0);
players_0.chgCardS(0);
players_0.chgCardS(1, 0);
players_0.chgCardS(2, 1);
players_0.moveCardN(0, 1);
outputPlayersCard(players_0);
players_0.moveCardN(0, 2);
outputPlayersCard(players_0);
players_0.moveCardN(0, 3);
outputPlayersCard(players_0);
players_0.moveCardN(0, 2);
outputPlayersCard(players_0);
players_0.moveCardN(0, 1);
outputPlayersCard(players_0);
players_0.moveCardN(0, 0);
players_0.chgCardS(0);
outputPlayersCard(players_0);