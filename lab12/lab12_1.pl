Read LPN! Chapter 1 and do the following exercises:

1. From LPN!
    a. Exercise 1.4 - Explain why you built the representations as you did.

    ANSWER:
        > The first three tasks are facts. So, they can be represented by using a functor and atoms for
        the names of the person.

        > For "Marsellus kills everyone who gives Mia a footmassage.":
            -  "everyone" should be represented using a variable.
            -  The statement can be interpreted as "If X gave Mia a footmassage, then Marsellius will kill X."
               So, "Marsellus kills everyone" is the head, and "...gives Mia a footmassage" is the body.

        > For "Mia loves everyone who is a good dancer.":
            -  "everyone" should be represented using a variable.
            -  The statement can be interpreted as "If X is a good dance, Mia loves X."
               So, "Mia loves X" is the head, and "...is a good dancer is the body" is the body.

        > For "Jules eats anything that is nutritious or tasty.":
            -  "anything" should be represented using a variable.
            -  The statement can be interpreted as "If X is nutritious and X is tasty, jules eats X."
               So, "jules eats X" is the head, and "...is nutritious or tasty" is the body.

        Representation built:
            killer(butch).
            married(mia, marsellius).
            dead(zed).
            kills(marsellius, X):- footMassage(X, mia).
            loves(mia, X):- goodDancer(X).
            eats(jules, X):- nutritious(X); tasty(X).

    b. Exercise 1.5 - Explain how Prolog comes up with its answers.
        ANSWER:
          It searches its knowledge base for a fact that answers the query. Otherwise, it looks for a rule that answers
          the query, then it checks if the body is satisfiable. If the body is satisfiable, it then returns the values that
          satisfy the query.

          e.g.
            For wizard(ron) - the knowledge base has the fact. So, it''s returns true or yes.
            For witch(ron) - not represented in the knowledge base. So, it returns false or no.
            For wizard(hermoine) - check hasBroom(hermoine) and hasWand(hermoine)
                for hasBroom: check quidditchPlayer(hermone). Since quidditchPlayer(hermone) is not in the knowledge,
                    it returns false or no.

2. Consider the well-known modus ponens. Does Prolog implement a version of modus ponens in propositional logic form?
If so, demonstrate how it’s done; if not, explain why not. If it doesn’t, can you implement one? Why or why not?

    ANSWER: If the body of a rule can be deduced to be true using the knowledge base, then it will deduce that the head must
        also be true.

3. Prolog supports representations in the form of Horn clauses. Compare and contrast the representational power they
provide with that of propositional logic.

    ANSWER: Propositional logic statements and Horn clauses are equivalent. A statement in propositional logic has the
          format (a ∧ b ∧ c ∧ ...) ⇒ q.

            - Since p ⇒ q ≡ ¬p v q, ((a ∧ b ∧ c ∧ ...) ⇒ q) ≡ ¬(a ∧ b ∧ c ∧ ...) v q.
            - Using DeMorgan''s law, ¬(a ∧ b ∧ c ∧ ...) v q ≡ ¬a V ¬b V ¬b V ... v q, which is in Horn clause form.

4. Logical implementations generally distinguish the basic operations of TELL and ASK. Does Prolog support this
distinction? If so, how; if not, why not?

    ANSWER:
        Prolog represents "TELL" using facts and "ASK" using rules.