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
import string

#test for people, prophet and scripture examples

#add section that elimates Mormons word
patterns = [r'[bB]ook of Mormon', r'[mM]ormon [sS]cripture']
 
#Note:
#add a range for distance from index like before

#text = """when he read the scripture."""
#for i in range(394, 395):
mormon_scripture_list = [112]
#mormon_scripture_list = [403, 413, 415, 425, 429, 430, 431, 444, 465,466,472,476,482,507,512,514,536,538,542,553,559,563,568,576,588,603,691,725,727,754,757,758,803,846,858,867,892,895,912,938,947,963,1000,1071,1099,1122,1134,1218,1224,1265,1374,1375,1380,1397,1405,1457,1460,1471,1472,1531,1555,1559,1599,1610,1617,1646,1678,1685,1686,1729,1758,1816,1820,1823,1853,3704,3730,3749,3753,3755,3759,3796,3798,3801,3802,3813,3860,3874,3892,3893,4400,4401,4449,4642,4887,4954,4987,5028,5191,5192,5200,5201,5225,5236,5241,5272,5292,5319,5320,5339,5353,5362,5369,5370,5374,5385,5407,5432,5439,5443,5463,5505,5554,5555,5556,5557,5568,5573,5576,5579,5580,5582,5584,5586,5587,5592,5596,5597,5598,5600,5601,5603,5615,5636,5637,5641,5682]
#mormon_scripture_list = [4401,4449,4642,4887,4954,4987,5028,5191,5192,5200,5201,5225,5236,5241,5272,5292,5319,5320,5339,5353,5362,5369,5370,5374,5385,5407,5432,5439,5443,5463,5505,5554,5555,5556,5557,5568,5573,5576,5579,5580,5582,5584,5586,5587,5592,5596,5597,5598,5600,5601,5603,5615,5636,5637,5641,5682]

