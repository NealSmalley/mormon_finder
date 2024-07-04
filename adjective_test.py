import spacy
import textacy
from textacy.extract import token_matches

#test for people, prophet and scripture examples

#add section that elimates Mormons word

text = """Mormon pioneer. Mormon communities. Mormon movement. Mormons. Mormon creativity. The Mormon Church. Mormon leaders. Mormon families. Mormon Country. The Mormon commonwealth. Mormon attitude. Mormon economy. Mormon. Mormon officials. Mormon history. Mormon policy. Mormon settlements."""

text = text.replace("\n\n", " ").replace("\n", " ")

nlp = spacy.load("en_core_web_sm")

doc = nlp(text)
sentences = list(doc.sents)
sentence = (sentences[1])
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


def remove_people_mormon(all_mormon_reference):
    patterns = [[{"POS":"PROPN"}, {"POS": "PROPN"}], [{"POS":"PROPN"}, {"POS": "NOUN"}]]
    # patterns2 = [[{"POS":"PROPN"}, {"POS": "ADV"}], [{"POS":"PROPN"}, {"POS": "VERB"}]]
    mormon_peoples = token_matches(doc, patterns=patterns)
    #print(str(mormon_peoples))

    for mormon_people in mormon_peoples:
           #print(mormon_people)
           if "Mormon" in str(mormon_people):
              print(mormon_people)
              remove_people_list.append(mormon_people)
              #print(remove_people_list)
              #print("This is separate")

    for mormon_mention in all_mormon_reference:
        for mormon_remove in remove_people_list:
            if mormon_remove not in mormon_mention:
                final_remove_people_list.append(mormon_remove)
    unique_mormon_mentions = remove_duplicates(final_remove_people_list)
    return unique_mormon_mentions

def remove_duplicates(items):
        """Remove duplicate items from a list."""
        #print(items)
        seen = set()
        unique_items = []
        for item in items:
            item = str(item).strip()
            if item not in seen:
                unique_items.append(item)
                seen.add(item)
        #print(unique_items)
        return unique_items


    
    # print("  ")  
    # print("Prophet or Scripture")
    # print("  ")  
    # verb_phrases2 = token_matches(doc, patterns=patterns2)

    # for verb_phrase2 in verb_phrases2:
    #      if "Mormon" in str(verb_phrase2):
    #          print(verb_phrase2)


def all_together(sentences):
    all_mormon_reference = all_mormons(sentences)
    removed_people_list = remove_people_mormon(all_mormon_reference)
    #print(removed_people_list)

all_together(sentences)