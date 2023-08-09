outputCardList(cardList_U);
outputCardList(cardList_H);
// ----- コードテスト -----
outputBoard();

watchPlayers(players_0, "life", decisionLose);

players_0.moveCardN(1, 1);
players_0.moveCardN(2, 2);
players_0.moveCardN(3, 3);
players_0.moveCardN(4, 3)
outputPlayersCard(players_0);

startPhase(players_0);
outputPlayersCard(players_0);
outputBoard();
startPhase(players_0);
outputPlayersCard(players_0);
outputBoard();
startPhase(players_0, true);
outputPlayersCard(players_0);
outputBoard();