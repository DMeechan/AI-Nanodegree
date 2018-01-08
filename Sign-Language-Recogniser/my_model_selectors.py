import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences

# Hide divide by zero error
np.seterr(divide='ignore')


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: 
    
    BIC = -2 * log L + p * log N
    => L = likeihood of fitted model
    => p = number of free parameters in model (complexity)
    => p * log N = penalty term (higher p = higher penalty, to reduce complexity & avoid overfitting)
    => N = number of data points // size of data set

    Equation becomes:
    score = -2 * log (likelihood) + num free parameters * log (num data points)

    Lower score = better model

    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        lowest_score = float('inf')
        best_model = None

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(num_states)
                log_likelihood = model.score(self.X, self.lengths)

                # N = number of data points; f = number of features
                N, f = self.X.shape
                log_n = np.log(N)
                # N = len(self.X)

                # Number of free parameters: p = m^2 + 2mf-1
                p = (num_states ** 2) + 2 * num_states * f - 1

                score = -2 * log_likelihood + p * log_n

                if score < lowest_score:
                    lowest_score = score
                    best_model = model

            except Exception as e:
                print('Hit an exception. We shall venture forth into the unknown: ', e)
                pass

        if best_model:
            return best_model
        else:
            return self.base_model(self.n_constant)

        # DONE: implement model selection based on BIC scores


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf


    DIC = log (P (X(i) ) - 1 / (M - 1) * SUM (log (P (X (all but i))
    => log (P (our word)) - average (log (P (every other word)))
    => log likelihood of the data belonging to the model - average of anti log likelihood of data and model

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        highest_score = float('-inf')
        best_model = None

        try:
            for num_states in range(self.min_n_components, self.max_n_components + 1):
                model = self.base_model(num_states)

                # Get model scores:
                # Iterate through each word and append their scores
                # If they're not the word we're checking against now
                scores = []
                for word, (X, lengths) in self.hwords.items():
                    if word != self.this_word:
                        scores.append(model.score(X, lengths))

                # score = model score for our word  - average of log likelihood of every other word
                score = model.score(self.X, self.lengths) - np.mean(scores)

                # Filter through to get the model with the best score
                if score > highest_score:
                    highest_score = score
                    best_model = model

            return best_model

        except Exception as e:
            print('Hit an exception. Abandon ship: ', e)
            return self.base_model(self.n_constant)

        # DONE: implement model selection based on DIC scores
        

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation (CV) folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        num_splits = 3
        kf = KFold(n_splits = num_splits, shuffle = False, random_state = None)

        highest_score = float("-inf")
        best_model = None

        for state_num in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(state_num)
                scores = []

                # Iterate through separating sequences into folds
                # So folds can be rotated out of the training set and tested
                # By scoring for corss-validation
                for training_index, test_index in kf.split(self.sequences):
                    # Recombine training sequences after being split with KFold
                    self.X, self.lengths = combine_sequences(training_index, self.sequences)
                    # # Recombine test sequences after being split with KFold
                    X, lengths = combine_sequences(test_index, self.sequences)

                    training_model = self.base_model(state_num)
                    scores.append(training_model.score(X, lengths))
                
                score = np.mean(scores)

                if (score > highest_score):
                    highest_score = score
                    best_model = model

            except Exception as e:
                print('Hit an exception. We shall venture forth into the unknown: ', e)
                pass

        if best_model:
            return best_model
        else:
            return self.base_model(self.n_constant)

        # DONE: implement model selection using CV
