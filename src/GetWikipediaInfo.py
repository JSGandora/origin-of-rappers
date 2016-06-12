import wikipedia, urllib
from bs4 import BeautifulSoup

input = open("rappers_151-200.txt", "r")
output = open("birthplaces_151-200.txt", "w")

rappers = input.readlines()
for x in range(0, len(rappers)):
    rapper = rappers[x]
    url = wikipedia.page(wikipedia.search(rapper)[0]).url
    print url
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    birth_source = soup.find_all('span', class_='birthplace')
    infocard = soup.find_all('table', class_='infobox vcard plainlist')
    output.write(rapper.encode('utf8'))
    if len(birth_source) >= 1:
        print rapper, birth_source[0].get_text()
        output.write(birth_source[0].get_text().encode('utf8') + '\n')
    else:
        info = infocard[0].get_text().split('\n')
        for i in range(0, len(info)):
            if info[i] == u'Born':
                print rapper, info[i+2]
                output.write(info[i+2].encode('utf8')+'\n')
            if info[i] == u'Origin':
                print rapper, info[i+1]
                output.write(info[i+1].encode('utf8')+'\n')

input.close()
output.close()
