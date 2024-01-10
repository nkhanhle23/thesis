# Predicting Financial Performance through Forward-Looking Statement Analysis

## Welcome to My Repository

This repository contains the research and implementation for my Master's thesis at HWR Berlin, supervised by Prof. Dr. Diana Hristova and Prof. Dr. Roland Müller.

------

### Abstract
This thesis explores the automation of financial data extraction from SEC Form 10-K reports, focusing on Forward-Looking Statements (FLS) that predict future revenues and earnings. It proposes a structured framework that uses a rule-based approach for extracting financial metric-related sentences, filtering FLS, and identifying predictive models for future performance. This research aims to establish a foundation for an automated NLP model that streamlines data extraction and predictive analysis from 10-Ks, aiding financial investors' decision-making. The findings indicate that a rule-based approach can effectively extract relevant sentences. Moreover, the study compares the effectiveness of FinBERT and DistilBERT in classifying FLS, revealing no significant advantage of one over the other. In performance prediction, Random Forest Regressor (RFR) outperforms FinBERT Regressor (FBR) across various metrics. The analysis also highlights the different textual features deemed important by each model, with trends pointing towards the relevance of company names and FLS-related terms.

------

### Repository Structure

#### Data
The data used in this study is hosted externally and can be accessed through a provided [Google Drive link](https://drive.google.com/drive/folders/1eZ7FoB_PpnJOM5LC0Sd9c1H-ig_c3GFM?usp=drive_link). The data directory is organized as follows:
- **00_raw**: Stores the raw data extracted from the 10-K filings.
- **01_interim**: Contains intermediary data used throughout the analysis.
- **02_processed**: Holds the processed datasets ready for model training and evaluation.
- **03_result_reviews**: Includes data sets for manual review and verification purposes.

#### Models
##### BERT-based models 
The BERT-based models are stored on [my HuggingFace repository] (https://huggingface.co/lenguyen). 

##### Not BERT-based models
The other models are available via a separate [Google Drive link](https://drive.google.com/drive/folders/165aLV5WdMfNTRIe_9_d3o4u0oFAYcOsK?usp=drive_link) and include:
- **finbert-regression**: Contains scalers for post-processing predictions and Shapley values for contextual analysis.
- **random_forest**: Houses trained Random Forest Regressors, each encapsulating a TF-IDF vectorizer and the best estimator from GridSearchCV.


#### Notebooks
This directory hosts Jupyter notebooks for each step of the implementation. Detailed descriptions of the notebooks are included within the thesis document.

------

### User Guide
Before navigating through the notebooks, please ensure that all dependencies are installed using the following command:
```
pip install -r requirements.txt
```
------

### Disclaimer
Many code snippets and methodologies implemented in this repository were developed with the assistance of AI tools such as ChatGPT and GitHub Copilot.

------

### Installation and Setup

To clone the repository and set up the necessary environment:

```bash
git clone [URL to repository]
cd [repository name]
pip install -r requirements.txt
```
Please follow the instructions within the notebooks in numerical order for the best experience.

------

### Contributing
This project is a part of academic research, and while open to suggestions and improvements, it may not be set up for external contributions. For any queries or discussions, please reach out via the contact information provided in the thesis.

------

### Acknowledgements
This work would not have been possible without the support of my academic advisors, the open-source software community, and the financial databases that have been crucial for the research.

------

### Contact
For any additional information or support, please refer to the contact details specified in the thesis document.

