'''
This code extracts the names of the top 200 rappers from ranker.com and saves the list as a text file.
'''

from bs4 import BeautifulSoup
import urllib

# make our "soup" to scrape the rapper names
source_url = 'http://www.ranker.com/list/loadmore.htm?page=4&format=GRID&defaultpropid=0&listId=855723&inlineAdLoaded=true&instart_disable_injection=true'
r = urllib.urlopen(source_url).read()
soup = BeautifulSoup(r, "html.parser")

# find all all occurrences of rapper names which appears in span tags of class 'inlineBlock oNode robotoC'
rappers_source = soup.find_all('span', class_='inlineBlock oNode robotoC')

# compile the rapper names into an array
rappers = []
for text in rappers_source:
    name = unicode(text.get_text())
    rappers.append(name)

# print rappers to console and to text
text_file = open("rappers.txt", "w")
for i in range(0, len(rappers)):

    # swap the unicode character \xe9 with e which occurs in Andre 3000, other names do not contain any special
    # characters so this is the only cleaning we have to do
    if rappers[i] == u' Andr\xe9 3000':
        rappers[i] = 'Andre 3000'

    text_file.write(rappers[i].encode("UTF-8") + "\n")

text_file.close()
