from textblob import TextBlob

with open('/home/ron/repos/python/textBlob/roberts.txt', 'r') as text1:
    content = text1.read()
blob = TextBlob(content)
b = blob.tags
print(b[0][0] + ' ' + b[0][1])

      

