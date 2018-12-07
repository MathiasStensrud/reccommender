import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pyspark as ps
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae

def als_func(spark_df, train, test):
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
    recs.to_csv('recs.csv')

    test_df=test.toPandas()
    train_df=train.toPandas()
    test_df.fillna(train_df.prediction.mean(), inplace=True)

    return rec, recs, test_df, train_df

def recommend_user(df, userId, recs):

    temp=recs.loc[recs['userId'] == userId]
    r=np.array(temp.recommendations.all())[:,0]
    temp=[]
    for i in range(len(r)):
       temp.append(df.loc[df['movieId'] == r[i]].title.all())
    r=[]
    return temp

def violin_plot(df):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(6,6))

    axes[0].violinplot(df['rating'], points=20, widths=0.3,
                        showmeans=True, showextrema=True, showmedians=True)
    axes[0].set_title("Ratings", fontsize=10)

    axes[1].violinplot(df['prediction'], points=20, widths=0.3,
                        showmeans=True, showextrema=True, showmedians=True)
    axes[1].set_title("Predictions", fontsize=10)
    plt.savefig('images/violin_plot2.png')

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()

    movie_df=pd.read_csv('data/movies/movies.csv')
    df_movies =pd.read_csv('data/movies/movies.csv')
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

    recommender, recs, test_df, train_df = als_func(spark_df, train, test)
    rec_users = recommend_user(df_movies, 471, recs)
    violin_plot(test_df)

    print(rec_users)
