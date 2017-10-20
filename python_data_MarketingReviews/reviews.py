import os
import cPickle as pickle
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

### set working directory and open file
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

reviews_file = open('CustomerReviews.txt')

raw_data = reviews_file.read()

### clean up data, create column heads, separate data, and output to CSV

raw_lines = raw_data.splitlines()

raw_lines_sep = []
for row in raw_lines:
    if row :
        raw_lines_sep = raw_lines_sep + [row.split(': ')]

def partitions(data_list,n):
    def review_partitions():
        for i in range(0,len(data_list),n):
            yield data_list[i:i+n]
    return [i for i in review_partitions()]
    
partitions_list = partitions(raw_lines_sep,14)

column_heads = [[row[0] for row in partitions_list[0]]]

reviews_rows =  [[col[1] for col in row] for row in partitions_list]

reviews_table = column_heads + reviews_rows

csv_output = open('CustomerReviews.csv','wt')
csv_output.write("\n".join(",".join(row) for row in reviews_table))
csv_output.close()

### Open csv and query data

cust_reviews = pd.read_csv('CustomerReviews.csv')

core_heads = ['ProductModelName','ProductPrice','ReviewRating']

df1 = cust_reviews[core_heads].head()
df2 = cust_reviews[cust_reviews['ReviewRating']>3][core_heads].head()
df3 = cust_reviews[(cust_reviews['ReviewRating']==5) & (cust_reviews['ProductPrice']>1000)][core_heads].head()

byRetailer_count = cust_reviews.RetailerName.value_counts()
byProduct_count = cust_reviews.ProductModelName.value_counts()
byCategory_count = cust_reviews.ProductCategory.value_counts()

ChicagoShoppers = cust_reviews[cust_reviews.RetailerCity=='Chicago']
ChicagoShoppers = ChicagoShoppers.set_index('RetailerName')
ChicagoShoppers = ChicagoShoppers.sort_index()



ChicagoShoppers_by_Price = ChicagoShoppers.ProductPrice.sort_values(ascending=False)
ChicagoShoppers_by_Price_alt = ChicagoShoppers.sort_values(ascending=False, by=['ProductPrice'])
ChicagoShoppers_by_PriceManuf = ChicagoShoppers.sort_values(ascending=[False,True], by=['ProductPrice','ManufacturerName'])

Chicago_Top10 = ChicagoShoppers.set_index('ProductModelName')
Chicago_Top10 = Chicago_Top10.ReviewRating.sort_values(ascending=False)[:10]




ItemsByCity = cust_reviews.groupby('RetailerCity')
for key, group in ItemsByCity:
    print key
    print group

highestPrice_gen = (group.sort_values(by='ProductPrice', ascending=False)[:1] for rtc, group in ItemsByCity)

highestPrice_byCity = pd.DataFrame()

for line in highestPrice_gen:
    highestPrice_byCity = highestPrice_byCity.append(line)

highestPrice_byCity

ItemsByCity['ProductPrice'].median().plot()
plt.show()



TopRating_gen = (group.sort_values(by='ReviewRating', ascending=False)[:5] for rtc, group in ItemsByCity )

highestRating_byCity = pd.DataFrame()
for line in TopRating_gen:
    highestRating_byCity = highestRating_byCity.append(line)

highestRating_byCity


TopRatingPrice_byRetailerCity_gen = (group.sort_values(ascending=[False,False,True],
                                    by=['ReviewRating','ProductPrice','RetailerName'])
                                    [:5]
                                    for rtc, group in ItemsByCity)

TopRatingPrice_byRetailerCity = pd.DataFrame()
for line in TopRatingPrice_byRetailerCity_gen:
    TopRatingPrice_byRetailerCity = TopRatingPrice_byRetailerCity.append(line)

TopRatingPrice_byRetailerCity[['RetailerCity', 'RetailerName', 'ProductModelName', 'ProductPrice', 'ReviewRating']]






###   Final exercises
### R1 Variables

r1_columns = ['RetailerCity', 'RetailerName', 'ProductModelName', 'ReviewRating']

Disliked_byRetailer_gen = (group.sort_values(ascending=[True,True],
                                    by=['ReviewRating','RetailerName'])
                                    [:5]
                                    for rtc, group in ItemsByCity)
Disliked_byRetailer = pd.DataFrame()
for line in Disliked_byRetailer_gen:
    Disliked_byRetailer = Disliked_byRetailer.append(line)

r1 = Disliked_byRetailer[r1_columns].sort_values(ascending=[True,True],by=['RetailerCity','RetailerName'])
r1


### R2 variables WRONG WRONG WRONG

r2_columns = ['RetailerCity', 'RetailerName', 'ProductModelName', 'ProductPrice']

