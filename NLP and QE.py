import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords,wordnet
import pandas 
import re
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")
from sklearn.feature_extraction.text import TfidfVectorizer
from thefuzz import fuzz,process
def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:         
        return None
stop_words=stopwords.words("english")
test_file=pandas.read_csv("Crawled_url4.csv")
h1s=test_file["h1"]
count=0
d={}
index=0
index1=0
for i in range(len(test_file["url"])):
    d[index]=[test_file["url"][i],test_file["h1"][i],test_file["p"][i]]
    test_file["url"][index1]=index
    index+=1
    index1+=1
for i in h1s:
    if(type(i)==str):
        test_file["h1"][count]=re.sub(r"[\w\s]","",test_file["h1"][count])
        test_file["h1"][count]=nltk.pos_tag(word_tokenize(i))
        test_file["h1"][count] = list(map(lambda x: (x[0], pos_tagger(x[1])), test_file["h1"][count]))
    else:
        test_file["h1"][count]=[]
    newstr=""
    for tup in test_file["h1"][count]:
        word=tup[0]
        word=word.lower()
        if(word not in stop_words):
            try:
                newstr+=(lemmatizer.lemmatize(word))+" "
            except KeyError:
                pass
    test_file["h1"][count]=newstr
    count+=1

user_query=(input("Enter Your Query:  ")).split()

for i in range(len(user_query)):
    user_query[i]=user_query[i].lower()
    user_query[i]=lemmatizer.lemmatize(user_query[i])

user_text=""
for i in user_query:
    user_text+=i+" "

ans=process.extract(user_text,test_file["h1"],limit=10,scorer=fuzz.token_set_ratio)
for i in ans:
    print("   ",d[i[2]][1],end="\n\n")
    print("       ",d[i[2]][0],end="\n\n")
    print("   ",d[i[2]][2][:200],"...",end="\n\n")
    print("---------------------------------------------------------------------------",end="\n\n")


