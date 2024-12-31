import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
from fpgrowth_py import fpgrowth

data1 = pd.read_csv('/spotify/2023_spotify_ds1.csv')
data2 = pd.read_csv('/spotify/2023_spotify_ds1.csv')

data = pd.concat([data1, data2])

basket = data[['track_name', 'album_name']].groupby('album_name')['track_name'].apply(list).values.tolist()

#te = TransactionEncoder()
#te_ary = te.fit(basket).transform(basket)

#df = pd.DataFrame(te_ary, columns=te.columns_)

#frequent, rules = fpgrowth(df, min_support=0.001, use_colnames=True)

#print(frequent)

#rules = association_rules(frequent, metric="lift", min_threshold=1.0,  num_itemsets=2)

#print(frequent)
#print(rules)



freqItemSet, rules = fpgrowth(basket, minSupRatio=0.5, minConf=0.7)
print(rules)
