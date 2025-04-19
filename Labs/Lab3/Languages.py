def difficult_languages (aList):
    global language_list
    for i in aList:
        language_list.remove(i)
    

language_list = ["french", "spanish", "english", "german", "russian", "portuguese"]

print("current list of languages: ", language_list) # prints the current list of languages

print("difficult languages: french, russian, german")

print("removing difficult languages from the list of languages we get: ")

difficult_languages(["french", "russian", "german"])

print(language_list) # prints the list of languages
# compares difficult languages to the list of languages and removes the difficult languages from the list of languages
