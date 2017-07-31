#import pandas as pd
#df = pd.read_json('books.json')
#booksurldf = df.iloc[:,5]
#url_json = booksurldf.to_json()

#with open('booksurl.json','w') as f:
#    f.write(url_json)
import json

with open('books.json') as data_file:
    data = json.load(data_file)

print(data[0]['goodreads_book_url'])
print(len(data)) 
