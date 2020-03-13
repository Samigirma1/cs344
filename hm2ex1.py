import pprint

prettier = pprint.PrettyPrinter()

probTable = dict()

spam_corpus = [["I", "am", "spam", "spam", "I", "am"], ["I", "do", "not", "like", "that", "spamiam"]]
ham_corpus = [["do", "i", "like", "green", "eggs", "and", "ham"], ["i", "do"]]

def spamFilter(spam, ham):
    wordStats = dict()

    # count word in spam
    for document in spam:
        for word in document:
            if word in wordStats.keys():
                wordStats[word]["spam"] += 1
            else:
                wordStats[word] = {"spam": 1, "ham": 0}

    # count word in ham
    for document in ham:
        for word in document:
            if word in wordStats.keys():
                wordStats[word]["ham"] += 1
            else:
                wordStats[word] = {"ham": 1, "spam": 0}

    # calculate the probabilities
    returnContainer = dict()

    for word in wordStats:
        if wordStats[word]["spam"] + wordStats[word]["ham"] > 1:
            statSpam = 1 if wordStats[word]["spam"] / len(spam) > 1 else wordStats[word]["spam"] / len(spam)
            statHam = 1 if 2*wordStats[word]["ham"]/len(ham) > 1 else 2*wordStats[word]["ham"]/len(ham)
            prob = statSpam / (statHam + statSpam)

            returnContainer[word] = (prob if prob > 0.01 else 0.01) if prob < 0.99 else 0.99


    return returnContainer

prettier.pprint(spamFilter(spam_corpus, ham_corpus))