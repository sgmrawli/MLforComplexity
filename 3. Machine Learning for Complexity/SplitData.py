import pandas as pd
import numpy as np

# Set a random seed to show reproducability
RNG_SEED = 42
np.random.seed(seed=RNG_SEED)

df = pd.read_csv('FixedFormula.csv')

X = df['StructuralFormula']
y = df['Total Information Content']

unique_formulae = X.unique()

# Set a random seed to ensure reproducibility across runs
np.random.seed(seed=RNG_SEED)

# Store a list of all unique formulae
all_formulae = unique_formulae.copy()

# Define the proportional size of the dataset split
val_size = 0.2
test_size = 0.2
train_size = 1 - val_size - test_size

# Calculate the number of samples in each dataset split
num_val_samples = int(round(val_size * len(unique_formulae)))
num_test_samples = int(round(test_size * len(unique_formulae)))
num_train_samples = int(round((1 - val_size - test_size) * len(unique_formulae)))

# Randomly choose the formulate for the validation dataset, and remove those from the unique formulae list
val_formulae = np.random.choice(all_formulae, size=num_val_samples, replace=False)
all_formulae = [f for f in all_formulae if f not in val_formulae]

# Randomly choose the formulate for the test dataset, and remove those from the unique formulae list
test_formulae = np.random.choice(all_formulae, size=num_test_samples, replace=False)
all_formulae = [f for f in all_formulae if f not in test_formulae]

# The remaining formulae will be used for the training dataset
train_formulae = all_formulae.copy()

df_train = df[df['StructuralFormula'].isin(train_formulae)]
df_val = df[df['StructuralFormula'].isin(val_formulae)]
df_test = df[df['StructuralFormula'].isin(test_formulae)]

# Double Check
train_formulae = set(df_train['StructuralFormula'].unique())
val_formulae = set(df_val['StructuralFormula'].unique())
test_formulae = set(df_test['StructuralFormula'].unique())

common_formulae1 = train_formulae.intersection(test_formulae)
common_formulae2 = train_formulae.intersection(val_formulae)
common_formulae3 = test_formulae.intersection(val_formulae)

print(f'# of common formulae in intersection 1: {len(common_formulae1)}; common formulae: {common_formulae1}')
print(f'# of common formulae in intersection 2: {len(common_formulae2)}; common formulae: {common_formulae2}')
print(f'# of common formulae in intersection 3: {len(common_formulae3)}; common formulae: {common_formulae3}')

# Write to csv
df_train.to_csv('Data/train.csv', index=False)
df_val.to_csv('Data/val.csv', index=False)
df_test.to_csv('Data/test.csv', index=False)