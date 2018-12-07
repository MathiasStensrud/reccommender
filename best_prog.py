import pyspark as ps
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.ml.recommendation import ALS
import numpy as np
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae

spark = SparkSession.builder.getOrCreate()


def recommend_user(userId, recs):
    movie_df=pd.read_csv('data/movies/movies.csv')
    temp=recs.loc[recs['userId'] == userId]
    r=np.array(temp.recommendations.all())[:,0]
    temp=[]
    for i in range(len(r)):
        temp.append(movie_df.loc[movie_df['movieId'] == r[i]].title.all())
    r=[]
    return temp

# spark_df=spark.createDataFrame(pd.read_csv('data/movies/ratings.csv'))
movie_df=pd.read_csv('data/movies/movies.csv')
df=pd.read_csv('data/movies/ratings.csv')
df.drop('timestamp',axis=1, inplace=True)
spark_df=spark.createDataFrame(df)
# spark_df=spark_df.filter(spark_df.userId!=468)
pandas_count = spark_df.groupby("movieId").count().toPandas()
pandas_mean = spark_df.groupby("movieId").mean('rating').toPandas()
# temp=recs.loc[recs['userId'] == userId]
bad=pandas_mean.loc[pandas_mean['avg(rating)']==5]
spark_df=spark.createDataFrame(df[~df['movieId'].isin(bad.movieId)])


train, test = spark_df.randomSplit([0.8, 0.2])
als_model = ALS(
    itemCol='movieId',
    userCol='userId',
    ratingCol='rating',
    nonnegative=True,
    regParam=0.15,
    rank=10)
rec=als_model.fit(train)
test=rec.transform(test)
train=rec.transform(train)

test_df=test.toPandas()
train_df=train.toPandas()
test_df.fillna(train_df.prediction.mean(), inplace=True)

rmse=np.sqrt(mse(test_df.rating, test_df.prediction))
m=mae(test_df.rating, test_df.prediction)
print('rmse: ',rmse,' mae: ',m)
spark_df=rec.transform(spark_df)
df=spark_df.toPandas().fillna(train_df.prediction.mean(), inplace=True)
recs=rec.recommendForAllUsers(5).toPandas()
recs.to_csv('static/recs.csv')

print(recommend_user(50, recs))
