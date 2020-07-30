from csv import reader
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

weak_words = []
word_file = open('weak_words.txt', 'r')
for word in word_file:
    weak_words.append(word.strip())
print(weak_words)

f = open("story.txt", "rt") 
story = f.read()
sentences = re.split('(\.|!|\?)', story)
sentences_terminated = [a + b for a,b in zip(sentences[0::2], sentences[1::2])]

def main():
    """For loop to find any instance of weak words in text."""
     
    for sentence in sentences_terminated:
        for word in weak_words:
            if word in sentence:
                print("The word " + str(word) + " is in your story. This is the context...")
                print(sentence + "\n")
                answer = ''
                while answer is not 'y' or 'n':
                    answer = input("Would you like to replace this word for a better one? y/n ")
                    if answer == 'y':
                        thesaurus(word)
                        new_word = input("Enter the word you'd like to use to replace " + word + ": ")
                        replace(word, new_word)
                        break
                    elif answer == 'n':
                        break
                    else:
                        print("Incorrect answer")

    print("You're story looks good now!")

def thesaurus(word):
    """Takes in a the weak word and looks up synonyms on thesaurus.com."""

    driver.get("https://www.thesaurus.com/browse/" + word)

    html_list = driver.find_element_by_class_name("css-17d6qyx-WordGridLayoutBox")
    synonyms = html_list.find_elements_by_tag_name("li")
    syn_list = []
    print("These are the replacemnt words we found...\n")
    for word in synonyms:
        syn_list.append(word.text)
    print(syn_list)
    print("\n")

def replace(word, new_word):
    """Takes in a the weak word and the new word. The weak word gets replaced by the new word."""

    global story 
    story = story.replace(word, new_word, 1)

    global f
    f.close()
   
    f = open("story.txt", "wt") 
    f.write(story)
    f.close()


if __name__ == "__main__":
    main()