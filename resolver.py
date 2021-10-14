import re, sys, requests
from requests.exceptions import ReadTimeout

filename = sys.argv[1]
foundUrls = [];
resolvedUrls = {}
invalidUrls = [];
fileData = None

print("opening File " + filename)

with open(filename, 'r') as file:
    fileData = file.read()

results = re.findall(r"((http|https):\/\/www.nessus.org\/u.*[^<\/see_also>|\n])", fileData)

for result in results:
    foundUrls.append(result[0])

foundUrls = list(set(foundUrls))

print('Found ' + str(len(foundUrls)) + ' URLS')

print('Resolving')

session = requests.Session()

for url in foundUrls:
    resp = session.head(url, allow_redirects=True).url
    try: 
        resolvedUrls[url] = requests.get(resp, timeout=10).url
        print(url + ' - ' + resolvedUrls[url])
    except:
        print('Count not resolve: ' + url)
        pass


print('Replacing References')

for original, resolved in resolvedUrls.items():
    fileData = fileData.replace(original, resolved)

if len(invalidUrls):
    print('Removing Invalid References')
    for url in invalidUrls:
        fileData = fileData.replace(url, '')

f = open('resolvedReferences.nessus', 'w')
f.write(fileData)
f.close()

print('Complete!')