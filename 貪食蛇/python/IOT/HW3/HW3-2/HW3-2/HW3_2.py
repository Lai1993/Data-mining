import pymysql as MySQLdb
import pandas as pd
from pandas import DataFrame as df
import numpy as np
from sklearn.linear_model import LogisticRegression as lr

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="iotnbdb")
cursor = db.cursor()
cursor.execute("SELECT * FROM iotnb")
results = cursor.fetchall()
x,y=[],[]
for record in results:
    print("%s,%s,%s"%(record[0],record[1],record[2]))
    x.append(record[1])
    y.append(record[1]>500)
#print(x)
#print(y)
x_np = np.array(x)
y_np = np.array(y)
#print(x_np)
#print(y_np)
x_np = x_np.reshape(-1,1)

clf=lr()
clf.fit(x_np,y_np)
status=clf.predict(500)
#print("state")
#print(status)

tx = np.array(x)
#tx = tx.reshape(-1,1)

ty = clf.predict(tx.reshape(-1,1))
#print(ty)

dictTest={
    "1:value":tx,
    "2:state":ty
}
#print("dicttest")
#print(dictTest)

dataOut=pd.DataFrame(dictTest)
#print("dataoutput")
print(dataOut)
