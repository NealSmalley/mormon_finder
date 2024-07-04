import spacy
import textacy
from textacy.extract import token_matches
import re
import webbrowser
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import csv
import queue
import time
import random
from requests_html import HTMLSession
import os
from openai import OpenAI
from itertools import chain

#test for people, prophet and scripture examples

#add section that elimates Mormons word
patterns = [r'Book of Mormon']

#SUGGESTIONS:
#add the propernoun noun function to get rid of mormon scripture
#add [b][B] to regex for flexibility
#caught words of mormon



#text = """when he read the scripture."""

for i in range(1001, 1002):
    i = str(i)
    url = "http://byu-studies-frontend.s3-website-us-west-2.amazonaws.com/article/"+i
    webbrowser.open(url)

    #scrapes the page
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render(sleep=.50)

        soup = BeautifulSoup(response.html.html, 'html.parser')
        article = soup.find(class_='text-lg article lg:min-w-[600px] pb-10')
        article_text = article.text
    except Exception as e:
            print(f"An error occurred: {str(e)}")
    finally:
        session.close()
    text = article_text.replace("\n\n", " ").replace("\n", " ")

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    sentences = list(doc.sents)
    #sentence = (sentences[1])
    all_mormon_sentences = []
    remove_people_list = []
    final_remove_people_list = []
    clean_final_remove_people_list = []



    def all_mormons(sentences):
        for specific_sentence in sentences:
            #print(specific_sentence)
            if "Mormon" in str(specific_sentence):
                #print(specific_sentence)
                #print("This is separate")
                all_mormon_sentences.append(specific_sentence)
        #print(all_mormon_sentences)
        return all_mormon_sentences

    def remove_BOM(all_mormon_sentences):
        all_mormon_sentences_string = ''.join(map(str, all_mormon_sentences))
        #print(all_mormon_sentences_string)
        for pattern in patterns:
                matches = re.findall(pattern, all_mormon_sentences_string)
                if matches:
                    replaced_BOM_reference = all_mormon_sentences_string.replace("Book of Mormon", "")
                    #print(replaced_BOM_reference)
                else:
                    replaced_BOM_reference = all_mormon_sentences_string
                    #print("broken")
        #print(replaced_BOM_reference)
        return replaced_BOM_reference

    # Custom classification function
    def classify_mormon(replaced_BOM_reference):
        doc2 = nlp(replaced_BOM_reference)
        #print(doc2)
        results_prophet = []
        results_scripture = []
        results_people = []


        
        for token in doc2:
            if token.text.lower() == 'mormon':
                if token.ent_type_ == 'PERSON':
                    results_prophet.append((token.text, 'Person'))
                    #print(results)
                else:
                    # Check surrounding words for context clues
                    surrounding_text = doc2[max(token.i - 5, 0): min(token.i + 6, len(doc2))]
                    surrounding_words = [t.text.lower() for t in surrounding_text]
                    
                    # Custom rules for determining if it's the scripture, person, or people
                    if 'book' in surrounding_words or 'scripture' in surrounding_words or 'chapter' in surrounding_words:
                        results_scripture.append(token.text)
                        print(surrounding_words)
                        print(results_scripture)
                    elif 'people' in surrounding_words or 'members' in surrounding_words or 'followers' in surrounding_words:
                        results_people.append((token.text, 'People'))
                        #print(surrounding_words)
                    else:
                        results_prophet.append((token.text, 'Person'))
        #print(results_scripture)
        return results_scripture

    def final_function(classified_mormon_sentences):
        if classified_mormon_sentences != []:
            for item in classified_mormon_sentences:
                if item == "Mormon":
                    classified_mormon_sentences = ["Mormon+"+str(i)]
        elif classified_mormon_sentences == []:
            classified_mormon_sentences = ["No Mormon scripture references+"+str(i)]
            #print("No Mormon scripture references")
        else:
            print("broken final")
        return classified_mormon_sentences

    all_mormon_sentences = all_mormons(sentences)
    mormon_sentences_without_BOM = remove_BOM(all_mormon_sentences)
    #print(mormon_sentences_without_BOM)
    classified_mormon_sentences = classify_mormon(mormon_sentences_without_BOM)
    final_function_result = final_function(classified_mormon_sentences)
    #print(final_function_result)

    #print(final_function_result)
            