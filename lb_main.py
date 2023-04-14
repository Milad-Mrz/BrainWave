import pandas as pd
import os
import time
import random
import subprocess
from lb_gui import *



# item lists
data_box_names = [-1, 0, 1, 3, 7, 15, 30, 60, 120, 999]
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

def map_reduce(file_name):
    # file_name = "data.csv"
    # read file
    df_temp = pd.read_csv(file_name)
    # read categories
    study_options = df_temp['Category'].unique().tolist()

    # call gui: first page containing all options to study 
    # ( course_A, ..., course_Z, French, Skill_A, ..., Skill_Z, Startup, Book, favourite_dialogues, work_place_dialogues, pickup_dialogues, poems)
    
    category = gui_first_page(study_options)

    subset = df[(df['Age'] > 30) & (df['City'] == 'London')]
    #print(subset)


    # crop the data frame by answer
    answer = study_options[int(answer) - 1]
    df = df_temp[df_temp['Category'] == answer]
    df_temp = df_temp[df_temp['Category'] != answer]

    if len(df) > 0:
        print("loading course successful. There are", len(df), "cards to study")
        print("_____________________________________________________________________________________")

    else:
        print("wrong input")
        select_course(file_name)
    clear_prompt()
    return df, df_temp


def data_monitor(df):
    data_rev = []  # data to review
    data_rem = []  # temp list to note and remove elements from data_rev later

    data_mis = []  # ( -1) mistaken data
    data_new = []  # (  0) new data

    data_001 = []  # (  1) data on 001 Day
    data_003 = []  # (  3) data on 003 Days
    data_007 = []  # (  7) data on 007 Days
    data_015 = []  # ( 15) data on 015 days
    data_030 = []  # ( 30) data on 030 days
    data_060 = []  # ( 60) data on 060 days
    data_120 = []  # (120) data on 120 days
    # Iterate over each row in the dataframe
    for index0, row in df.iterrows():
        # print(index, row)
        # Get data from files
        # SideA = str(row["SideA"])  # first side of the card
        # SideB = str(row["SideB"])  # seconf side of the card
        # misNo = int(row["misNo"])  # number of mistakes
        # OSide = int(row["OSide"])  # a flag that used for studing both sides
        # CateG = str(row["Category"])  # category of study

        BoxNo = int(row["BoxNo"])  # leitner box ID
        NextR = int(row["NextREV"])  # next reviewing time in minutes passed since epoch

        # print(SideA, SideB, CateG, BoxNo, NextR, OSide)
        if int(time.time() / 60.) > NextR: data_rev.append(index0)

        # allocate data to lists
        if BoxNo == -1:
            data_mis.append(index0)
        else:
            if BoxNo == 0 and int(time.time() / 60.) > NextR:
                data_new.append(index0)
            else:
                if BoxNo == 1:
                    data_001.append(index0)
                else:
                    if BoxNo == 3:
                        data_003.append(index0)
                    else:
                        if BoxNo == 7:
                            data_007.append(index0)
                        else:
                            if BoxNo == 15:
                                data_015.append(index0)
                            else:
                                if BoxNo == 30:
                                    data_030.append(index0)
                                else:
                                    if BoxNo == 60:
                                        data_060.append(index0)
                                    else:
                                        if BoxNo == 120:
                                            data_120.append(index0)
                                        else:
                                            print('Error-1')

    # def 3 monitor data
    len_rev = len(data_rev)
    len_mis = len(data_mis)
    len_new = len(data_new)
    len_001 = len(data_001)
    len_003 = len(data_003)
    len_007 = len(data_007)
    len_015 = len(data_015)
    len_030 = len(data_030)
    len_060 = len(data_060)
    len_120 = len(data_120)

    print("_____________________________________________________________________________________")
    print("number of mistakes:", len_mis)
    print("items to review:   ", len_rev)
    print(" ")
    print("[0]: ", len_new, "  [1]: ", len_001, "  [3]: ", len_003, "  [7]: ", len_007, "  [15]: ", len_015, "  [30]: ",
          len_030, "  [60]: ", len_060, "  [120]: ", len_120)
    print("_____________________________________________________________________________________")
    clear_prompt()

    return data_rev, len_mis, len_rev, len_new, len_001, len_003, len_007, len_015, len_030, len_060, len_120


