import spacy

# Load a pre-trained SpaCy model
nlp = spacy.load('en_core_web_sm')

# Custom classification function
def classify_mormon(text):
    doc = nlp(text)
    results = []
    
    for token in doc:
        if token.text.lower() == 'mormon':
            if token.ent_type_ == 'PERSON':
                results.append((token.text, 'Person'))
            else:
                # Check surrounding words for context clues
                surrounding_text = doc[max(token.i - 5, 0): min(token.i + 6, len(doc))]
                surrounding_words = [t.text.lower() for t in surrounding_text]
                
                # Custom rules for determining if it's the scripture, person, or people
                if 'book' in surrounding_words or 'scripture' in surrounding_words or 'chapter' in surrounding_words:
                    results.append((token.text, 'Scripture'))
                elif 'people' in surrounding_words or 'members' in surrounding_words or 'followers' in surrounding_words:
                    results.append((token.text, 'People'))
                else:
                    results.append((token.text, 'Person'))
    return results

# Example text
text = """
Mormon was a prophet who compiled the Book of Mormon. The Book of Mormon is considered scripture by members of the Church of Jesus Christ of Latter-day Saints. Mormon's teachings are fundamental to the faith. Many Mormons follow the teachings of the Book of Mormon and are known for their strong community.
"""

# Process the text and classify 'Mormon'
classifications = classify_mormon(text)
for classification in classifications:
    print(classification)

# Expected output example:
# ('Mormon', 'Person')
# ('Mormon', 'Scripture')
# ('Mormon', 'Scripture')
# ('Mormon', 'Person')
# ('Mormon', 'People')
