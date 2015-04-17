from requests import session
import parse
import cache

payload = {
    'action': 'login2',
    'user': '',
    'passwrd': ''
}

url = 'http://forum.ubuntu.ir/index.php?action=mlist;sort=registered;start={0}'

def get_account():
    print('Please enter your ubuntu.ir account!')
    print('Username:', end=' ')
    payload['user'] = input()
    print('Password:', end=' ')
    payload['passwrd'] = input()

with session() as req:
    #login
    get_account()
    r = req.post('http://forum.ubuntu.ir/index.php', data=payload)
    
    response = req.get(url.format(0))
    page_max, page_inc = parse.count_pages(response.text)
    page_count = (page_max/page_inc) + 1
    
    try:
        app_data = cache.json_load()
        parse.user_per_year = app_data['user_per_year']
        parse.user_degree = app_data['user_degree']
        first_page = app_data['page'] + page_inc
    except FileNotFoundError:
        print('Analyzing page 1 of {0:.0f}'.format(page_count), end='\r')
        parse.count_users(response.text)
        first_page = page_inc
    
    for i in range(first_page, page_max + page_inc, page_inc):
        print('Analyzing page {0:.0f} of {1:.0f}'.format((i+page_inc)/page_inc, page_count), end='\r')
        response = req.get(url.format(i))
        parse.count_users(response.text)
        #don't save last page in cache
        if not i == page_max:
            cache.json_save(parse.user_per_year, parse.user_degree, i)

parse.report()
