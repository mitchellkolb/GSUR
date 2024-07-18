# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:34:58 2021
Edited on Feb 2024
@author: sl1mc and mitchellkolb
"""
import os
import pandas as pd
from csv import reader
from sklearn.tree import DecisionTreeClassifier
import datetime


full_number = 0
actual_number = 0

def do_calc(path, output_name):
    sq_correct = 0
    sq_incorrect = 0
    sq_hint = 0
    correct = 0
    incorrect =0
    hint = 0
    exp_dir = 0
    next_page = 0
    prev_page = 0
    m_back = 0
    
    sq_crrect_l = []
    sq_incorrect_l = []
    sq_hint_l = []
    correct_l = []
    incorrect_l = []
    hint_l = []
    exp_dir_l = []
    next_page_l = []
    prev_page_l = []
    m_back_l = []
    m_forward_l = []
    
    m_forward = 0
    time_list = []
    
    shade_region = []
    switcher = 0
    
    color_regions = []


    try:
        #Begins with the analysis of the data file
        with open(path, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            i = 0
            
            for row in csv_reader:
                if len(row) == 0:
                    continue
                if(i == 1):
                    init_time = row[3]
                    #print(row, init_time)
                    #date_time_obj = datetime.datetime.strptime(init_time, '%m/%d/%Y %H:%M')
                    date_time_obj = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
                    init_time = date_time_obj.timestamp()
                    #print(init_time)
                else:
                    if(row[3] != None):
                        #print(row[3])
                        try:
                            #date_time_obj = datetime.datetime.strptime(row[3], '%m/%d/%Y %H:%M')
                            date_time_obj = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                            new_time = date_time_obj.timestamp()
                            time_list.append(new_time-init_time)
                            shade_region.append(switcher)
                        except:
                            #print('Wrong format')
                            other = 2
                
                #print(str(' '.join(row)))
                if('Skill' in str(' '.join(row)) and ('incorrect' in str(' '.join(row)) or 'Incorrect' in str(' '.join(row)))):# or 'incorrect' in row[5] or 'Incorrect' in row[5] or 'incorrect' in row[5] or 'Incorrect' in row[5]):
                    sq_incorrect +=1                
                elif('incorrect' in str(' '.join(row)) or 'Incorrect' in str(' '.join(row))):# or 'incorrect' in row[5] or 'Incorrect' in row[5] or 'incorrect' in row[5] or 'Incorrect' in row[5]):
                    incorrect +=1
                    #print('inc')
                    
                if('Skill' in str(' '.join(row)) and (' correct' in str(' '.join(row)) or ' Correct' in str(' '.join(row)))):# or 'correct' in row[5] or 'Correct' in row[5] or 'correct' in row[5] or 'Correct' in row[5]):
                    sq_correct += 1
                if('Skill' not in str(' '.join(row)) and 'incorrect' not in str(' '.join(row)) and ('correct' in str(' '.join(row)))):
                    correct += 1
                    #print('cor')
                if(('Skill' in str(' '.join(row)) or ('skill' in str(' '.join(row)))) and('hint' in str(' '.join(row)) or 'Hint' in str(' '.join(row)))):# or 'hint' in row[5] or 'Hint' in row[5] or 'hint' in row[5] or 'Hint' in row[5]):
                    sq_hint +=1
                elif('hint' in str(' '.join(row)) or 'Hint' in str(' '.join(row))):# or 'hint' in row[5] or 'Hint' in row[5] or 'hint' in row[5] or 'Hint' in row[5]):
                    hint +=1
                    #print('h')
                if('experimenter direction' in str(' '.join(row))):
                    exp_dir += 1
                    #print('ed dir')
                if('next' in str(' '.join(row)) and 'page' in str(' '.join(row))):
                    next_page += 1
                    #print('next')
                if('previous' in str(' '.join(row)) and 'page' in str(' '.join(row))):
                    prev_page += 1
                    #print('prev')
                if('Moved back' in str(' '.join(row))):
                    m_back += 1
                    #print(row)
                if('Moved forward' in str(' '.join(row))):  #here we see if we should reset
                    m_forward += 1
                    sq_crrect_l.append(sq_correct)
                    sq_incorrect_l.append(sq_incorrect)
                    sq_hint_l.append(sq_hint)
                    correct_l.append(correct)
                    incorrect_l.append(incorrect)
                    hint_l.append(hint)
                    exp_dir_l.append(exp_dir)
                    next_page_l.append(next_page)
                    prev_page_l.append(prev_page)
                    m_back_l.append(m_back)
                    m_forward_l.append(m_forward)
                    correct = 0
                    incorrect =0
                    hint = 0
                    exp_dir = 0
                    next_page = 0
                    prev_page = 0
                    m_back = 0
                    m_forward = 0
                    if(switcher == 0):
                        switcher = 1
                    else:
                        switcher = 0
                    color_regions.append(i)
                    #print(row)
                i += 1
                

        sq_crrect_l.append(sq_correct)
        sq_incorrect_l.append(sq_incorrect)
        sq_hint_l.append(sq_hint)
        correct_l.append(correct)
        incorrect_l.append(incorrect)
        hint_l.append(hint)
        exp_dir_l.append(exp_dir)
        next_page_l.append(next_page)
        prev_page_l.append(prev_page)
        m_back_l.append(m_back)
        m_forward_l.append(m_forward)
        #REPEATED QUESTIONS: supress trailing logs except those that are different
        #dont allow two hints in a row

        #This code gets the patient_name, date, and time_taken columns from the file label.
        filename = os.path.basename(path)
        # Split the file name by underscore and period to isolate the components
        name_parts = filename.split('_')
        if len(name_parts) > 1:
            patient_name = name_parts[0]  # The first part is the name of the file
            # Further split the second part by the period to separate the date and time from the extension
            date_time_part = name_parts[1].split('.')
            date_time = date_time_part[0]  # Before the period is the date and time
            # Assuming the format is consistently "date time"
            date, time_taken = date_time.split(' ')
        else:
            patient_name = None
            date = None
            time_taken = None  # Return None if the expected format is not met
        print(patient_name, date, time_taken)

        #This code saves the first two words from the data file action column that are in the second to last row for consistency
        #Gets the quiz_name value from the .csv
        # Read the CSV file into a DataFrame
        df = pd.read_csv(path)
        # Ensure the DataFrame is not empty and has the necessary column
        if not df.empty and 'action' in df.columns:
            # Get the 'action' value from the second-to-last row
            #TRY OUT LAST 14 CHARACTERS or just replace any Skills Quiz with Skills Quiz-30
            action_value = df.iloc[-2]['action']
            # Split the 'action' string and take the first two words
            action_words = action_value.split()[:2]
            # Join the first two words to form the quiz name
            quiz_name = ' '.join(action_words)
            #This is a hardcoded solution to the weird label that skills quiz 30 is. Every other quiz has the number with the hyphen but quiz 30 doesn't
            if quiz_name == "Skills Quiz":
                quiz_name = "Skills Quiz-30"
        else:
            quiz_name = "Quiz_name_NA"  # Default value if the conditions are not met

        #This code calculates the time variables for this data
        hours, remainder = divmod(time_list[-1]-time_list[0], 3600)
        minutes, seconds = divmod(remainder, 60)



        #Katie said she would work on getting the value for the Quiz_attempt column
        quiz_attempt = "000"



        df_data = pd.DataFrame({'patient_name':patient_name,
                                'date':date,
                                'time_taken':time_taken,
                                'quiz_name':quiz_name,
                                'quiz_attempt':quiz_attempt,
                                'skill quiz incorrect':sq_incorrect,
                                'skill quiz correct':sq_correct,
                                'prev_page':prev_page,
                                'next_page':next_page,
                                'skill quiz hint':sq_hint,
                                'incorrect':incorrect,
                                'correct':correct,
                                'hint':hint,
                                'm_forward':m_forward,
                                'm_back':[m_back],
                                'Hours':hours,
                                'Minutes':minutes,
                                'Seconds':seconds
                                })
        


        # Check if the file exists
        file_exists = os.path.exists(str(output_name)+'FinalResults.csv')

        # Append if file exists, otherwise write a new file
        mode = 'a' if file_exists else 'w'

        # Include header if file does not exist
        header = not file_exists

        # Saves dataframe to .csv file
        df_data.to_csv(str(output_name)+'FinalResults.csv', mode=mode, index=False, header=header)

        #update totals numbers to do stats at the end of execution
        global actual_number 
        actual_number = (1 + actual_number)
            
    except Exception as e:
        print(f"{path} --> Error in file occured: {e} ")
        


def setup():
    '''
    Place the file you want to verify in './people', and write its name in "filename"
    '''

    # Get the current working directory (where the script is located)
    current_directory = os.path.dirname(os.path.realpath(__file__))
    print("Main directory:", current_directory)

    # Checks/creates the Results folder in this directory
    results_dir_path = os.path.join(current_directory, "Results")
    if not os.path.exists(results_dir_path):
        os.makedirs(results_dir_path)

    people_dir_path = os.path.join(current_directory, "People")
    txt_files = []  # Initialize an empty list to store the full paths of .txt files

    # Check if the People directory exists
    if os.path.exists(people_dir_path) and os.path.isdir(people_dir_path):
        # List all files in the directory and sort them
        files = sorted(os.listdir(people_dir_path))
        # Append the full path of .txt files to the list
        for file in files:
            if file.endswith('.txt'):
                full_path = os.path.join(people_dir_path, file)
                txt_files.append(full_path)
    else:
        print("The people/data directory does not exist or is not a directory.")


    outputFilePath= os.path.join(current_directory, "Results/")


    #update totals numbers to do stats at the end of execution
    #This resets the UI total numbers so if you run the downloader multiple times the number stays consistent
    global actual_number, full_number
    actual_number = 0
    full_number = 0

    # countENDER = 0
    # for dataFilePath in txt_files:
    #     if countENDER != 16:
    #         do_calc(dataFilePath, outputFilePath)
    #         full_number = (1 + full_number)
    #         countENDER += 1
    for dataFilePath in txt_files:
        do_calc(dataFilePath, outputFilePath)
        full_number = (1 + full_number)

    skipped_number = full_number - actual_number
    return(f"{actual_number} files analyzed of {full_number}.\n{skipped_number} were skipped.")    


   
if __name__ == "__main__":
            
    setup()


