import json

def json_save(user_per_year, user_degree, page):
    app_data = {}
    app_data['user_per_year'] = user_per_year
    app_data['user_degree'] = user_degree
    app_data['page'] = page
    
    with open('data.json', mode='w', encoding='utf-8') as f:
        json.dump(app_data, f, indent=2)
        
def json_load():
    with open('data.json', mode='r', encoding='utf-8') as f:
        app_data = json.load(f)
        
    return app_data
    
