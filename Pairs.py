import cryptpandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import numpy as np
df1 = cryptpandas.read_encrypted(path="./release_3867.crypt", password='mXTi0PZ5oL731Zqx')
df = df1.dropna()
#Correlation
beta_matrix = np.zeros(shape=(len(df.columns),len(df.columns)))
for i in range(len(df.columns)):
    for j in range(i,len(df.columns)):
        beta_matrix[i][j] = df[df.columns[i]].corr(df[df.columns[j]])
        
flag = [False for col in df.columns]
pairs = []
betas = []
for i in range(len(df.columns)):
    for j in range(i+1,len(df.columns)):
        if abs(beta_matrix[i][j]) > 0.7 and flag[i] == False and flag[j] == False:
            pairs.append(['strat_'+str(i),'strat_'+str(j)])
            betas.append(beta_matrix[i][j])
            flag[i] = True
            flag[j] = True
         
#Test Stationarity
pair_df = pd.DataFrame()
for i,pair in enumerate(pairs):
    pair_df[pair[0]+' '+pair[1]] = df[pair[0]] - betas[i]*df[pair[1]]
    pair_df[pair[0]+' '+pair[1]] = (pair_df[pair[0]+' '+pair[1]] - np.mean(pair_df[pair[0]+' '+pair[1]]))/np.std(pair_df[pair[0]+' '+pair[1]])

ADF = []
new_pairs = []
new_betas = []
p_vals=[]
for i,pair in enumerate(pairs):
    adf_val = adfuller(pair_df[pair[0]+' '+pair[1]])[0]
    p_val = adfuller(pair_df[pair[0]+' '+pair[1]])[1]
    ADF.append(float(adf_val))
    if p_val < 0.05:
        new_pairs.append([pair[0],pair[1]])
        new_betas.append(betas[i])

amt_per_pair = min(1/len(new_pairs),0.1)
proportions = []
for i,pair in enumerate(new_pairs):
    beta = betas[i]
    if beta > 0:
        proportions.append([amt_per_pair/(1+beta),-1*(amt_per_pair*beta)/(1+beta)])
    else:
        proportions.append([amt_per_pair/(1-beta),1*(amt_per_pair*beta)/(1-beta)])

weights = dict(zip(['strat_'+str(i) for i in range(len(df.columns))],[0 for col in df.columns]))
for i,pair in enumerate(new_pairs):
    weights[pair[0]] = proportions[i][0]
    weights[pair[1]] = proportions[i][1]

portfolio = 0
for strat in weights.keys():
    portfolio += df[strat]*weights[strat]

sharpe = np.mean(portfolio)/np.std(portfolio)
print(sharpe)
    

        

