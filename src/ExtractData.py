from bs4 import BeautifulSoup
import urllib
import wikipedia

# make our "soup"
source_url = 'http://www.ranker.com/list/loadmore.htm?page=4&format=GRID&defaultpropid=0&listId=855723&inlineAdLoaded=true&instart_disable_injection=true'
r = urllib.urlopen(source_url).read()
soup = BeautifulSoup(r, "html.parser")

print type(soup)

rappers_source = soup.find_all('span', class_='inlineBlock oNode robotoC')

rappers = []
for text in rappers_source:
    name = unicode(text.get_text())
    rappers.append(name)

# print rappers to console and to text
text_file = open("rappers.txt", "w")
for i in range(0,len(rappers)):
    if rappers[i] == u' Andr\xe9 3000':
        rappers[i] = 'Andre 3000'
    # else:
    #     rappers[i] = str(rappers[i])[1:]
    # rappers[i] = rappers[i].replace(' ', '_')
    text_file.write(rappers[i].encode("UTF-8") + "\n")

print rappers
print len(rappers)
text_file.close()
