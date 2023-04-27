import pandas as pd
import time
from lb_gui import *


# Category,BoxNo,SideA,SideB,ActiveSide,TimeNextREV,MistakeNo

# item lists
answer_int = 0

#   -1: new words
#    0: to be reviewed now
#    1: to be reviewed after a day
#    3: to be reviewed after 3 days
#    7: to be reviewed after a week
#   15: to be reviewed after 2 weeks
#   60: to be reviewed after 2 months
#  120: to be reviewed after 4 months
#  999: output

def mainDataCheck(df):
    # clean data 
    # check for 1-duplicates 2-zeros 3-... 
    df = df
    return df

def mainMapReduce():
    file_name = 'BladeLearner2049/data/data.csv'
    # read file - file_name = "data.csv"  /home/milad/Desktop/Current Project/LearningBox/BladeLearner2049/data/data.csv   
    df = pd.read_csv(file_name)
    #clean the data
    df = mainDataCheck(df)
    # read categories
    study_options = df['Category'].unique().tolist()
    # call gui: first page containing all options to study 
    # ( course_A, ..., course_Z, French, Skill_A, ..., Skill_Z, Startup, Book, favourite_dialogues, work_place_dialogues, pickup_dialogues, poems)
    return study_options, df

def mainSubset(selected_category, mistake, df):
    #category_subset = df[(df['Category'] == selected_category)]
    if mistake == 1 : 
        study_subset = df[(df['Category'] == selected_category) & (df['MistakeNo'] > 2) ] 
    else:    
        study_subset = df[(df['Category'] == selected_category) & (df['TimeNextREV'] < int(time.time() / 60.)) ]

    return study_subset

    #subset = df[(df['Age'] > 30) & (df['City'] == 'London')]

def mainLietner(row, answer):
    box_id = [-1, 0, 1, 3, 7, 15, 30, 60, 120]
    # update box number to zero if answer was negative
    if answer == 0 :
        row['BoxNo'] = 0
        row['MistakeNo'] += 1
    else:
        card_box_id = row['BoxNo']
        if card_box_id < 120:
            # update box,  number if answer was positive
            row['BoxNo'] = box_id[box_id.index(card_box_id)+1]
            row["NextREV"] = int(time.time()/60.) + (1440 * row['BoxNo']) + 360

        else: # == 120
            # if first side is learnt 
            if row['ActiveSide'] == 0 : 
                row['ActiveSide'] = 1
                row["NextREV"] = int(time.time()/60.) + 360 

            if row['ActiveSide'] == 1 : 
                row["NextREV"] = int(time.time()/60.) + 262800 
                row['ActiveSide'] == 0
    return row

def mainDataWriter(df):
    df.to_csv("./data/data_bu.csv", index=False)



'''
df, df_temp = select_course("data.csv")
data_rev, len_mis, len_rev, len_new, len_001, len_003, len_007, len_015, len_030, len_060, len_120 = data_monitor(df)
df = study(df, data_rev)
data_writer(df, df_temp)
'''







