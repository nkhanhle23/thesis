# WELCOME TO MY REPOSITORY 
This is the repository for my Master's thesis at HWR with Prof. Dr. Diana Hristova as my first supervisor, and Prof. Dr. Roland Müller as my second supervisor.

The topic of this thesis is 
    **Predicting Financial Performance through Forward looking statement analysis**

The repository's structure is as follows: 

> data (is uploaded seperately in a Google Drive link)
    > *00_raw*: stores raw data 
    > *01_interim*: stores data of intermediary steps. 
    > *02_processed*: stores official datasets for training and developing models.
    > *03_result reviews*: stores data for manual reviews. 

> models: (is uploaded seperately in a Google Drive link)
    > *finbert-regression*: stores Scalers for post-processing predictions and Shapley values for sample contextual analysis. 
    > *random_forest*: stores trained Random Forest Regressors (RFR). Each RFR is a pipeline of 1) TF-IDF vectorizer and 2) Best estimator of RFR produced by GridSearchCV in the training process. 

> notebooks: stores notebooks for each implemented step (more details can be found in thesis)

**Disclaimer**: many code snippets here are written with the help of AI tools such as ChatGPT and GitHub Copilot.


