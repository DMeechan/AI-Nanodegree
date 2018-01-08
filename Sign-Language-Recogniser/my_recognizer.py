import warnings
from asl_data import SinglesData

def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    for test_word, (text_X, test_length) in test_set.get_all_Xlengths().items():
        best_score = float('-inf')
        best_guess = None
        word_likelihoods = {}

        # Iterate through every item and score each test word against them
        for word, model in models.items():
            try:
                score = model.score(text_X, test_length)
            except:
                score = float('-inf')

            # If the guess scored well, store it as the best
            if score > best_score:
                best_score = score
                best_guess = word

            # Store the results for every word in word_likelihoods
            word_likelihoods[word] = score

        guesses.append(best_guess)
        probabilities.append(word_likelihoods)

    return probabilities, guesses

    # Done: implement the recognizer
