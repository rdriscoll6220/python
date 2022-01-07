from textblob import TextBlob

with open('/home/ron/repos/python/textBlob/roberts.txt', 'r') as text1:
    content = text1.read()
blob = TextBlob(content)

a = blob.detect_language()
print(a)
b = blob.tags
print(b)
c = blob.noun_phrases
print(c)
d = blob.sentences
print(d)


