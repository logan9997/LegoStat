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