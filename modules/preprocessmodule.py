__name__ = "preprocessmodule"
__doc__ = "Turns all text files in foldername to a csv with columns [Category, Genre, Language, Status, Rating, Author URL, Story], with separator | and line terminator ¦."

import os
import pandas as pd


def folder_to_csv(foldername = "Fictionpress", destination = "data.csv"):

    columns = ["Category", "Genre", "Language", "Status", "Rating", "Author URL", "Story"]


    df = pd.DataFrame(columns = columns)
    
    for filename in os.listdir(foldername):
        path = foldername + "/" + filename

        data = dict()

        with open(path, mode='r', encoding='utf-8') as f:
            print(path)
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