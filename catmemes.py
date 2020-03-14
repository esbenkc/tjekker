# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:20:25 2020

@author: esben
"""
import pytesseract
import tweepy
from PIL import Image, ImageFont, ImageDraw 

# Authenticate to Twitter
auth = tweepy.OAuthHandler("g4SfvJprquMWFghRJaK8AUGiW", "tyO2KCYwxNn5r2VnqR9pnfVx6KHKCQYUBqhP88a7234NBEri01")
auth.set_access_token("1229683640877092865-fDweu5Pe05upadoB9GCdJCdyj6orp0", "aJcG59wrVaeU5upVPBkWw483YiaLw7kA0eaKbUf3vv3g1")

# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
api.list_timeline(api.get_user("elonmusk"))

timeline = api.home_timeline()
#for tweet in timeline:
#    print(f"{tweet.user.name} said {tweet.text}")
    
user = api.get_user("elonmusk")

print("User details:")
print(user.name)
print(user.description)
print(user.location)

memeTexts = ["When your boss says:","\"Stop reading reddit\"","Who's {0}?\nYou're {0}."]
memeImages = []
fontFile = "C:\Windows\Fonts\impact.ttf"

image = Image.open("train/cat.0.jpg")

def writeText(img, text, x = 10, y = 10, size = 48, color = (255,255,255), stroke = (0,0,0), s_w = 1, s_h = 1):
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(fontFile, 48)
    
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

writeText(writeText(image, memeTexts[0]), memeTexts[1], y = 300).save("catmeme.jpg")

# Create a tweet
api.media_upload("catmeme.jpg")

