### toxic_tweets 

Computer Science with Applications 2 Project
Team: Rose Gao, Andrea Koch, Ian Lyons

Project Objective: Detect toxicity, insult, obscenity, and identity hate in tweets. 
Visualize and track trends of toxicity for topics (e.g. abortion) and towards individuals (e.g. Clinton) throughout 2016-2018.

Main Folders:
1. archive: includes old project (fake news tweets detection), temporary Jupyter notebooks, 
and scraped and classified data that we did not use for trends/visuals.

2. toxic: includes final project
- Folders:
  - classified_tweets: stores classified tweets (CSV files)
  - demo: self-contained demo
    - read demo/Demo_README.md for command line arguments
  - kaggle_data: stores data downloaded from Kaggle's toxic comment classification competition
  - scraped_tweets: stores scraped tweets (CSV files)
  - toxicity_models: stores pickled models for vectorizers and logistic regression models
  - visuals: stores visualizations created in plotly and edited in Inkscape
- Files:
  - Toxic Comment Data EDA.ipynb: toxic comment dataset exploratory data analysis
  - Toxic Tweets.pdf: final presentation (PowerPoint)
  - build_toxicity_models.py: builds vectorizers and toxicity models
  - classify_tweets.py: given a scraped tweets CSV file, outputs a classified tweets CSV file
      - to run in command line: "python classify_tweets.py <scraped tweets csv> <output classfied tweets csv filename>"
  - query.py: scrapes tweets given a query term and outputs a scraped tweets CSV file
