from bs4 import BeautifulSoup, Tag
import re

user_per_year = {}
user_degree = {}

def count_pages(doc):
    soup = BeautifulSoup(doc)
    counts = []
    
    pages = soup.find_all(href=re.compile(r"^http://forum.ubuntu.ir/index.php\?action=mlist;sort=registered;start=\d+$"))
    for page in pages:
        i = int(page['href'].split('=')[-1])
        if i:
            counts.append(i)

    return max(counts), min(counts)

def count_users(doc):
    soup = BeautifulSoup(doc)
    
    for tr in soup.tbody:
        if  isinstance(tr, Tag):
            user = tr.td.find_next_sibling("td")
            #print(user.string, end=' ')
            
            degree = user.find_next_sibling("td", class_="windowbg lefttext")
            #print(degree.string, end=' ')
            # collect user degrees
            try:
                user_degree[degree.string] += 1
            except KeyError:
                user_degree[degree.string] = 1
            
            date = degree.find_next_sibling("td")
            year = date.string.split('-')[0]
            #print(year)
            # collect user signup years
            try:
                user_per_year[year] += 1
            except KeyError:
                user_per_year[year] = 1

def report():
    user_count = 0
    for y in user_per_year:
        user_count += user_per_year[y]
    print('\nTotal {0} users.'.format(user_count))

    print('Registration date:')
    for y in sorted(user_per_year):
        print('We have {0} users signed up in {1}'.format(user_per_year[y], y))
        
    print('User degrees:')
    for d in sorted(user_degree):
        print('We have {0} {1} users.'.format(user_degree[d], d))
