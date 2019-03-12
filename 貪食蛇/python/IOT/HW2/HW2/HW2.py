import pandas as pd
from pandas import DataFrame as df
import numpy as np
from sklearn.linear_model import LogisticRegression as lr
FILE = "D:\\test.csv"
data = pd.read_csv(FILE)
x = np.array(data["value"])
y = np.array(data["state"])

print(x)
print(y)
x = x.reshape(-1,1)

clf=lr()
clf.fit(x,y)
status=clf.predict(300)
print(status)

data = pd.read_csv(FILE)

tx = np.array(data["value"])
#tx = tx.reshape(-1,1)

ty = clf.predict(tx.reshape(-1,1))
print(ty)
print(type(ty))

dictTest={
    "value":tx,
    "state":ty
}
print(dictTest)
print(type(dictTest))

dataOut=pd.DataFrame(dictTest)
print(dataOut)

dataOut.to_csv("D:\\training.csv")