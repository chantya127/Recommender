

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt#for visualization
import seaborn as sns #for visualization
from wordcloud import WordCloud #for visualization
import string
from nltk.corpus import stopwords
from openpyxl import Workbook # converting csv -> xlsx
import re
import csv




dataset = pd.read_csv('CCMLEmployeeData.csv')




#dataset.head()




event = set(dataset['Event1'])

print('STARTED..')



#plotting counts of various domains
#plt.figure(figsize = (17,10))
#ax = plt.gca()
#sns.countplot(dataset['Domain'])
#plt.xticks(rotation=45)




#plotting counts of various events
#plt.figure(figsize = (17,10))
#ax = plt.gca()
#sns.countplot(dataset['Event1'])
#plt.xticks(rotation=45)




#visualization part

#sentences = dataset['Event1'].tolist()
#sentences = ' '.join(sentences)
#plt.figure(figsize=(20,20))
#plt.imshow(WordCloud().generate(sentences))



dataset_3  = dataset.copy()
dataset_3 = dataset_3.iloc[:,1:3]

domains__ = dataset_3['Domain']

dataset_3=pd.get_dummies(dataset_3['Event1'])

dataset_3['Domain'] = domains__
domains = set(list(domains__))

domains = [domain.lower() for domain in domains]

aggregation_functions = {'Certifications': 'sum', 'Competitions': 'sum','Courses': 'sum', 'Expos':'sum', 'Fests':'sum',  'Hackathons':'sum',  'Internships':'sum',  'Jobs':'sum',  'Seminars':'sum', 'Talks':'sum','Trainings':'sum','Webinars':'sum','Workshops':'sum','Domain': 'first'}


new_df = dataset_3.groupby(dataset_3['Domain']).aggregate(aggregation_functions)


new_df.reset_index(inplace=True,drop=True)


columns = new_df.columns
columns = [col.lower() for col in columns]
new_df.columns = columns

print("Executing..")

user_id_matrix = new_df.pivot_table(index = 'domain')

user_id_matrix.index = [index.lower() for index in user_id_matrix.index]
user_id_matrix = user_id_matrix.rename(columns = lambda x : str(x)[:-1])

events = dataset['Event1']
events = set(list(events))
events = [event.lower() for event in events]
events = [event[:-1] for event in events if event.endswith('s')]


dataset_2= dataset.copy()
dataset_2 = dataset_2.iloc[:,0:3]
dataset_2['Domain'] =dataset_2['Domain'].str.lower()
dataset_2['Event1'] =dataset_2['Event1'].str.lower()
dataset_2['Event1'] = dataset_2.apply(lambda x: x['Event1'][:-1], axis = 1)


headers = {'Event':'Recommendations'}
def recommend(mini_challenge , i):
    aa = mini_challenge
    remove = string.punctuation
    remove = remove.replace("+", "") # don't remove + sign
    pattern = r"[{}]".format(remove) # create the pattern
    
    my_dict = {}

    mini_challenge = re.sub(pattern, "", mini_challenge) 
    mini_challenge =[char.lower() for char in mini_challenge.split() if char.lower() not in stopwords.words('english')]
    mini_challenge = [text if not text.endswith('s')else text[:-1] for text in mini_challenge]
    
    if i==0:
        with open('dict.csv','w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in headers.items():
                writer.writerow([key, value])
    
    
    
    
    words = [word for word in mini_challenge if  word in events] # all the events found
 
    if len(words)>0:
        for event in words:
            recommendations = user_id_matrix[event]
            domain= recommendations.sort_values(ascending=False).head(1).index.values
            ttt = str(domain[0])
            names = dataset_2.loc[(dataset_2['Domain'] == ttt) &(dataset_2['Event1'] == event)]['Name'].values 
            
            names = list(names)
            try:
                my_dict.append(names)
            except:
                my_dict[aa] = (names)
    
        
        with open('dict.csv', 'a') as csv_file:  
            writer = csv.writer(csv_file)
            
            for key, value in my_dict.items():
                   writer.writerow([key, value])
                
        #Converting csv -> xlsx            
        wb = Workbook()
        ws = wb.active
        with open('dict.csv', 'r') as f:
            for row in csv.reader(f):
                ws.append(row)
        wb.save('output.xlsx')           
       
        
        
    else:
        names = '---'
        try:
            my_dict.append(names)
        except:
            my_dict[aa] = (names)
    
        
        with open('dict.csv', 'a') as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in my_dict.items():
                   writer.writerow([key, value])
                
        #Converting csv -> xlsx            
        wb = Workbook()
        ws = wb.active
        with open('dict.csv', 'r') as f:
            for row in csv.reader(f):
                ws.append(row)
        wb.save('output.xlsx')   
        

#Taking inputs from input.csv file
inputs = pd.read_csv('input.csv')
num =1

while num!=0:
    try:
        for i in range (len(inputs)):
            text = inputs.iloc[i,:][0]
            #print(text[:4])
            recommend(text , i)
        print('Success!!')
        num =0
    except:
        pass


           
        
    
    




