from cgitb import small
import numpy as np
from scipy import stats
import re
import os
import csv
import pathlib
import time

def createCsv(dirName, header, data):
    #print(dirName)
    #print(data)
    place = dirName + '\\' + 'fictionpress_section_stats.csv'
    with open(place, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)
        csv_file.close()

def sectionStats(path):
    file = open(path, 'r', encoding='utf-8')
    
    words = 0
    words_per_section = []
    last_line = ''
    sections = 0
    smallest_section = 100000
    largest_section = 0
    read = False
    
    for line in file.readlines():
        if 'Words:' in line:
            words = line.split(':')[1]
            #temp_1 = line.split(':')[1]
            #temp_2 = temp_1.strip() 
            #temp_3 = temp_2.replace(',','')
            #words = int(temp_3)
        if 'Summary:' in line:
            read = True
            continue
        if read:
            if len(line) > 1 and  'End file' not in line:
                split_length = len(re.findall("[\w']+",line))
                if split_length > 0:
                    if split_length < smallest_section:
                        smallest_section = split_length
                
                    if largest_section < split_length:
                        largest_section = split_length

                    words_per_section.append(split_length)
                    sections += 1
            
    file.close()

    mean = round(np.mean(words_per_section),3)
    median = np.median(words_per_section)
    mode = stats.mode(np.array(words_per_section), keepdims=False)[0]
    
    return [words, sections, smallest_section, largest_section, mean, median, mode]
    #return {'words': words, 'amount': sections, 'smallest': smallest_section, 'largest': largest_section, 'mean': mean, 'median': median, 'mode': mode}


def getTexts(N):
    dirName = os.path.dirname(__file__)
    pathName = os.path.join(dirName, 'fictionpress01\\fictionpress')
    dirList = os.listdir(pathName)
    data = []
    i = 1
    
    for fileName in dirList:
        split = fileName.split('-')
        genre = split[0].strip()
        author = split[1].strip()
        story = split[2].strip()
        
        piece = [i,genre,author,story] + sectionStats(pathName + '\\' + fileName)
        data.append(piece)

        if i == N:
            break
        i = i + 1

    header = ['id', 'genre', 'author', 'story', 'words', 'sections', 'smallest_section', 'largest_section', 'word_mean', 'word_median', 'word_mode']
    createCsv(dirName, header, data)
    

def main():
    #dirName = os.path.dirname(__file__)
    #pathName = os.path.join(dirName, 'fictionpress01\\fictionpress')
    start = time.time()
    getTexts(10000)
    end = time.time()
    print(end - start)
    
  
if __name__=="__main__":
    main()