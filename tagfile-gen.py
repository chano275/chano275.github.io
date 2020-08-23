import os
directory = '_posts/'

tagslist = []
finaltags = []

for file in os.listdir(directory):
    print (file)
    f = open('_posts/' + file)
    lines = f.read().splitlines()
    for index, line in zip(range(5), lines):
        if index == 4: # Post Tags are in 4th line of a Post
            #print (line)
            line = line.split(':')
            line = line[1].split(' [')
            line = line[1].split(']')
            line = line[0].split(', ')
            tagslist.append(line) #array of comma seperated tags added into tagslist array

for tags in tagslist:
    for tag in tags:
        if tag not in finaltags: #If tag is not already in final tags list, add it.
            finaltags.append(tag)



for final in finaltags: #Actual Tag-File generation
    #print( final )
    tagfile = open('tags/' + final + '.md','w')
    tagfile.write('---')
    tagfile.write('\n')
    tagfile.write('layout: tagpage')
    tagfile.write('\n')
    tagfile.write('tag: '+ final)
    tagfile.write('\n')
    tagfile.write('permalink: /tags/' + final + '/')
    tagfile.write('\n')
    tagfile.write('---')
    tagfile.close()