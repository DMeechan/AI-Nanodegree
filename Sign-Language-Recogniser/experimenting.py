import numpy as np
import pandas as pd
from asl_data import AslDb

# Initialise the database
ASL = AslDb()
DATAFRAME = ASL.df

DATAFRAME['grnd-ry'] = DATAFRAME['right-y'] - DATAFRAME['nose-y']
DATAFRAME['grnd-rx'] = DATAFRAME['right-x'] - DATAFRAME['nose-x']
DATAFRAME['grnd-ly'] = DATAFRAME['left-y'] - DATAFRAME['nose-y']
DATAFRAME['grnd-lx'] = DATAFRAME['left-x'] - DATAFRAME['nose-x']
FEATURES_GROUND = ['grnd-ry', 'grnd-rx', 'grnd-ly', 'grnd-lx']

# Extract the ground features for a single frame
FRAME_FEATURES_GROUND = [DATAFRAME.ix[98, 1][feature] for feature in FEATURES_GROUND]

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
# features_norm = ['norm-rx', 'norm-ry', 'norm-lx','norm-ly']
# features_pos = ['right-x', 'right-y', 'left-x', 'left-y']

# for index, value in enumerate(features_norm):
#     feature = features_pos[index]
#     mean = DATAFRAME['speaker'].map(DF_MEANS[feature], na_action=None)
#     std = DATAFRAME['speaker'].map(DF_STD[feature], na_action=None)
#     z_score = (DATAFRAME[feature] - mean) / std
#     DATAFRAME[value] = z_score

# FIND POLAR COORDINATES
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
        
DATAFRAME.head()

# Display first five rows of database, indexed by video and frame
HEAD = DATAFRAME.head()

# Clear terminal screen
# print("\n"*20)
# Display what we've found
print(HEAD)
# print("Training words: {}".format(GROUND_TRAINING.words))
# print(DF_MEANS)
