import re, sys, requests
from requests.exceptions import ReadTimeout

filename = sys.argv[1]
foundUrls = [];
resolvedUrls = {}
invalidUrls = [];
fileData = None
regex = re.compile(r"http:\/\/www.nessus.org\/u.*")

print("opening File " + filename)

with open(filename, 'r') as file:
    fileData = file.read()

results = regex.findall(fileData)

for result in results:
    foundUrls.append(result.replace('</see_also>', '').strip())

foundUrls = list(set(foundUrls))

print('Found ' + str(len(foundUrls)) + ' URLS')

print('Resolving')

session = requests.Session()

for url in foundUrls:
    resp = session.head(url, allow_redirects=True).url
    try: 
        resolvedUrls[url] = requests.get(resp, timeout=10).url
        print(resolvedUrls[url])
    except ReadTimeout:
        print('Count not resolve due to timeout: ' + url)
        invalidUrls.append(url)

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