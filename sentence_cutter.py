import spacy
import string

# Load a pre-trained SpaCy model
nlp = spacy.load('en_core_web_sm')

# Example text
text = """Alma was a prophet who compiled the Book of Mormon text text. The Book of Mormon is considered scripture by members of the Church of Jesus Christ of Latter day Saints."""

# Process the text
doc2 = nlp(text)
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
    if direction == "left":
        for i in range(index, -1, -1):
            #print(doc[i].text + " " + str(i))
            if doc[i].text in string.punctuation:
                #print(doc[i].text + " " + str(i))
                return i+1
        return 0
    elif direction == "right":
        for i in range(index, len(doc)):
            #print(doc[i].text + " " + str(i))
            if doc[i].text in string.punctuation:
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
        print("space")
        print(surrounding_words)
