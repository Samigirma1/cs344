from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# a
grass = BayesNet([
    ('Cloudy', '', 0.5),
    ('Sprinkler', 'Cloudy', 0.1),
    ('Rain', 'Cloudy', 0.8),
    ('WetGrass', 'Sprinkler Rain', {(T, T): 0.99, (T, F): 0.9, (F, T): 0.9, (F, F): 0}),
    ])


# b - - - 8
#