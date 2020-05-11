Exercise 13.1

Do the following exercises.

1. Do these exercises from LPN!.
    a. Exercise 3.2

        ANSWER:

        directlyIn(natasha, irina).
        directlyIn(olga, natasha).
        directlyIn(katarina, olga).

        in(X, Y) :- directlyIn(X, Y).
        in(X, Z) :- directlyIn(X,Y), in(Y, Z).

    b. Exercise 4.5

        ANSWER:

        tran(eins,one).
        tran(zwei,two).
        tran(drei,three).
        tran(vier,four).
        tran(fuenf,five).
        tran(sechs,six).
        tran(sieben,seven).
        tran(acht,eight).
        tran(neun,nine).

        listtran([], []).
        listtran([X|Y], [W|Z]) :- tran(X, W), listtran(Y, Z).
        listtran([X|Y], [W|Z]) :- tran(W, X), listtran(Y, Z).

2. Does Prolog implement a version of generalized modus ponens (i.e., modus ponens with variables and instatiation)? If
   so, demonstrate how it’s done; if not, explain why not. If it doesn’t, can you implement one? Why or why not?

Save your program in lab_1.pl.