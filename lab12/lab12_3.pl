weighsSameAsDuck(SuspectA).
hasTurnedPersonToNewt(b).
isWitch(X) :-
    isWood(X).
isWood(X) :- weighsSameAsDuck(X).
/*The next two rules are not necessary*/
canMakeBridge(X):-
    isWood(X);
    isStone(X).
floats(X) :-
    isWood(X);
    isApple(X);
    isBread(X);
    isSmallStone(X);
    isCider(X);
    isGravy(X);
    isCherry(X);
    isMud(X);
    isChurches(X);
    isLead(X);
    isDuck(X).
burn(X) :- isWitch(X); isWood(X).