Cheapest_byRetailer_gen = (group.sort_values(ascending=[True,True],
                                    by=['ProductPrice','RetailerName'])
                                    [:5]
                                    for rtc, group in ItemsByCity)
Cheapest_byRetailer = pd.DataFrame()
for line in Cheapest_byRetailer_gen:
    Cheapest_byRetailer = Cheapest_byRetailer.append(line)

r2 = Cheapest_byRetailer[r2_columns].sort_values(ascending=[True,True],by=['RetailerCity','RetailerName'])
r2


### R3 Total Products Reviewed by City (5 Ratings)

Rating_countByCity_gen = (group for rtc, group in ItemsByCity)
                                    
Rating_countByCity = pd.DataFrame()

for line in Rating_countByCity_gen:
    Rating_countByCity = Rating_countByCity.append(line)

r3 = (Rating_countByCity[(Rating_countByCity['ReviewRating']==5)][['ProductModelName', 'RetailerCity', 'ReviewRating']]).RetailerCity.value_counts()
print('''\nTotal number of products reviewed in each city with a 5 rating:''')
r3

### R4

top2_byZip = (Rating_countByCity[(Rating_countByCity['ReviewRating']==5)][['RetailerZipCode', 'RetailerCity', 'ReviewRating']]).RetailerZipCode.value_counts().head(2)
print('''\nTop 2 list of zipcodes where highest number of products got a 5 rating:\n\n''')
top2_byZip


### R5
r5_1 = Rating_countByCity[['RetailerCity','ProductModelName','ReviewRating']]
r5_2 = r5_1.groupby(['ProductModelName','RetailerCity'],as_index=False).size()
r5_2.name = 'No.Reviews'
r5_2 = r5_2.reset_index().sort_values(ascending=False,by='No.Reviews')
r5_2 = r5_2.drop_duplicates(['ProductModelName'])
r5_2 = r5_2.sort_values(ascending=True,by='ProductModelName')

print('''Cities with the most 3+ reviews for each individual product (sorted by product name):''')
r5_2


### Extra Credit Plot

a = cust_reviews.groupby(['ReviewRating','RetailerCity']).size()
a.name = 'No.Reviews'
a = a.reset_index()
a = a.sort_values(ascending=[True,True],by=['RetailerCity','ReviewRating'])
cities = a.RetailerCity.unique()
cities_count = len(cities)

cols        = a.columns
boston      = a[(a['RetailerCity']=='Boston')]
atlanta     = a[(a['RetailerCity']=='Atlanta')]
chicago     = a[(a['RetailerCity']=='Chicago')]
los_angeles = a[(a['RetailerCity']=='Los Angeles')]
san_fran    = a[(a['RetailerCity']=='San Francisco')]
miami       = a[(a['RetailerCity']=='Miami')]
cleveland   = a[(a['RetailerCity']=='Cleveland')]
naperville  = a[(a['RetailerCity']=='Naperville')]


def fill_empty(city,city_string):
        for i in range(1,6):
            if any(city.ReviewRating == i):
                continue
            else:
                df = pd.DataFrame([[i, city_string, 0]], columns=list(cols))
                city = city.append(df).sort_values(ascending=True,by='ReviewRating')
        return(city)
        
boston      = fill_empty(boston,'Boston')
atlanta     = fill_empty(atlanta,'Atlanta')
chicago     = fill_empty(chicago,'Chicago')
los_angeles = fill_empty(los_angeles,'Los Angeles')
san_fran    = fill_empty(san_fran,'San Francisco')
miami       = fill_empty(miami,'Miami')
cleveland   = fill_empty(cleveland,'Cleveland')
naperville  = fill_empty(naperville,'Naperville')

final_frame = boston.append(atlanta).append(chicago).append(los_angeles).append(san_fran).append(miami).append(cleveland).append(naperville)
final_frame = final_frame.sort_values(ascending=[True,False],by=['RetailerCity','ReviewRating'])
 

gf = final_frame.groupby(['RetailerCity','ReviewRating']).sum()


reviewRatingFig_UNSTACKED = gf.unstack(level=-1).plot(kind='bar',stacked=False, title='STACKED Bar Plot',
                            color=['red','orange','purple','yellow','green'], grid=False)
reviewRatingFig_UNSTACKED
plt.legend(title='Rating Levels', labels=['1','2','3','4','5'])
plt.show()



reviewRatingFig_STACKED = gf.unstack(level=-1).plot(kind='bar',stacked=True, title='STACKED Bar Plot',
                        color=['red','orange','purple','yellow','green'],label=range(1,5), grid=False)
reviewRatingFig_STACKED
plt.legend(title='Rating Levels', labels=['1','2','3','4','5'])
plt.show()