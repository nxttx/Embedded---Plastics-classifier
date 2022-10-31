#!/usr/bin/env python
# coding: utf-8

# # EVD3 ML Algortime V1

# In[1]:


import numpy as np
import pandas as pd
import sklearn


# ## Reading and parsing csv file

# In[2]:


df = pd.read_csv ('dataset.csv', index_col=0)


# In[3]:


df.info()


# In[4]:


df.head()


# In[5]:


y = df.loc[:, "0"]
y


# In[6]:


X = df.loc[:, ["1", "2", "3", "4", "5", "6"]]
X


# ## Pre processing pipeline

# In[7]:


from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# In[8]:


# pipe = Pipeline([('scaler', StandardScaler())])


# In[9]:


# X = pipe.fit_transform(X)


# ## Train test split

# In[10]:


# from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split

# In[11]:


# sss =  StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)


# In[12]:


# for train_index, test_index in sss.split(X, y):
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True,stratify=y)
# In[13]:


len(X_train) / len(X)


# ## Model creation

# In[14]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier


# In[15]:


knn_clf = KNeighborsClassifier()
svm_clf = SVC(decision_function_shape='ovo')
random_forest_clf = RandomForestClassifier(random_state=42)
naive_classifier = GaussianNB()
lda_clf = LinearDiscriminantAnalysis()
decision_tree_clf = DecisionTreeClassifier()


# ## Model Validation

# In[16]:


from sklearn.model_selection import cross_val_score


# In[17]:


print(cross_val_score(knn_clf, X_train, y_train, cv=3))


# In[18]:


print(cross_val_score(svm_clf, X_train, y_train, cv=3))


# In[19]:


print(cross_val_score(random_forest_clf, X_train, y_train, cv=3))
print(cross_val_score(naive_classifier, X_train, y_train, cv=3))
print(cross_val_score(lda_clf, X_train, y_train, cv=3))
print(cross_val_score(decision_tree_clf, X_train, y_train, cv=3))


# ## Model selection

# In[20]:


model = random_forest_clf


# In[21]:


model.fit(X_train, y_train)


# In[22]:


print(model.score(X_test, y_test))


# ## Final results

# In[23]:


from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


# In[24]:


y_pred = model.predict(X_test)


# In[25]:


cm = confusion_matrix(y_test, y_pred)


# In[26]:


display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)


# In[27]:


display.plot()
plt.show()


# In[28]:
# Overfitting and underfitting graph

from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(model, X_train, y_train, cv=3, scoring='accuracy', n_jobs=-1, train_sizes=np.linspace(0.01, 1.0, 50))

train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.plot(train_sizes, train_scores_mean, label='Training score', color='black')
plt.plot(train_sizes, test_scores_mean, label='Cross-validation score', color='dimgrey')

plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, color='gray')
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, color='gainsboro')

plt.title('Learning Curve')
plt.xlabel('Training Set Size'), plt.ylabel('Accuracy Score'), plt.legend(loc='best')
plt.tight_layout()
plt.show()


# In[29]:
# export model for later use
import joblib
joblib.dump(model, 'model.pkl')