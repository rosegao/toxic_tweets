  ### toxic_tweets 

Computer Science with Applications 2 Project
Team: Rose Gao, Andrea Koch, Ian Lyons


Project Objective: Detect toxicity, insult, obscenity, and identity hate in tweets. 
Visualize and track trends of toxicity for topics (e.g. abortion) and towards individuals (e.g. Clinton) throughout 2016-2018.


OVERALL STRUCTURE:
1) query.py:
  - User provides query parameters: (query_term, search dates, output filename)
  - Queries tweets and exports as a CSV
2) classify_tweets.py:
  - Reads in the CSV of raw tweets as a pandas dataframe
  - Tweets are processed and 
  - Vectorize the text in each tweet
  - Use the 6 toxic models to identify levels of toxicity (Toxic, Severe Toxic, 
    Obscene, Threat, Insult, Identity Hate)
3) Visualization:
  - Create graphs and pull them into a dashboard


INSTRUCTIONS:
1) Navigate to the 'toxic_tweets/toxic' directory and open an ipython terminal. Run query.py.

2) Use the 'go' method with paramaters <query term, e.g. 'metoo'>, <start date, e.g. '01/01/2018'>, <end date, e.g. '01/30/2018'>, <filename, e.g. 'scraped_tweets'>.
	- query_term (str): search term(s) (all in one string)
		- e.g. 'metoo'
	- starting_date (str): date in the format 'MM/DD/YYYY'
		- e.g. '01/01/2018'
	- ending_date (str): date in the format 'MM/DD/YYYY'
		- e.g. '01/30/2018'
	- filename (str): string 

3) Quit the ipython terminal. In the command line, enter: "python classify_tweets.py <scraped tweets csv> <output classified tweets csv filename>".

4) Visualize classified tweets using seaborn or plotly.


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
      - to run in command line: "python classify_tweets.py <scraped tweets csv> <output classified tweets csv filename>"
  - query.py: scrapes tweets given a query term and outputs a scraped tweets CSV file

All code was original code.
See note in build_toxicity_models.py regarding code adapted from sklearn documentation.
