"""
========================================
Example: skhubness in Pipelines
========================================

Estimators from scikit-hubness can - of course - be used in a scikit-learn ``Pipeline``.
In this example, we select the best hubness reduction method and several other
hyperparameters in grid search w.r.t. to classification performance.
"""
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from skhubness.neighbors import KNeighborsClassifier

# Not so high-dimensional data
X, y = make_classification(n_samples=1_000,
                           n_features=50,
                           n_informative=20,
                           n_classes=2,
                           random_state=3453)

X, X_test, y, y_test = train_test_split(X, y,
                                        test_size=100,
                                        stratify=y,
                                        shuffle=True,
                                        random_state=124)

# Pipeline of standardization, dimensionality reduction, and kNN classification
pipe = Pipeline([('scale', StandardScaler(with_mean=True, with_std=True)),
                 ('pca', PCA(n_components=20, random_state=1213)),
                 ('knn', KNeighborsClassifier(n_neighbors=10, algorithm='lsh', hubness='mp'))])

# Exhaustive search for best algorithms and hyperparameters
param_grid = {'pca__n_components': [10, 20, 30],
              'knn__n_neighbors': [5, 10, 20],
              'knn__algorithm': ['auto', 'hnsw', 'lsh', 'falconn_lsh', 'nng', 'rptree'],
              'knn__hubness': [None, 'mp', 'ls', 'dsl']}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=1354)
search = GridSearchCV(pipe, param_grid, n_jobs=5, cv=cv, verbose=1)
search.fit(X, y)

# Performance on hold-out data
acc = search.score(y_test, y_test)
print(acc)
# 0.79

print(search.best_params_)
# {'knn__algorithm': 'auto',
#  'knn__hubness': 'dsl',
#  'knn__n_neighbors': 20,
#  'pca__n_components': 30}
