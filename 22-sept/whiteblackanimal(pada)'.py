import numpy as np
import pandas as pd



info={
    "name": ["abhay","girish","priyanka","girishEx"],
    "age": [20,23,27,29],
    "course":["aiml", "cse", "blockchain", "cybersecurity"],
    "marks": [32,81,91,100]
}

dp=pd.DataFrame(info)
print(dp)
print(dp["name"])
print(dp[["name","course"]])
print(dp.iloc[0])
print(dp.loc[2, "marks"])

high_scorers=dp[dp["marks"] > 80]
print("high scorers: ",high_scorers)

dp["res"]=np.where(dp["marks"] >=80, "pass","fail")

dp.loc[dp["name"]=="priyanka", "marks"]= 95
print(dp)
