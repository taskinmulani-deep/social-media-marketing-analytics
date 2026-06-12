#import pandas as pd

#df1 = pd.read_csv('data/raw/social_media_engagement.csv')
#df2 = pd.read_csv('data/raw/social_media_advertising.csv')
#df3 = pd.read_csv('data/raw/marketing_campaign_perf.csv')

# Explore each
#print("Dataset 1:", df1.shape, "\nColumns:", df1.columns.tolist())
#print("Dataset 2:", df2.shape, "\nColumns:", df2.columns.tolist())
#print("Dataset 3:", df3.shape, "\nColumns:", df3.columns.tolist())


import pandas as pd

df1 = pd.read_csv('data/raw/social_media_engagement.csv')
df2 = pd.read_csv('data/raw/social_media_advertising.csv')
df3 = pd.read_csv('data/raw/marketing_campaign_perf.csv')

print("=== Dataset 1 ===")
print(df1.shape)
print(df1.columns.tolist())
print(df1.head(2))

print("\n=== Dataset 2 ===")
print(df2.shape)
print(df2.columns.tolist())
print(df2.head(2))

print("\n=== Dataset 3 ===")
print(df3.shape)
print(df3.columns.tolist())
print(df3.head(2))