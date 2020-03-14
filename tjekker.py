# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:20:25 2020

@author: esben
"""

from PIL import Image, ImageFont, ImageDraw 
import pandas as pd, nltk, numpy as np, tweepy, pytesseract
from nltk.stem import SnowballStemmer

def AnalyzeSentiment():    
    tweets = pd.read_csv('200314-coronadk.csv', encoding='ISO-8859-1')
    sent_list = []
    for tweet in tweets['text']:
        sent_list.append(sentidaV2(tweet, output = "total"))
    tweets = tweets.assign(sentiment = sent_list)
    over10 = tweets.loc[tweets['sentiment'] < -5]
    print (over10['text'])

# Authenticate to Twitter
auth = tweepy.OAuthHandler("g4SfvJprquMWFghRJaK8AUGiW", 
                           "tyO2KCYwxNn5r2VnqR9pnfVx6KHKCQYUBqhP88a7234NBEri01")
auth.set_access_token("1229683640877092865-2U3mUcMp4XQBFNf74EqjXyrnrNWwJi", 
                      "rYopCzidCZUHuqQ0Up7Z3PfIaTnRbL5E7dng4tzBcUZ7D")

# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
  
# print(api.me())
# api.list_timeline(api.get_user("elonmusk"))

# timeline = api.home_timeline()
#for tweet in timeline:
#    print(f"{tweet.user.name} said {tweet.text}")
'''
user = api.get_user("elonmusk")

print("User details:")
print(user.name)
print(user.description)
print(user.location)
'''
memeTexts = ["Hov hov hov hov, min ven...","\"XXX\", \"XXX\", \"XXX\" er vist\nikke venlige ord at sige.","Who's {0}?\nYou're {0}."]
memeImages = []
fontFile = "C:\Windows\Fonts\impact.ttf"

image = Image.open("botman.jpg")

def GenerateImage(img, text, x = 65, y = 10, size = 86, color = (255,255,255), stroke = (0,0,0), s_w = 5, s_h = 5):
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(fontFile, size)
    
    # Stroke HACK
    draw.text((x - s_w, y), text, stroke, font = font)
    draw.text((x + s_w, y), text, stroke, font = font)
    draw.text((x, y - s_h), text, stroke, font = font)
    draw.text((x, y + s_h), text, stroke, font = font)
    
    draw.text((x + s_w, y + s_h), text, stroke, font = font)
    draw.text((x + s_w, y - s_h), text, stroke, font = font)
    draw.text((x - s_w, y + s_h), text, stroke, font = font)
    draw.text((x - s_w, y - s_h), text, stroke, font = font)
    
    draw.text((x, y), text, color, font = font)
    
    return img
    # img.save(save)

GenerateImage(GenerateImage(image, memeTexts[0]), memeTexts[1], y = 800).save("botman_edit.jpg")

# Create a tweet
api.media_upload("botman_edit.jpg")

def ChooseTweet():
    print("Choosing tweet and returning ID")

def InitializeText():
    print("Returns text to print on image")

def PostTweet():
    print("Posting tweet as response")














        
        
        
        
###############################################################################

#################
### CONSTANTS ###
#################

B_INCR = 0.293
B_DECR = -0.293

C_INCR = 0.733
N_SCALAR = -0.74

QM_MULT = 0.94
QM_SUCC_MULT = 0.18

EX_INTENSITY = [1.291, 1.215, 1.208]
UP_INTENSITY = 1.733
BUT_INTENSITY = [0.5, 1.5]

N_TRIGGER = "no"

NEGATE = \
    ['ikke', 'ik', 'ikk', 'ik\'', 'aldrig', 'ingen']

ADD = \
    ['og', 'eller']

BUT_DICT = \
    ['men', 'dog']

BOOSTER_DICT = \
    {"temmelig": 0.1, "meget": 0.2, "mega": 0.4, "lidt": -0.2, "ekstremt": 0.4,
     "totalt": 0.2, "utrolig": 0.3, "rimelig": 0.1, "seriøst": 0.3}

SENTIMENT_LADEN_IDIOMS = {}

SPECIAL_CASE_IDIOMS = {}

##############################
### CUSTOM IMPLEMENTATIONS ###
###     STATIC METHODS     ###
##############################

# Function for working around the unicode problem - shoutout to jry
def fix_unicode(df_col):
    return df_col.apply(lambda x: x.encode('raw_unicode_escape').decode('utf-8'))

# Reading the different files and fixing the encoding
aarup = pd.read_csv('aarup.csv', encoding='ISO-8859-1')
intensifier = pd.read_csv('intensifier.csv', encoding='ISO-8859-1')
intensifier['stem'] = fix_unicode(intensifier['stem'])

# Function for modifing sentiment according to the number of exclamation marks:
def exclamation_modifier(sentence):
    ex_counter = sentence.count('!')
    value = 1
#    if ex_counter > 3:
#        ex_counter = 3
    if ex_counter == 0:
        return 1
    for idx, m in enumerate(EX_INTENSITY):
        if idx <= ex_counter:
            value *= m
    return value

# Function for counting the number of question marks in the input:
def question_identifier(sentence):
    return sentence.count('?')

# Function for cleaning the input of punctuation:
def punct_cleaner(sentence):
    table = str.maketrans('!?-+_#.,;:\'\"', 12*' ')
    return sentence.translate(table)

# Function for making letters lower case:
def string_to_lower(sentence):
    return sentence.lower()

# Function for splitting sentences by the spaces:
def split_string(sentence):
    return sentence.split()

# Function for removing punctuation from a sentence and turning it into a 
# list of words
def clean_words_caps(sentence):
    return split_string(punct_cleaner(sentence))

# Function for removing punctuation from a sentence, making the letters lower 
# case, and turning it into a list of words
def clean_words_lower(sentence):
    return split_string(string_to_lower(punct_cleaner(sentence)))

# Function for getting the positions of words that are written in upper case:
def caps_identifier(words):
    positions = []
    for word in words:
        if word.upper() == word:
            positions.append(words.index(word))
    return positions

# Function for modifing the sentiment score of words that are written in 
# upper case:
def caps_modifier(sentiments, words):
    positions = caps_identifier(words)
    for i in range(len(sentiments)):
        if i in positions:
            sentiments[i] *= UP_INTENSITY
    return sentiments

# Function for identifying negations in a list of words. Returns list of 
# positions affected by negator.
def get_negator_affected(words):
    positions = []

    for word in words:
        if word in NEGATE:
            neg_pos = words.index(word)
            positions.append(neg_pos)
            positions.append(neg_pos + 1)
            positions.append(neg_pos - 1)
            positions.append(neg_pos + 2)
            positions.append(neg_pos + 3)
    return positions

# Get all intensifiers
def get_intensifier(sentiments, word_list):
    intensifiers_df = intensifier.loc[intensifier['stem'].isin(word_list)]
    intensifiers = intensifiers_df['stem'].tolist()
    scores = intensifiers_df['score'].tolist()
    position = []

    for word in word_list:
        if word in intensifiers:
            inten_pos = word_list.index(word)

            if inten_pos + 1 not in position:
                position.append(inten_pos + 1)
                if inten_pos + 1 < len(sentiments):
                    sentiments[inten_pos +
                               1] *= scores[intensifiers.index(word)]

            if inten_pos - 1 not in position:
                position.append(inten_pos - 1)
                if inten_pos - 1 > 0:
                    sentiments[inten_pos -
                               1] *= scores[intensifiers.index(word)]

            if inten_pos + 2 not in position:
                position.append(inten_pos + 2)
                if inten_pos + 2 < len(sentiments):
                    sentiments[inten_pos +
                               2] *= scores[intensifiers.index(word)]

            if inten_pos + 3 not in position:
                position.append(inten_pos + 3)
                if inten_pos + 3 < len(sentiments):
                    sentiments[inten_pos+3] *= scores[intensifiers.index(word)]

    return sentiments


# Function for identifying 'men' (but) in a list of words:
def men_identifier(words):
    position = 0
    for word in words:
        if word == 'men':
            position = words.index(word)
    return position

# Function for modifying the sentiment score according to whether the words are 
# before or after the word 'men' (but) in a list of words
def men_sentiment(sentiments, words):
    for i in range(len(sentiments)):
        if i < men_identifier(words):
            sentiments[i] *= BUT_INTENSITY[0]
        else:
            sentiments[i] *= BUT_INTENSITY[1]

    return sentiments
# Need imperical tested weights for the part before and after the 'men's'

# Function for stemming the words of a sentence (stemming is NOT optimal for 
# expanding the vocabulary!):
def stemning(words):
    stemmer = SnowballStemmer('danish')
    return [stemmer.stem(word) for word in words]


# Function that takes a list of words as the input and returns the corresponding 
# sentiment scores
def get_sentiment(word_list):
    sentiment_df = aarup.loc[aarup['stem'].isin(word_list)]
    words = sentiment_df['stem'].tolist()
    scores = sentiment_df['score'].tolist()
    senti_scores = []

    for i in word_list:
        if i in words:
            senti_scores.append(scores[words.index(i)])
        else:
            senti_scores.append(0)

    return senti_scores

'''
Function for turning a text input into a mean sentiment score.

Architecture as following tree:
    output: mean -> mean branch
        Analyzes the text as a single sentence
    output: total || by_sentence_mean || by_sentence_total
        Splits into sentences to analyze each as a single sentence
        Splits branch into output branches

'''
def sentidaV2(text, output = ["mean", "total", "by_sentence_mean", "by_sentence_total"], normal = False):
    
    # Goes into sentence splitting if it's not the global mean output
    if output == "by_sentence_mean" or output == "by_sentence_total" or output == "total":
        sentences = nltk.sent_tokenize(text)
        # The tokenizer splits !!! into two sentences if at the end of the text
        # Remove problem by analyzing, appending, and removing
        if sentences[-1] == "!": 
            sentences[-2] = sentences[-2] + "!"
            del sentences[-1]
        sentences_output = []
        
        # Sentence splitting branch
        for sent in sentences:
            words_caps = clean_words_caps(sent)
            words_lower = clean_words_lower(sent)
            stemmed = stemning(words_lower)
            sentiments = get_sentiment(stemmed)
    
            if men_identifier(words_lower) > 0:
                sentiments = men_sentiment(sentiments, words_lower)
        
            sentiments = get_intensifier(sentiments, stemmed)
            sentiments = caps_modifier(sentiments, words_caps)
            
            if question_identifier(sent) == 0:
                for i in set(get_negator_affected(words_lower)):
                    if i < len(sentiments) and i >= 0:
                        sentiments[i] *= -1
        
            if len(words_lower) == 0:
                sentences_output.append(0)
            
            ex_mod = exclamation_modifier(sent)
            sentiments[:] = [sentiment * ex_mod for sentiment in sentiments if sentiment != 0]
            
            if normal:    
                sentiments = np.multiply([float(i) for i in sentiments], ([0.2]*len(sentiments)))
                sentiments = np.where(sentiments < -1, -1, np.where(sentiments > 1, 1, sentiments))
        
            total_sentiment = sum(sentiments)
            if output == "total" or output == "by_sentence_total":
                sentences_output.append(total_sentiment)
            elif output == "by_sentence_mean" and len(sentiments) != 0: sentences_output.append(total_sentiment / len(sentiments))
            else: sentences_output.append(0)
        
        if output == "by_sentence_mean" or output == "by_sentence_total":
            if len(sentences_output) <= 1:
                return sentences_output[0]
            return sentences_output
        elif output == "total":
            return sum(sentences_output)
        else:
            return sentences_output

    elif output == "mean":
        words_caps = clean_words_caps(text)
        words_lower = clean_words_lower(text)
        stemmed = stemning(words_lower)
        sentiments = get_sentiment(stemmed)

        if men_identifier(words_lower) > 0:
            sentiments = men_sentiment(sentiments, words_lower)
    
        sentiments = get_intensifier(sentiments, stemmed)
        sentiments = caps_modifier(sentiments, words_caps)
    
        if question_identifier(text) == 0:
            for i in set(get_negator_affected(words_lower)):
                if i < len(sentiments) and i >= 0:
                    sentiments[i] *= -1
    
        if len(words_lower) == 0:
            sentences_output.append(0)
        
        ex_mod = exclamation_modifier(text)
        sentiments[:] = [sentiment * ex_mod for sentiment in sentiments if sentiment != 0]
        
        if normal:    
            sentiments = np.multiply([float(i) for i in sentiments], ([0.2]*len(sentiments)))
            sentiments = np.where(sentiments < -1, -1, np.where(sentiments > 1, 1, sentiments))
        
        if len(sentiments) > 0: return sum(sentiments) / len(sentiments)
        else: return 0    
