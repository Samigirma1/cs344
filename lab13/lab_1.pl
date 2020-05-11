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

        ANSWER:
        Prolog implements a generalized modus ponens.

        Modus ponens deduces the goal by proving that the predicates are true. Prolog, tries to assert the predicates by
        searching the knowledge base for a fact or heads that unify with the predicates. Since variables unify with other
        terms, it can continue this process until if gets to an facts or statements that don''t exist. If the search proves
        that the predicates are true, then it deduces that the goal is true.

        e.g. Using question from Exercise 2

        Prolog:
        on(a, b).
        on(b, c).
        on(Y, X) :- supports(X, Y).

        supports(table, c).

        above(X, Y) :- on(X, Y).
        above(X, Y) :- above(X, Z), above(Z, Y).

        Proving above(a, table):
            1. Prove above(a, Z), above(Z, table):

                above(a, Z) :- above(a, D), above(D, Z).
                    above(a, D) :- on(a, D)
                    unifying on(a, D) = on(a, b), D = b

                    Since D = b...
                    above(b, Z) :- on(b, Z)
                    unifying on(b, Z) = on(b, c), Z = c

                Since Z = c
                above(Z, table) = above(c, table)
                above(c, table) :- on(c, table)

                on(c, table), searches supports (c, table)
                supports(c, table) is a fact. So, it''s proven.

             2. Since the predicates above(a, c), and above(c, table) are true,
                above(a, table) must also be true.
        ___

Save your program in lab_1.pl.