Read LPN! Chapter 2 and do the following exercises:

From LPN!
Exercise 2.1, questions 1, 2, 8, 9, 14 - Give the necessary instantiations.
    1.  bread = bread
        ANSWER:
            yes
    2.  'Bread' = bread
        ANSWER:
            no
    8.  food(X) = food(bread)
        ANSWER:
            X = bread;
            yes
    9.  food(bread, X) = food(Y, sausage)
        ANSWER:
            Y = bread;
            X = sausage;
            yes
    14. meal(food(bread),X)  =  meal(X,drink(beer))
        ANSWER:
            no
         > X is instantiated to food(bread); when the second argument tries to re-instantiate it too drink(beer), it
           returns no.

Exercise 2.2 - Explain how Prolog does its unification and reasoning. If you have issues getting the results you’d
expect, are there things you can do to game the system? Does inference in propositional logic use unification? Why or
why not?

    ANSWER:
        1. ?-  magic(house_elf). => no;  witch(house_elf), wizard(house_elf), and house_elf(house_elf)) not knowledge base
        5. ?-  wizard(harry). => no;  not in the Knowledge base
        3. ?-  magic(wizard). => no;  witch(wizard), wizard(wizard), and house_elf(wizard)) not knowledge base
        4. ?-  magic(’McGonagall’). => yes; witch('McGongall') is in the knowledge base
        5. ?-  magic(Hermione). => yes; Hermione is a variable and magic(X) is in the knowledge base

    When unifying terms, Prolog compares the the type of "objects" represented by those terms. If terms represent atoms,
    it checks if they are the same. If the terms are complex, it checks if they have the same functors, the same number
    of arguments. and also if the corresponding arguments can be unified.

    When it evaluates a query, it finds a fact or a rule with a head that unifies with the query. If the query unifies
    with a head, it tries to find other facts or head''s of rules that unify with the goals in the in th body og the
    current rule.

Does Prolog inferencing use resolution? Why or why not?