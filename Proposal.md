# Alt Recommender Case Study

##### Our Goal:
Our goal is to improve the performance of our recommender to increase overall revenue.
We believe we can improve our recommender using collaborative filtering, in which the system predicts user interests using a collection of preferences from many users and compares either users to each other or items to each other. This would replace our current recommender using the mean of means.
Below is a visual for collaborative filtering.

<p align="center">
  <img width="350" height="350" src="images/Collaborative_filtering.gif">
</p>

##### Our model:
We are using an item-item collaborative filtering (comparing similarities between movie's ratings per user) since we have more users than movies in order to increase computation speeds. We use an Alternating Least Squares (ALS) model to fit our data and find similarities between movie ratings. Our model doesn't take into account movies with an average score of 5.0 since movies with a perfect score are likely not to have enough ratings to accurately reflect the preferences of the user.

<p align="center">
  <img width="350" height="350" src="images/violin_plot2.png">
</p>

Our model shows a 11.8% improvement in performance over our previous model.

For our prototype we have our recommender deployed on a flask app.

##### Sample Recommendations:

| User ID |                                                                                                      Movie Recommendation                                                                                                     |
|:-------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    50   | ’Love Is a Many-Splendored Thing (1955)’, “Rory O’Shea Was Here (Inside I’m Dancing) (2004)“, ‘Dear Zachary: A Letter to a Son About His Father (2008)’, ‘Fawlty Towers (1975-1979)’, ‘Gigantic (A Tale of Two Johns) (2002)’ |
|   333   |    'Rory O’Shea Was Here (Inside I’m Dancing) (2004)', ‘Dear Frankie (2004)’, ‘Love Is a Many-Splendored Thing (1955)’, ‘Dear Zachary: A Letter to a Son About His Father (2008)’, ‘Apollo 13: To the Edge and Back (1994)’   |
|   500   |                     ‘Angus, Thongs and Perfect Snogging (2008)’, ‘Pride and Prejudice (1995)’, ‘Dear Zachary: A Letter to a Son About His Father (2008)’, ‘Young Victoria, The (2009)’, ‘Penelope (2006)’                     |

##### Recommended Next Steps:
Our next recommendation would be to perform an AB test with a 95% confidence level (based on industry standards) to compare the new collaborative filtering recommender to the mean of means recommender on actual users. For the AB test, we could deploy our new recommender through our app to half of our users for testing while our current recommender will stay active for the other half. We could then measure how well our recommender is perceived through different metrics. These metrics could include how long a user stays on the site, how many times they relaunch the recommender, or even by having a single rating option after each launch asking "was this helpful".
