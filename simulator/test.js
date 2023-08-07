outputCardList(cardList_U);
outputCardList(cardList_H);
// ----- コードテスト -----
console.log(moveAreaValPoss(distance, dust, 8));
console.log(moveAreaValPoss(distance, dust, 7));
outputBoard();

outputPlayersCard(players_0);
players_0.moveCard(0, 1);
outputPlayersCard(players_0);
players_0.moveCard(0, 2);
outputPlayersCard(players_0);
players_0.moveCard(0, 3);
outputPlayersCard(players_0);
players_0.moveCard(0, 2);
outputPlayersCard(players_0);
players_0.moveCard(0, 1);
outputPlayersCard(players_0);
players_0.moveCard(0, 0);
outputPlayersCard(players_0);