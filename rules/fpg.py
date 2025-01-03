import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pickle

data1 = pd.read_csv('./spotify/2023_spotify_ds1.csv')
# data2 = pd.read_csv('spotify/2023_spotify_ds2.csv')

data = data1
data = data.drop_duplicates()

basket = data.groupby('pid')['track_name'].apply(list).tolist()

basket = [list(set(sublist)) for sublist in basket]

te = TransactionEncoder()
te_ary = te.fit(basket).transform(basket)

df = pd.DataFrame(te_ary, columns=te.columns_)


frequent = fpgrowth(df, min_support=0.05, use_colnames=True)


rules = association_rules(frequent, metric="lift", min_threshold=1.0, num_itemsets=2)

with open('/data/rule1.pkl', 'wb') as file:
            pickle.dump(rules, file)
            print("Rules saved successfully!")
