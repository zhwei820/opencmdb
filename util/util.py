import hashlib

def handle_uploaded_file(f):
    img_url = 'media/image/' + CalcMD5(f) + f._name
    with open(img_url, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return ('/' + img_url, f._name)

def CalcMD5(f):
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    hash = md5obj.hexdigest()
    return hash