for i in mormon_scripture_list:
    i = str(i)
    url = "http://byu-studies-frontend.s3-website-us-west-2.amazonaws.com/article/"+i
    #webbrowser.open(url)

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
        pattern = r'\bMormon\b'
        all_mormon_sentences = []

        for specific_sentence in sentences:
            matches = re.findall(pattern, str(specific_sentence), re.IGNORECASE)
            #print(matches)
            if matches:
                all_mormon_sentences.append(specific_sentence)
            
        #print(all_mormon_sentences)
        return all_mormon_sentences
    

    def remove_numbered_scriptures(all_mormon_sentences):
        all_mormon_sentences_string = ""
        for object_spacy_tokens in all_mormon_sentences:
            all_mormon_sentences_string += str(object_spacy_tokens)
        #print(all_mormon_sentences_string)
        patterns = [
            r'Words of [Mm]ormon',
            r'[Bb]ook of [Mm]ormon',
            r'[Mm]ormon (?:[1-9])',
            r'Title Page of the [Bb]ook of [Mm]ormon',
            r'Testimony of the Twelve Apostles from the [Bb]ook of [Mm]ormon'
        ]

        #Book of Mormon is mentioned 58 times
        for pattern in patterns:
                matches = re.findall(pattern, all_mormon_sentences_string)
                #print(matches)
                if matches:
                    for match in matches:
                        all_mormon_sentences_string = all_mormon_sentences_string.replace(match, "")
                        #print(removed_numbered_scriptures)
        #print(removed_numbered_scriptures)
        return all_mormon_sentences_string


    def remove_BOM(all_mormon_sentences):
        all_mormon_sentences_string = ''.join(map(str, all_mormon_sentences))
        #print(all_mormon_sentences_string)
        for pattern in patterns:
                matches = re.findall(pattern, all_mormon_sentences_string)
                if matches:
                    #Note:
                    #add Mormon Scripture
                    replaced_BOM_reference = all_mormon_sentences_string.replace("Book of Mormon", "").replace("book of Mormon", "").replace("book of mormon", "").replace("Mormon scripture", "").replace("mormon scripture", "")
                    #print(replaced_BOM_reference)
                else:
                    replaced_BOM_reference = all_mormon_sentences_string
                    #print("broken")
        return replaced_BOM_reference


    # Custom classification function
    def classify_mormon(replaced_BOM_reference):
        doc2 = nlp(replaced_BOM_reference)
        #print(doc2)
        results_prophet = []
        results_scripture = []
        results_people = []
        sentences = list(doc2.sents)
        surrounding_words_list = []
        #print(sentences)

        for sentence in sentences:
            for token in sentence:
                if token.text.lower() == 'mormon':
                    #print(sentence)
                    #print("space")
                    if token.ent_type_ == 'PERSON':
                        results_prophet.append((token.text, 'Person'))
                        #print(results)
                    else:
                        # Check surrounding words for context clues
                        mormon_index_list = []

                        # Assume we are interested in the token "Mormon"
                        token = None
                        for i, t in enumerate(doc2):
                            #print(str(t)+" "+str(i))
                            if t.text.lower() == 'mormon':
                                token = t
                                mormon_index_list.append(i)
                        #print(mormon_index_list)

                                #break

                        # Function to find nearest punctuation mark
                        def find_nearest_punctuation(doc, index, direction):
                            sentence_ending_punctuation = '.!?'
                            if direction == "left":
                                for i in range(index, -1, -1):
                                    #print(doc[i].text + " " + str(i))
                                    if doc[i].text in sentence_ending_punctuation:
                                        #print(doc[i].text + " " + str(i))
                                        return i+1
                                return 0
                            elif direction == "right":
                                for i in range(index, len(doc)):
                                    if doc[i].text in sentence_ending_punctuation:
                                        #print(doc[i].text)
                                        #print(i)
                                        return i
                                return len(doc)

                        # Extract surrounding words with adjusted range
                        if token:
                            for index in mormon_index_list:
                                start_index = find_nearest_punctuation(doc2, index, "left")
                                #print(start_index)
                                end_index = find_nearest_punctuation(doc2, index, "right")
                                #print(end_index)
                                surrounding_text = doc2[start_index:end_index]
                                #print(surrounding_text)
                                #print("space")
                                surrounding_words = [t.text.lower() for t in surrounding_text]
                                #print(surrounding_words)

                        #surrounding_text = doc2[max(token.i - 5, 0): min(token.i + 6, len(doc2))]
                        #surrounding_words = [t.text.lower() for t in surrounding_text]
                        
                        # Custom rules for determining if it's the scripture, person, or people
                        if 'book' in surrounding_words or 'scripture' in surrounding_words or 'chapter' in surrounding_words:
                            results_scripture.append(token.text)
                            surrounding_words_list.append(surrounding_words)
                            #print(surrounding_words)
                            #print("space")
                            #print(results_scripture)
                        elif 'people' in surrounding_words or 'members' in surrounding_words or 'followers' in surrounding_words:
                            results_people.append((token.text, 'People'))
                            #print(surrounding_words)
                        else:
                            results_prophet.append((token.text, 'Person'))
        def cut_string_before_keywords(text):
            # Define the pattern to match "book", "scripture", or "chapter" (case-insensitive)
            pattern = r'\b(book|scripture|chapter)\b'
            pattern2 = r'\bMormon\b'
            # Search for the pattern in the text
            match = re.search(pattern, text, re.IGNORECASE)
            
            if match:
                # Find the start position of the match
                cut_front = match.start()
                # Return the substring from the cut position onward
                front_cut_result = text[cut_front:]
                match2 = re.search(pattern2, front_cut_result, re.IGNORECASE)

                if match2:
                    cut_back = match2.end()
                    remaining_text = front_cut_result[cut_back:].strip()
                    next_word = re.search(r'\b\w+\b', remaining_text)

                    if next_word:
                        extra_word_end = next_word.end()
                        final_cut_result = front_cut_result[:cut_back+extra_word_end+1]
                        return final_cut_result
                    
            return text
            #else:
                # If no match is found, return the original text
                #return text
        if surrounding_words_list != []:
            surrounding_words_string = ' '.join(surrounding_words_list[0])
            #print(surrounding_words_string)
            print(cut_string_before_keywords(surrounding_words_string))
        else:
            print("No mormon scriptures")

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
    removed_numbered_scriptures = remove_numbered_scriptures(all_mormon_sentences)
    #print(removed_numbered_scriptures)
    mormon_sentences_without_BOM = remove_BOM(removed_numbered_scriptures)
    #print(mormon_sentences_without_BOM)
    classified_mormon_sentences = classify_mormon(mormon_sentences_without_BOM)
    final_function_result = final_function(classified_mormon_sentences)
    print(final_function_result)

    # with open('mormon_finder3real.csv', 'a', newline='') as file:
    #      writer = csv.writer(file)
    #      writer.writerow(final_function_result)
    #  print(final_function_result)