import pandas as pd 
import json
def normalize(val):
    normalized = float(val/98)
    return normalized

f = open("shudbelikethis.json", "rb")
myfile = f.read()

jsonData=json.loads(myfile)
df = pd.DataFrame(jsonData,index=[0])
df = df.drop(['Unnamed: 0','Death'],axis=1)
df['Age'].iloc[0] = float(normalize(df['Age'].iloc[0]))
df['Age'] = df['Age'].astype('float32')
print(df['Age'].iloc[0])