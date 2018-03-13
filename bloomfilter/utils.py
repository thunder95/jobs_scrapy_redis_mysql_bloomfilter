import re,urlparse

#crawl more pages
MORE_PAGE = True

#build url params
def crate_params(pos, params):
    plist = []
    plist.append(pos)

    for item in params:
        plist.append(str(item))

    return '~'.join(plist)

#get number from a string
def get_num(string):
    if string.find('?') > 0:
            string = string.split('?')[0]

    nums = re.findall(r'\d+', string)
    return nums[0]

# set empty string as default value
def getVal(data):
        return data if data else ''

#get url parameters
def get_qs(url):
    query = urlparse.urlparse(url).query
    return dict([(str(k),str(v[0])) for k,v in urlparse.parse_qs(query).items()])

def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()