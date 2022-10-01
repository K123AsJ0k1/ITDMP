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
    words_read = False
    previous_line = ''
    for line in file.readlines():
        if 'Words:' in line and 'Chapters:' in previous_line and not words_read:
            #print(line)
            #words = line.split(':')[1]
            #try:
            temp_1 = line.split(':')[1]
            temp_2 = temp_1.strip() 
            temp_3 = temp_2.replace(',','')
            words = int(temp_3)
            #except:
            #    words = '*** ' + line.split(':')[1]
            #print(words)
            words_read = True
        if 'Author URL:' in line:
            read = True
            continue
        if read:
            if len(line) > 1 and 'End file' not in line and 'Summary:' not in line:
                split_length = len(re.findall("[\w']+",line))
                if split_length > 0:
                    if split_length < smallest_section:
                        smallest_section = split_length
                
                    if largest_section < split_length:
                        largest_section = split_length

                    words_per_section.append(split_length)
                    sections += 1
        previous_line = line
            
    file.close()
    #print(words_per_section)
    mean = None
    median = None
    mode = None
    #print(words_per_section)
    if len(words_per_section) > 0:
        mean = round(np.mean(words_per_section),3)
        median = np.median(words_per_section)
        #print(stats.mode(np.array(words_per_section), keepdims=False)[1])
        mode = stats.mode(np.array(words_per_section), keepdims=False)[0]
    
    return [words, sections, smallest_section, largest_section, mean, median, mode]
    #return {'words': words, 'amount': sections, 'smallest': smallest_section, 'largest': largest_section, 'mean': mean, 'median': median, 'mode': mode}

def statTest(fileName):
    dirName = os.path.dirname(__file__)
    pathName = os.path.join(dirName, 'fictionpress01\\fictionpress')
    print(pathName + '\\' + fileName)
    #sectionStats(pathName + '\\' + fileName)
    print(sectionStats(pathName + '\\' + fileName))


def getTexts(N):
    dirName = os.path.dirname(__file__)
    pathName = os.path.join(dirName, 'fictionpress01\\fictionpress')
    dirList = os.listdir(pathName)
    data = []
    i = 1
    
    for fileName in dirList:
        split = fileName.split(' - ')
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
    getTexts(100000)
    end = time.time()
    print(end - start)
    # Test
    # Action - bloodyhand43 - The Great Fight Between a US Soldier and The Koreans.txt
    # Action - lan Bradley - Oil.txt
    # Action - huiyan - The Pickpocket.txt
    # Action - FreedomsFlight - The Last King.txt
    # Action - CorkyBookworm1 - The Nightlight.txt
    # Action - G-Masta - Heaven for a blaller.txt
    # Action - ilu - Arc_ngeles.txt
    # Action - jclappt - Access to Betrayal.txt
    # Action - Aurora Moon1 - a very long night.txt
    # Action - Dr.Anonymous - Implosion.txt
    # Fantasy - Autumn-Wind-Kaze - Shadow Words_The Lovelorn Shadow.txt
    #statTest('Action - bloodyhand43 - The Great Fight Between a US Soldier and The Koreans.txt')
    #statTest('Action - Ian Bradley - Oil.txt')
    #statTest('Action - huiyan - The Pickpocket.txt')
    #statTest('Action - FreedomsFlight - The Last King.txt')
    #statTest('Action - CorkyBookworm1 - The Nightlight.txt')
    #statTest('Action - G-Masta - Heaven for a blaller.txt')
    #statTest('Action - ilu - Arc_ngeles.txt')
    #statTest('Action - jclappt - Access to Betrayal.txt')
    #statTest('Action - Aurora Moon1 - a very long night.txt')
    #statTest('Action - juicier-than-thou - pirate girl part 2.txt')
    #statTest('Fantasy - Autumn-Wind-Kaze - Shadow Words_ The Lovelorn Shadow.txt')
    #statTest('')
    
  
if __name__=="__main__":
    main()