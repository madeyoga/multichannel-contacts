import pandas as pd
from sklearn.metrics import accuracy_score

subm1 = pd.read_csv("submission.csv")
subm2 = pd.read_csv("submission-3.csv")

subm2 = subm2.loc[(subm2.index < 13027)]

print(subm1.shape)
print(subm2.shape)


a = subm1["ticket_trace/contact"].values
b = subm2["ticket_trace/contact"].values

print(accuracy_score(a, b))

##mse = mean_squared_error()
