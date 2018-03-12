  ### toxic_tweets 

Computer Science with Applications 2 Project
Team: Rose Gao, Andrea Koch, Ian Lyons


Project Objective: Detect toxicity, insult, obscenity, and identity hate in tweets. 
Visualize and track trends of toxicity for topics (e.g. abortion) and towards individuals (e.g. Clinton) throughout 2016-2018.


OVERALL STRUCTURE:
1) TwitterScraper:
  - User provides query (query_term, search dates, output filename)
  - Query tweets and export as a CSV
2) Classifier:
  - Read in the CSV as a pandas dataframe
  - Vectorize the text in each tweet
  - Use the 6 toxic models to identify levels of toxicity (Toxic, Severe Toxic, 
    Obscene, Threat, Insult, Identity Hate)
3) Visualization:
  - Create graphs and pull them into a dashboard


INSTRUCTIONS:
1) 


How to install required libraries that you many not already have: 
  TwitterScraper:
    from the command line, run:  pip install twitterscraper
  Sklearn:
    from the command line, run:  pip install -U scikit-learn
  NLTK:
    For Mac/Unix:
      from the command line, run:  sudo pip install -U nltk
    For Windows:
      from the command line, run:  pip install nltk
  Plotly:
    from the command line, run:  pip install plotly


USED LIBRARIES:
  pandas
  datetime
  csv
  sys
  pickle
  NLTK
  sklearn
  scipy
  TwitterScraper
  seaborn
  plotly
  matplotlib.pyplot
  ipython.display





Main Folders:
1. archive: includes old project (fake news tweets detection), temporary Jupyter notebooks, 
and scraped and classified data that we did not use for trends/visuals.

2. toxic: includes final project
- Folders:
  - classified_tweets: stores classified tweets (CSV files) -- Andrea Koch
  - demo: self-contained demo -- Rose Gao (combination of code from all files by Rose, Ian, Andrea)
    - read demo/Demo_README.md for command line arguments
  - kaggle_data: stores data downloaded from Kaggle's toxic comment classification competition
  - scraped_tweets: stores scraped tweets (CSV files)
  - toxicity_models: stores pickled models for vectorizers and logistic regression models
  - visuals: stores visualizations created in plotly and edited in Inkscape
- Files:
  - Toxic Comment Data EDA.ipynb: toxic comment dataset exploratory data analysis
  - Toxic Tweets.pdf: final presentation (PDF)
  - build_toxicity_models.py: builds vectorizers and toxicity models
  - classify_tweets.py: given a scraped tweets CSV file, outputs a classified tweets CSV file
      - to run in command line: "python classify_tweets.py <scraped tweets csv> <output classfied tweets csv filename>"
  - query.py: scrapes tweets given a query term and outputs a scraped tweets CSV file

All code was original code.
See note in build_toxicity_models.py regarding code adapted from sklearn documentation.
