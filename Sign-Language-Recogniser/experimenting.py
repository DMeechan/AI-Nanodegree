import numpy as np
import pandas as pd
from asl_data import AslDb

import warnings
from hmmlearn.hmm import GaussianHMM

import math
from matplotlib import (cm, pyplot as plt, mlab)

# Initialise the database
ASL = AslDb()
DATAFRAME = ASL.df

DATAFRAME['grnd-ry'] = DATAFRAME['right-y'] - DATAFRAME['nose-y']
DATAFRAME['grnd-rx'] = DATAFRAME['right-x'] - DATAFRAME['nose-x']
DATAFRAME['grnd-ly'] = DATAFRAME['left-y'] - DATAFRAME['nose-y']
DATAFRAME['grnd-lx'] = DATAFRAME['left-x'] - DATAFRAME['nose-x']
FEATURES_GROUND = ['grnd-ry', 'grnd-rx', 'grnd-ly', 'grnd-lx']

# Extract the ground features for a single frame
# FRAME_FEATURES_GROUND = [DATAFRAME.ix[98, 1][feature] for feature in FEATURES_GROUND]

# Build a training set
# GROUND_TRAINING = ASL.build_training(FEATURES_GROUND)

# Look at the data for an individual frame
# FRAME_DATA = DATAFRAME.ix[91, 1]

# Find the means grouped by speaker
DF_MEANS = DATAFRAME.groupby('speaker').mean()

# Select a mean that matches by speaker
# DATAFRAME['left-x-mean'] = DATAFRAME['speaker'].map(DF_MEANS['left-x'])

# Find the standard deviation grouped by speaker
DF_STD = DATAFRAME.groupby('speaker').std()

# FIND NORMALIZED CATESIAN COORDINATES
def get_norm():
    features_norm = ['norm-rx', 'norm-ry', 'norm-lx','norm-ly']
    features_pos = ['right-x', 'right-y', 'left-x', 'left-y']

    for index, value in enumerate(features_norm):
        feature = features_pos[index]
        mean = DATAFRAME['speaker'].map(DF_MEANS[feature], na_action=None)
        std = DATAFRAME['speaker'].map(DF_STD[feature], na_action=None)
        z_score = (DATAFRAME[feature] - mean) / std
        DATAFRAME[value] = z_score

# FIND POLAR COORDINATES
def get_polar():
    features_polar = ['polar-rr', 'polar-rtheta', 'polar-lr', 'polar-ltheta']
    features_ground = ['grnd-rx','grnd-ry','grnd-lx','grnd-ly']

    for index, feature in enumerate(features_polar):
        if index % 2 == 1:
            # Index is odd; therefore the feature is for an angle
            x_value = DATAFRAME[features_ground[index - 1]]
            y_value = DATAFRAME[features_ground[index]]
            DATAFRAME[feature] = np.arctan2(x_value, y_value)
        else:
            # Index is even; therefore the feature is for a radius
            x_value = DATAFRAME[features_ground[index]]
            y_value = DATAFRAME[features_ground[index + 1]]
            DATAFRAME[feature] = np.hypot(x_value, y_value)

# FIND DELTA DIFFERENCE 
# TO FIND DIFFERENCE VALUES BETWEEN ONE FRAME AND THE NEXT FRAME AS FEATURES

def get_delta():
    features_delta = ['delta-rx', 'delta-ry', 'delta-lx', 'delta-ly']
    features = ['right-x','right-y','left-x','left-y']

    for index, delta_feature in enumerate(features_delta):
        frame = DATAFRAME[features[index]]
        DATAFRAME[delta_feature] = frame.fillna(0).diff().fillna(0)

def train_a_word(word, num_hidden_states, features):
    
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    training = ASL.build_training(features)  
    X, lengths = training.get_word_Xlengths(word)
    model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(X, lengths)
    logL = model.score(X, lengths)
    return model, logL

def get_word(word, number):
    demoword = word
    model, logL = train_a_word(demoword, number, FEATURES_GROUND)
    print(" => Number of states trained in model for {} is {}".format(demoword, model.n_components))
    print(" => logL = {}".format(logL))
    return model

def show_model_stats(word, model):
    print('Number of states trained in model for {} is {}'.format(word, model.n_components))
    variance = np.array([np.diag(model.covars_[i]) for i in range(model.n_components)])
    for i in range(model.n_components):
        print('hidden state #{}'.format(i))
        print('mean = ', model.means_[i])
        print('variance = ', variance[i])
        print()

def visualize(word, model):
    """ visualize the input model for a particular word """
    variance=np.array([np.diag(model.covars_[i]) for i in range(model.n_components)])
    figures = []
    for parm_idx in range(len(model.means_[0])):
        xmin = int(min(model.means_[:,parm_idx]) - max(variance[:,parm_idx]))
        xmax = int(max(model.means_[:,parm_idx]) + max(variance[:,parm_idx]))
        fig, axs = plt.subplots(model.n_components, sharex=True, sharey=False)
        colours = cm.rainbow(np.linspace(0, 1, model.n_components))
        for i, (ax, colour) in enumerate(zip(axs, colours)):
            x = np.linspace(xmin, xmax, 100)
            mu = model.means_[i,parm_idx]
            sigma = math.sqrt(np.diag(model.covars_[i])[parm_idx])
            ax.plot(x, mlab.normpdf(x, mu, sigma), c=colour)
            ax.set_title("{} feature {} hidden state #{}".format(word, parm_idx, i))

            ax.grid(True)
        figures.append(plt)
    for p in figures:
        p.show()

# Clear terminal screen
print('\n')

# get_norm()
# get_polar()
# get_delta()

word = 'CHOCOLATE'
model = get_word(word, 3)

show_model_stats(word, model)
visualize(word, model)

# Output the results by
# Displaying first five rows of database, indexed by video and frame
HEAD = DATAFRAME.head()

# Display what we've found
# print(HEAD)
# print("Training words: {}".format(GROUND_TRAINING.words))
# print(DF_MEANS)
