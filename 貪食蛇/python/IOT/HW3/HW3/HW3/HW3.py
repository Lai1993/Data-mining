from sklearn import datasets as dset

#1 load data and convert it to nparray
iris = dset.load_iris()
x = iris.data
y = iris.target
print(x)
print(y)
print(x.shape,y.shape)
print(type(x))

#2 build model
from sklearn.linear_model import LogisticRegression as LR

model = LR()
model.fit(x,y)
print(model)
ans = model.predict(x)
print(ans)
score = model.score(x,y)
print(x[ans!=y])
print([x.tolist().index(x[ans!=y][i].tolist()) for i in range(len(x[ans!=y]))])
print(x[:5,:2])
print(score)

from sklearn.cross_validation import train_test_split as ttsplit
x_train, x_test, y_train, y_test = ttsplit(x,y,test_size = 0.20, random_state = 33)

model2 = LR()
model2.fit(x_train,y_train)
ansTrain = model.score(x_train,y_train)
ansTest = model.score(x_test,y_test)
print("ansTrain=",ansTrain)
print("ansTest=",ansTest)

from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold,cross_val_score
cv = KFold(x.shape[0],n_folds=5,shuffle=True,random_state = 33)

model3 = Pipeline([('scaler',StanderdScaler()),
                   ('linear_model',LR())])