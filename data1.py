#import library
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from csv import writer
import spacy


df=pd.read_csv("English_25K.csv")
print(df.head())
col=df['English'].unique()
col=col[5000:25000]
sh=col.shape
print(sh)
for i in range(sh[0]):
  txt=col[i]
  count=0
  for j in txt:
      if(j==" "):
          count=count+1
  if(count>=2 and count<7):
    # List 
    lemmatizer = WordNetLemmatizer()
    stop_words_isl = {"a", "an" ,"the", "is", "am", "are"}

  # Define function to lemmatize each word with its POS tag
 
  # POS_TAGGER_FUNCTION : TYPE 1
    def pos_tagger(word,nltk_tag):
      if word.endswith("ing"):
         return wordnet.VERB
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

    
# sent_tokenize is one of instances of 
# PunktSentenceTokenizer from the nltk.tokenize.punkt module
  
    tokenized = sent_tokenize(txt)

    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []

    for i in tokenized:
      
    # Word tokenizers is used to find the words 
    # and punctuation in a string
      wordsList = nltk.word_tokenize(i)
    
    # removing stop words from wordList
      wordsList = [w for w in wordsList if not w in stop_words_isl] 


    #  Using a Tagger. Which is part-of-speech 
    # tagger or POS-tagger. 
      tagged = nltk.pos_tag(wordsList)
  
    #print(tagged)
    # we use our own pos_tagger function to make things simpler to understand.
      wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[0],x[1])), tagged))
    #print(wordnet_tagged)

      lemmitization_dict = dict()

      for word, tag in wordnet_tagged:
          if tag is None:
            # if there is no available tag, append the token as is
              lemmatized_sentence.append(word)
          else:       
            # else use the tag to lemmatize the token
              lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
              lemmitization_dict[word] = lemmatizer.lemmatize(word, tag)

    
      print(lemmatized_sentence)
    #print(lemmitization_dict)

    
    nlp = spacy.load("en_core_web_sm")



# object and subject constants
    OBJECT_DEPS = {"dobj", "dative", "attr", "oprd","pobj","NN","nummod","npadvmod","det","advmod"}
    SUBJECT_DEPS = {"nsubj", "nsubjpass", "csubj","csubjpass", "agent", "expl", "acomp", "avmod","poss","meta"}
# tags that define wether the word is wh-
    WH_WORDS = {"WP", "WP$", "WRB"}
    q_words={"IS","ARE","HAS","AM","HAVE","HAD"}

# gather the user input and gather the info
    doc = nlp(txt)

# extract the subject, object and verb from the input
    def extract_svo(doc):
      sub = []
      at = []
      ve = []
      list_of_words = txt.split()
      len(list_of_words)
      for i in range(len(doc)):
          if doc[i].pos_ == "VERB":
            if(i<len(doc)-1):
              print(doc[i+1])
              #next_word=
              if((doc[i].pos_=="VERB" and doc[i+1].pos_=="ADP") or (doc[i].pos_=="VERB" and doc[i+1].pos_=="ADV")):
                ve.append(doc[i].text)
                ve.append(doc[i+1].text)
              else:
                ve.append(doc[i].text)

            else:
              ve.append(doc[i].text)
        # is this the object?
          if doc[i].dep_ in OBJECT_DEPS or doc[i].head.dep_ in OBJECT_DEPS:
              at.append(doc[i].text)
        # is this the subject?
          if doc[i].dep_ in SUBJECT_DEPS or doc[i].head.dep_ in SUBJECT_DEPS or doc[i].pos_ == "ADJ":
              sub.append(doc[i].text)
      return " ".join(sub).strip().lower(), " ".join(ve).strip().lower(), " ".join(at).strip().lower()


# wether the doc is a question, as well as the wh-word if any
    def is_question(doc):
    # is the first token a verb?
      if len(doc) > 0 and doc[0].pos_ == "VERB":
          return True, ""
    # go over all words
      for token in doc:
        # is it a wh- word?
          if token.tag_ in WH_WORDS:
              return True, token.text.lower()
      return False, ""

    def is_negation(doc):
     for token in doc:
       
        if token.text=='not' or token.text=="n't" or token.text=='never':
                return True
        
     return False
    is_negation(doc)

    
# print out the pos and deps
    for token in doc:
      print("Token {} POS: {}, dep: {}".format(token.text, token.pos_, token.dep_))

# get the input information
    subject, verb, attribute = extract_svo(doc)
    question, wh_word = is_question(doc)
    print("SVO:, Subject: {}, Verb: {}, Object: {}, Question: {}, Wh_word: {}".format(subject, verb, attribute, question, wh_word))


    if("which" in subject):
      txt_sov = " ".join([attribute.replace(wh_word,""), verb, subject.replace(wh_word,""), wh_word]) 
    elif(wh_word is not None):
      txt_sov = " ".join([subject.replace(wh_word,""), attribute.replace(wh_word,""), verb, wh_word]) 
    else:
      txt_sov = " ".join([subject,attribute, verb])

    for key, value in lemmitization_dict.items():
      txt_sov = txt_sov.replace(key, value)

    isl_list = [w for w in list(txt_sov.split(" ")) if not w in stop_words_isl]

    dict1={"1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine","0":"zero","27":"twenty seven"}
    #print(isl_list)
    isl = ""
    for i in isl_list:
      if i != "":
          for j in dict1:

            if j==i:
              i=dict1[j]
          isl = isl+" "+i
    if(is_negation(doc)):
        print(is_negation(doc))
        isl=isl+" no"

    print(isl)
    List=[txt,isl]
  
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open('dataset.csv', 'a',newline='') as f_object:

      writer_object = writer(f_object)

    # Pass the list as an argument into
    # the writerow()
      writer_object.writerow(List)

  #Close the file object
      f_object.close()