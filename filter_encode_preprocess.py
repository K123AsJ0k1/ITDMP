import os
import numpy as np
import pandas as pd
import time
import shutil

start_time = time.time()
path = os.getcwdb()

def label_encode(directory, reload_df=False, save_data=False, write=False):
    fanfics = os.listdir(directory) #list of fanfic filenames
    
    if reload_df == True:
        fanfic_df = pd.DataFrame(columns=['category', 'author', 'story'])
        for file in fanfics:
            if file.endswith('.txt'):
                file_path = directory+'/'+file
                with open(file_path, 'r') as fanfic:
                    line_counter = 0
                    row = []
                    while line_counter<15:
                        line = fanfic.readline().rstrip('\n')
                        if len(row) == 0 and len(line) != 0:
                            row.append(line)
                        if line[:3] == 'by ':
                            row.append(line[3:])
                        if line[:8] == 'Category':
                            row.append(line[10:])
                        line_counter += 1
                    if len(row)==3:     #this is necessary because the folder has random invisible (temporary?) files
                        fanfic_df = fanfic_df.append({'category': row[2], 'author': row[1], 'story': row[0]}, ignore_index=True)
    else:
        fanfic_df = pd.read_csv('encode_data/fanfic_data.csv', sep='|', names=['category', 'author', 'story'], header=0)

    if save_data == True:
        fanfic_df.to_csv('encode_data/fanfic_data.csv', sep='|')

    columns = fanfic_df.columns[:-1] #columns 'category' and 'author'
    for column in columns:
        labels, levels = pd.factorize(fanfic_df[column])
        fanfic_df[column] = labels
        if column == 'category':
            categ_ids = pd.DataFrame({'categories': levels})
        if column == 'author':
            auth_ids = pd.DataFrame({'author': levels, 'story_count': np.unique(labels, return_counts=1)[1]})

    if save_data == True:            
        categ_ids.to_csv('encode_data/categ_ids.csv', sep='|')
        auth_ids.to_csv('encode_data/auth_ids.csv', sep='|')

    if write == True:
        for file in reversed(fanfics):
            if file.endswith('.txt'):
                file_path = 'reduced_fanfics/'+file
                with open(file_path, 'r') as fanfic: #find the lines to be edited
                    line_counter = -1
                    lines = []
                    while line_counter<15:  #way to stop while loop after doing everything necessary
                        line_counter += 1
                        line = fanfic.readline().rstrip('\n')
                        if line[:3] == 'by ':
                            index = auth_ids.index[auth_ids['author']==line[3:]][0]
                            lines.append((line_counter, str(index)+'\n'+str(auth_ids.iloc[[index]].story_count.values[0])+'\n'))
                        if line[:8] == 'Category':
                            lines.append((line_counter, str(categ_ids.index[categ_ids['categories']==line[10:]][0])+'\n'))


                with open(file_path, 'r') as fanfic:
                    text = fanfic.readlines()
                    try:
                        text[lines[0][0]] = lines[0][1]
                        text[lines[1][0]] = lines[1][1]
                        with open('encoded_fanfics/'+file, 'w') as fanficc:
                            fanficc.writelines(text)
                    except IndexError:
                        print(lines)

    return categ_ids, auth_ids

def remove_foreign(directory):
    fanfic_folder = os.listdir(directory) #list of fanfic filenames

    for file in fanfic_folder:
        file_path = directory+'\\'+file

        with open(file_path) as fanfic:
            for line in range(10):
                next(fanfic)
            for i in range(2):
                line = fanfic.readline()
                if line[:8] == 'Language':
                    if line[8:] != ': English\n':
                        fanfic.close()
                        os.remove(fanfic.name)
                        break

    return None

def filter_categories(directory, category, copy_files=False, delete_files=False):
    fanfic_folder = os.listdir(directory)
    category_stories = [f for f in fanfic_folder if f[:len(category+' -')] == category+' -'] #list of stories in the given category

    if copy_files == True:
        os.mkdir('filtered_categories/'+category)      #make directory for new category

        if len(category_stories)<5000:  #if conditions to filter different amounts of stories depending on category size
            for j,i in enumerate(category_stories): #go through all stories in a given category
                if j%5 == 0:
                    orig = 'fictionpress01/fictionpress/'+i
                    dest = 'filtered_categories/'+category+'/'+i
                    shutil.copyfile(orig, dest) #copy story to new directory

        elif len(category_stories)<20000:
            for j,i in enumerate(category_stories):
                if j%10 == 0:
                    orig = 'fictionpress01/fictionpress/'+i
                    dest = 'filtered_categories/'+category+'/'+i
                    shutil.copyfile(orig, dest)

        elif len(category_stories)<100000:
            for j,i in enumerate(category_stories):
                if j%25 == 0:
                    orig = 'fictionpress01/fictionpress/'+i
                    dest = 'filtered_categories/'+category+'/'+i
                    shutil.copyfile(orig, dest)

        elif len(category_stories)<200000:
            for j,i in enumerate(category_stories):
                if j%50 == 0:
                    orig = 'fictionpress01/fictionpress/'+i
                    dest = 'filtered_categories/'+category+'/'+i
                    shutil.copyfile(orig, dest)

        else:
            for j,i in enumerate(category_stories):
                if j%100 == 0:
                    orig = 'fictionpress01/fictionpress/'+i
                    dest = 'filtered_categories/'+category+'/'+i
                    shutil.copyfile(orig, dest)

    if delete_files == True:    #Delete files from original directory (to save space on drive)
        for i in category_stories:
            orig = 'fictionpress01/fictionpress/'+i
            os.remove(orig)
    
def filter_pipeline(directory, category): #copy files to new directory, then delete files from original directory
    fanfic_folder = os.listdir(directory)
    filter_categories(directory, category, True, False)
    filter_categories(directory, category, False, True)

def folder_to_csv(foldername = "fictionpress", destination = "data.csv"):

    columns = ["Category", "Genre", "Language", "Status", "Rating", "Author URL", "Story"]


    df = pd.DataFrame(columns = columns)
    
    for filename in os.listdir(foldername):
        path = foldername + "/" + filename

        data = dict()

        with open(path, mode='r', encoding='utf-8') as f:
            #print(path)
            for line in f:
                keyvalue = line.split(":", 1)
                if keyvalue[0] in columns:
                    data[keyvalue[0]] = keyvalue[1]
                    continue
                
                if len(line) > 7 and line[0:7] == "Summary":
                    break

            #The rest of the file is the story
            data["Story"] = "".join(f.readlines())

        s = pd.Series(data)
        s = s.str.strip("\n")
        s["Story"] = s["Story"][:-9] #This removes "End file."
        df.loc[len(df.index)] = s.values
        
    df.to_csv(foldername + "/" + destination, sep = '|', index = False, line_terminator = "¦")

#label_encode('reduced_fanfics', False, False, True)
authors = label_encode('reduced_fanfics', False, False, False)[1]
print(authors[authors['story_count']>1])

print(f"{(time.time() - start_time)} seconds")