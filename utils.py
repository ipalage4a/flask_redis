from urllib.parse import urlparse

def decode_from_bin(data):
    return [ x.decode('utf-8') for x in data ]

def get_domain_from_url(url):
    if "//" in url:
        return urlparse(url).netloc.replace("www.","")
    else:
        return urlparse(f'//{url}').netloc.replace("www.", "")

