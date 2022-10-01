__name__ = "preprocessmodule"
__doc__ = "Turns all text files in foldername to a csv with columns [Category, Genre, Language, Status, Rating, Author URL, Story], with separator | and line terminator ¦."

import os
import pandas as pd
import re


def folder_to_csv(folderpath = "Fictionpress", destination = "data.csv", maxFiles = 10000):
    columns = ["Category", "Genre", "Language", "Status", "Rating", "Author URL", "Story"]

    df = pd.DataFrame(columns = columns)
    
    count = 0

    folder = os.listdir(folderpath)

    filecount = min(maxFiles, len(folder))

    for filename in folder:
        path = folderpath + "/" + filename

        data = dict()

        with open(path, mode='r', encoding='utf-8') as f:
            for line in f:
                keyvalue = line.split(":", 1)
                if keyvalue[0] in columns:
                    data[keyvalue[0]] = keyvalue[1]
                    continue
                
                if len(line) > 7 and line[0:7] == "Summary":
                    break

            #The rest of the file is the story
            data["Story"] = "".join(f.readlines())

        s = pd.Series(data, index = columns)
        s = s.str.strip("\n")
        s["Story"] = s["Story"][:-9] #This removes "End file."
        df.loc[len(df.index)] = s.values
        count += 1
        
        #Show percentage
        if 100 * count // filecount > 100 * (count - 1) // filecount:
            print("Processed: ", str(100 * count//filecount) + "%", sep = "")

        if count >= filecount:
            break
        
    df.to_csv(folderpath + "/" + destination, sep = '|', index = False, line_terminator = "¦")
