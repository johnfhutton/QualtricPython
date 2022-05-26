import pandas as pd
import matplotlib.pyplot as plt

# Note:  To generate the file from Qualtric, do the following
# - Export Data
# - CSV
# - (Check) Download all fields
# - (Radio) Use choice text
# - No additional options
# Remember to update the next line to the downloaded file name in local directory

#df=pd.read_csv('IndP1-Programming_Skills_Ranking_April-25_2022_19.27.csv')
df=pd.read_csv('AcaP1-Programming_Skills_Ranking_May-24_2022_21.23.csv')
# df.head()
# df.shape

q1df = df['Q1-Parsing'].str.split(',',expand=True)
# q1df.head()
# q1df.shape()

q1ranked = q1df.stack().value_counts()

file1 = open('results-rankedAca.txt', 'w')
file2 = open('results-alphaAca.txt',"w")
with pd.option_context('display.max_rows',None,'display.max_columns',None):
    print("-- Ranked List --")
    print( q1ranked.where(q1ranked>0).dropna() )
    print("-- Sorted by label --")
    print( q1ranked.sort_index() )
    file1.write("-- Ranked List --\n")
    file1.write( q1ranked.where(q1ranked>0).dropna().to_string() ) 
    file2.write("-- Sorted by label --\n")
    file2.write( q1ranked.sort_index().to_string() )

file1.close()
file2.close()

#q1ranked.sort_values().plot(y=2,left=0.35,kind='barh',figsize=(7.5,10))
#plt.show()