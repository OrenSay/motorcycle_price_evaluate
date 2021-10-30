# -*- coding: utf-8 -*-
"""

@author: orens
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
df = pd.read_csv('moto_cleaned_371.csv')

print(df.columns)

df_model = df[['categorty', 'hand', 'km_fix', 'price_fix', 'year', 'maker', 'model', 'region', 'size']]
df_dum = pd.get_dummies(df_model)
# %%
from sklearn.model_selection import train_test_split

X = df_dum.drop('price_fix', axis=1)
y = df_dum.price_fix.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# %%
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

# %%
# linear regrassion model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
print(lr_model.score(X_test, y_test))

print(np.mean(cross_val_score(lr_model, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')))
# %%
# lasso model defult alpha ==1
las_model = Lasso()
las_model.fit(X_train, y_train)
print(las_model.score(X_test, y_test))
print(np.mean(cross_val_score(las_model, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')))

alpha = []
error = []
# improve lasso model by changing alpha values
for i in range(1, 120):
    alpha.append(i)
    lasModel = Lasso(alpha=(i))
    error.append(np.mean(cross_val_score(lasModel, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')))

plt.plot(alpha, error)

df_err = pd.DataFrame({'alpha': alpha, 'error': error})
print(df_err[df_err.error == max(df_err.error)])
# %%
lass_model = Lasso(alpha=19)
lass_model.fit(X_train, y_train)
print(np.mean(cross_val_score(lass_model, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')))
# %%
# random forest regressor model
from sklearn.ensemble import RandomForestRegressor

regr_model = RandomForestRegressor()
print(np.mean(cross_val_score(regr_model, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')))

regr_model.fit(X_train, y_train)

print(regr_model.score(X_test, y_test))

# %%
# Grid search CV
from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators': range(10, 300, 10), 'criterion': ('mse', 'mae'), 'max_features': ('auto', 'sqrt', 'log2')}
gs = GridSearchCV(regr_model, parameters, scoring='neg_mean_absolute_percentage_error')
gs.fit(X_train, y_train)
# %%
print(gs.best_score_)
print(gs.best_estimator_)

# %%print results
from sklearn.metrics import mean_absolute_error

print('price mean')
print(df.price_fix.mean())
print('linear regrassion model')
tepred_lr = lr_model.predict(X_test)
print(mean_absolute_error(y_test, tepred_lr))
print('lasso model')
tepred_las = las_model.predict(X_test)
print(mean_absolute_error(y_test, tepred_las))
print('improved lasso model')
tepred_lass = lass_model.predict(X_test)
print(mean_absolute_error(y_test, tepred_lass))
print('random forest regressor model')
tepred_rg = regr_model.predict(X_test)
print(mean_absolute_error(y_test, tepred_rg))
print('improved random forest regressor model')
tepred_rgr = gs.best_estimator_.predict(X_test)
print(mean_absolute_error(y_test, tepred_rgr))

