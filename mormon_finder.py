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

#opens all urls
#5618
for i in range(5, 5618):
    i = str(i)
    url = "http://byu-studies-frontend.s3-website-us-west-2.amazonaws.com/article/"+i
    #webbrowser.open(url)

#scrapes the page
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=.50)

    soup = BeautifulSoup(response.html.html, 'html.parser')
    article = soup.find(class_='text-lg article lg:min-w-[700px] pb-10')
    article_text = article.text

    def pattern_matching(article_text):
        all_matches = []
        patterns = [
            r'Mormon(?!\s+Church\b)(?!\s*\d)',
            ]
        for pattern in patterns:
            matches = re.findall(pattern, article_text)
            if matches:
                #print(matches)
                all_matches.extend(matches)
        if matches == False:
                all_matches = ["No scriptures"]
        #print(all_matches)
        return all_matches
    

    def abreviation_remover(unique_items):
        replaced_unique_items = []
        patterns_abreviation = r'\b([1-3]?\s*[A-Za-z]+\s?[A-Za-z]+?\s?+[A-Za-z]+\.?\s?\d*?)$'
        #print(unique_items)
        for unique_item in unique_items:
            unique_item = unique_item.strip()
            #print(unique_item)
            matches_abreviation = re.findall(patterns_abreviation, unique_item)
            #print(matches_abreviation)
            if matches_abreviation:
                unique_item = unique_item.replace("Morm.", "Mormon")
                replaced_unique_items.append(unique_item)
                #print(replaced_unique_items)
            else:
                replaced_unique_items.append(unique_item)
        return replaced_unique_items

    def remove_duplicates(items):
        """Remove duplicate items from a list."""
        #print(items)
        seen = set()
        unique_items = []
        for item in items:
            
            if item not in seen:
                unique_items.append(item)
                seen.add(item)
        #print(unique_items)
        return unique_items

    def process_scriptures(article_text):
        pattern_matched = pattern_matching(article_text)
        #print(pattern_matched)
        abreviation_removed = abreviation_remover(pattern_matched)
        abreviation_removed = [item for item in abreviation_removed if item]
        #print(abreviation_removed)
        final_scriptures = remove_duplicates(abreviation_removed)
        if final_scriptures == []:
            final_scriptures = ["No scriptures"]
        return final_scriptures

    scriptures = process_scriptures(article_text)
    #print(scriptures)
    matches_string = ", ".join(scriptures)
    with open('mormon_finder.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([matches_string])
                writer.writerow(["+"])
                writer.writerow([i])
    print(matches_string)