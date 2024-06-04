import requests
from bs4 import BeautifulSoup
import re

url = 'https://en.wikipedia.org/wiki/Elon_Musk'
r = requests.get(url, headers={"Content-Type":"text"})
html = r.text

left_text = "A member of the wealthy South African Musk family, Musk was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at age 18" 

soup = BeautifulSoup(html, 'html.parser')
body = soup.find('body')
right_text = body.get_text()
left_text_words = left_text.split()
n = 4

# breaking the left list to chunks lists of 4 items
left_text_list = [' '.join(left_text_words[i:i+n]) for i in range(0,len(left_text_words),n)]
words_match_counter = 0

for index, chunk in enumerate(left_text_list):
    # find chunk in right plain text

    if len(chunk.split()) <3:
        #Palestine Liberation Organization
        if len(chunk.split()) == 2:
            # need to add 2 more words from previous chunk
            chunk_before = left_text_list[index-1].split()[-2:]
            chunk = ' '.join(chunk_before) + ' ' + chunk
        else:
            # need to add 2 more words from previous chunk
            chunk_before = left_text_list[index-1].split()[-3:]
            chunk = ' '.join(chunk_before) + ' ' + chunk
        print(chunk)

    if chunk in right_text:
        chunk_size = len(chunk.split())
        #found plain text in chunk now replacing in html
        if chunk in html:
            print('found line replacing')
            html = html.replace(chunk, "<b style='background-color: rgb(255, 102, 102);'>%s</b>" % chunk)     
            words_match_counter = words_match_counter + chunk_size

        else:
            print('chunk is hiding in span')
            #get element of chunk before 
            elem_search = soup(text=re.compile(r'{}'.format(left_text_list[index-1])))
            for elem in elem_search:
                current_chuck_list = chunk.split()

                for index, word in enumerate(current_chuck_list):
                    new_small_chunk_array_to_replace = []
                    if word in elem.next.text:
                        original_elem = elem.next
                        tag = soup.new_tag('b')
                        tag.attrs['style'] = 'background-color: rgb(255, 102, 102);'
                        elem.next.wrap(tag)
                        print(elem.next)
                        rep_tag = str(elem.next)
                        
                        str_elem = str(original_elem)
                        if str_elem in html:
                            html = html.replace(str_elem, rep_tag)
                        break
