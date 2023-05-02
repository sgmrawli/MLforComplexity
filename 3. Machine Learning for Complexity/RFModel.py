import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from CBFV.composition import generate_features
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

# Set a random seed to show reproducability
RNG_SEED = 42
np.random.seed(seed=RNG_SEED)

df_train = pd.read_csv('Data/train.csv')
df_val = pd.read_csv('Data/val.csv')
df_test = pd.read_csv('Data/test.csv')

# Beyond this point will need changing if I need to change to a composition based feature vector
df_train = df_train[['Total Information Content', 'StructuralFormula']]
df_val = df_val[['Total Information Content', 'StructuralFormula']]
df_test = df_test[['Total Information Content', 'StructuralFormula']]

# Rename for CBFV use
rename_dict = {'Total Information Content': 'target'}
df_train = df_train.rename(columns=rename_dict)
df_val = df_val.rename(columns=rename_dict)
df_test = df_test.rename(columns=rename_dict)

rename_dict = {'StructuralFormula': 'formula'}
df_train = df_train.rename(columns=rename_dict)
df_val = df_val.rename(columns=rename_dict)
df_test = df_test.rename(columns=rename_dict)    

# Generate CBFVs using mat2vec
X_train_unscaled, y_train, formulae_train, skipped_train = generate_features(df_train, elem_prop='mat2vec', drop_duplicates=False, extend_features=True, sum_feat=True)
X_val_unscaled, y_val, formulae_val, skipped_val = generate_features(df_val, elem_prop='mat2vec', drop_duplicates=False, extend_features=True, sum_feat=True)
X_test_unscaled, y_test, formulae_test, skipped_test = generate_features(df_test, elem_prop='mat2vec', drop_duplicates=False, extend_features=True, sum_feat=True)

print("Generated Data!")

# Scale the inputs using scikit preprocessing modules
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_unscaled)
X_val = scaler.transform(X_val_unscaled)
X_test = scaler.transform(X_test_unscaled)

# Normalise the input data
X_train = normalize(X_train)
X_val = normalize(X_val)
X_test = normalize(X_test)

print("Scaled Data!")

# Import SciKit Modules
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import ExtraTreesRegressor

# Initiliase class and list
Data = []
et = ExtraTreesRegressor()

# Fit using the training data
et.fit(X_train, y_train)

# Calculate metrics for the training set
y_pred = et.predict(X_train)
r2_train = r2_score(y_train, y_pred)
mae_train = mean_absolute_error(y_train, y_pred)
rmse_train = mean_squared_error(y_train, y_pred, squared=False)

# Add to list
Data.append(r2_train)
Data.append(mae_train)
Data.append(rmse_train)

# Calculate metrics for the validation set
y_pred = et.predict(X_val)
r2_val = r2_score(y_val, y_pred)
mae_val = mean_absolute_error(y_val, y_pred)
rmse_val = mean_squared_error(y_val, y_pred, squared=False)
Data.append(r2_val)
Data.append(mae_val)
Data.append(rmse_val)

# Plot the predicted data vs the actual
xymax = np.max([np.max(y_val), np.max(y_pred)])
plot = plt.figure(figsize=(6,6))
plt.plot(y_val, y_pred, 'o', ms = 9, mec='k', mfc='silver', alpha=0.4)
plt.plot([0, xymax], [0,xymax], 'k--', label = 'Ideal')
polyfit = np.polyfit(y_val, y_pred, deg = 1)
regys = np.poly1d(polyfit)(np.unique(y_val))
plt.plot(np.unique(y_val), regys, alpha=0.8, label='Linear Fit')
plt.axis('Scaled')
plt.xlabel('Actual Total Information Content / bits/u.c.')
plt.ylabel('Predicted Total Information Content / bits/u.c.')
plt.title(f'Extra Trees Model, r2 = {r2_val:0.4f}')
plt.legend(loc='upper left')
plt.savefig("PredictionPlot.png")
plt.clf()
print("Extra Trees Done!")

# Histogram of the predictions
mean = np.mean(y_pred)
plt.hist(y_pred, bins='fd', color = 'black')
plt.xlabel('Predicted Complexity')
plt.ylabel('Frequency')
plt.axvline(mean, color = 'red', linestyle = 'dashed', linewidth = 0.75, label = 'Mean '+str('%.2f' %mean))
plt.legend()
plt.show()
plt.savefig("Histogram.png")

print(Data)