def study(df, data_rev):

    data_rem = []  # temp list to note and remove elements from data_rev later
    new_BoxNo = 0
    # randomize the review list
    random.shuffle(data_rev)

    for index0 in data_rev:
        OSide = int(df.loc[index0, "OSide"])
        BoxNo = int(df.loc[index0, "BoxNo"])
        NextR = int(df.loc[index0, "NextREV"])
        if OSide == 0:
            SideA = str(df.loc[index0, "SideA"])
            SideB = str(df.loc[index0, "SideB"])
        else:
            SideA = str(df.loc[index0, "SideB"])
            SideB = str(df.loc[index0, "SideA"])

    #terminal user interface

        print("")
        print("")
        print("")
        print("=====================================================================================")
        print("")
        print("data ID: ", index0)
        print("")
        print(">>>   ", SideA, "?")
        print("")
        print("=====================================================================================")
        print("")


    # def 4 show
        print("Press enter to show other side")
        input( )
        print("=====================================================================================")
        print("")
        print('Answer:  ', SideB)
        print("")
        print("=====================================================================================")
        print("")
        print("")
        print("Great!")
        print("and did you remember it corretly?")
        answer = str(input())
        print("")
        print("")


    #def 5 check the answer
        # if yes then next box unless it's on last box
        # if no then

        if answer == 'yes' or answer == 'y' :
            # if user review and positive on remember then remove word from review list
            data_rem.append(index0)

            # check if it is on last box
            if BoxNo == 120:
                df.loc[index0, "BoxNo"] = 0

                # check if other side it already studied or not?
                if OSide == 0 :
                    #if not studied yet, set it to study
                    df.loc[index0, "OSide"] = 1
                    df.loc[index0, "NextREV"] = int(time.time()/60.) + 10
                else:
                    #if studied both sides, set it to review as a new word for next 6 month and reset sides
                    df.loc[index0, "NextREV"] = int(time.time()/60.) + 262800
                    df.loc[index0, "OSide"] = 0

            # when it is not on last box
            else:
                # update box number to next box

                new_BoxNo = data_box_names[data_box_names.index(BoxNo)+1]
                df.loc[index0, "BoxNo"] = new_BoxNo
                # current time + 60 * 24 hours * ..
                df.loc[index0, "NextREV"] = int(time.time()/60.) + 1440 * new_BoxNo

        if answer == 'no' or answer == 'n' :
            # set box number to mistaken
            df.loc[index0, "BoxNo"] = -1
            # current time + 10 minutes
            df.loc[index0, "NextREV"] = int(time.time()/60.) + 10
            # update number of mistkes
            df.loc[index0, "misNo"] += 1

        # in case of wrong input
        if answer != 'no' and answer != 'n' and answer != 'yes' and answer != 'y' :
            new_BoxNo = BoxNo
            print("wrong input the card will be review later again")

        print(BoxNo, '>>>', new_BoxNo)
        print("")

        data_monitor(df)

        print("")
        print("")
        print("")
        print("")
        df.to_csv("data_copy.csv", index=False)

    for index0 in data_rem:
        data_rev.remove(index0)

    data_rem = []
    clear_prompt()

    return df


def data_writer(df,df_temp):
    ## update and merge data frame
    frames = [df, df_temp]
    df = pd.concat(frames)
    df.to_csv("data.csv", index=False)

if __name__ == '__main__':
    Float_Layout().run()


df, df_temp = select_course("data.csv")
data_rev, len_mis, len_rev, len_new, len_001, len_003, len_007, len_015, len_030, len_060, len_120 = data_monitor(df)
df = study(df, data_rev)
data_writer(df, df_temp)



