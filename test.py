from cgitb import small
import numpy as np
from scipy import stats
import re
import os
import csv

#f = open('Fanfic_E\Fanfic_E\E-Ring\Completed\E-Ring - Longing for Oblivion - Crossing the line.txt', 'r')
#f = open('Fanfic_E\Fanfic_E\Earthbound\Completed\Earthbound - KMSymphonyOfSilence - All Souls.txt', 'r')

#def section_stats_csv(data):
#    header = ['id', 'genre', 'author', 'story', 'words', 'sections', 'smallest_section', 'largest_section', 'word_mean', 'word_median', 'word_mode']

#    with open('D:\\Users\\ITDMP\\fictionpress_section_stats.csv', 'w', encoding='UTF8', newline='') as csv_file:
#        writer = csv.writer(csv_file)
#        writer.writerow(header)
#        writer.writerows(data)
#        csv_file.close()

def section_stats(path):
    print(path)
    file = open(path, 'r')
    
    words = 0
    words_per_section = []
    last_line = ''
    sections = 0
    smallest_section = 100000
    largest_section = 0
    read = False
    
    for line in file.readlines():
        if 'Words:' in line:
            temp_1 = line.split(':')[1]
            temp_2 = temp_1.strip() 
            temp_3 = temp_2.replace(',','')
            words = int(temp_3)
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

path = 'D:\\Users\\ITDMP\\fictionpress01\\fictionpress'
dir_list = os.listdir(path)

data = []
N = 80 # of equally diviced genres
N_G = 8
count = 0
picked_genre = ''
i = 1
#action = 1250
#biography = 1250
#essay = 1250
#fable = 1250
#family = 1250
#fantasy = 1250
#friendship = 1250
#general = 1250
# Action, Biography, Essay, Fable, Family, Fantasy, Friendship, General 
for file in dir_list:
    #piece = []
    #print(file)
    #f = open(path + '\\' + str(file), 'r')
    #text = f.read()
    #section_stats(text)
    #f.close()
    split = file.split('-')
    genre = split[0].strip()
    author = split[1].strip()
    story = split[2].strip()

    #if picked_genre == '':
    #    piece = [i,genre,author,story] + section_stats(path + '\\' + str(file))
    #    data.append(piece)
    #    picked_genre = genre
    #    count = count + 1
    #    continue

    #if picked_genre == genre:
    #    if count == N/N_G:
    #        picked_genre = ''
    #        count = 0
    #        piece = [i,genre,author,story] + section_stats(path + '\\' + str(file))
    #        data.append(piece)
    #        continue

    #    piece = [i,genre,author,story] + section_stats(path + '\\' + str(file))
    #    data.append(piece)
    #    count = count + 1
        
        

    piece = [i,genre,author,story] + section_stats(path + '\\' + file)
    data.append(piece)
    #piece.append(section_stats(path + '\\' + str(file)))
    #
    #print(piece)
    #genre = split[0]
    #author = split[1]
    #story = split[2]
    #print(str(file))
    #print(split)
    #print(section_stats(path + '\\' + str(file)))
    #print('')

    if i == N:
        break
    i = i + 1

print(data)
#print(data)
#header = ['id', 'genre', 'author', 'story', 'words', 'sections', 'smallest_section', 'largest_section', 'word_mean', 'word_median', 'word_mode']

#csv_file = open('D:\\Users\\ITDMP\\fictionpress_section_stats.csv', 'w')
#writer = csv.writer(csv_file)
#writer.writerow(header)
#writer.writerows(data)
#csv_file.close()

#with open('D:\\Users\\ITDMP\\fictionpress_section_stats.csv', 'w', encoding='UTF8', newline='') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(header)
#    writer.writerows(data)
#    csv_file.close()

#with open('fictionpress_section_stats.csv', 'w', encoding='UTF8', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(header)
#    writer.writerows(data)

#print('Stats:')
#print(np.mean(words_per_section))
#print(np.median(words_per_section))
#print(stats.mode(np.array(words_per_section), keepdims=False)[0])
#print(words_per_section)
#print(smallest_section)
#print(largest_section)
#print(sections)
