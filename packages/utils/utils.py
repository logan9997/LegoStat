import time

def clean_html_codes(string:str):
    codes = {
        '&#40;':'(',
        '&#41;':')',
        '&#39;': "'"
    }
    for k, v in codes.items():
        if k in string:
            string = string.replace(k, v)
    return string

def item_type_convert(item_type:str):
    if len(item_type) > 1:
        return {'MINIFIG':'M', 'SET':'S'}[item_type]
    return {'M':'MINIFIG', 'S':'SET'}[item_type]


def timer(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        finish_time = time.time() - start_time
        print(f'<{func.__name__}> Finished in {round(finish_time)} seconds.')
    return inner
    