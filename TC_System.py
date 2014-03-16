# Text Categorizer class

import nltk

class TC_System:
    """A Text Categorization System that implements training and testing functionality"""

    # Constants 
    STOPLIST = set(nltk.corpus.stopwords.words('english'))

    # Variables defining the system 
    Categories = [] # vector of the different categories that exist
    Cat_vector = {} # category vector: contains list of documents corresponding to each category
    Prototype = {} # prototype vector representing trained system
    Bag-o-words = [] # list of all words in corpus


    # Constructor
    def __init__(self):
        print("This is your captain speaking. Please enjoy your ride as we " \
              "utilize this text categorization system")

    # prints the data members of the class for debuggin purposes
    def __str__(self):
        rep = str(self.Categories)+str(self.Cat_vector)
        return rep
        
    def categorize(self, train_name):
        # open file, read from it, and then close it
        train_file = open(train_name, "r")
        documents = train_file.readlines()
        train_file.close()

        # determine which categories exist
        # ASSUMING ONLY SPACE THAT EXISTS SEPARATES FILE NAME AND CATEGORY
        for item in documents:
            # parsing the string
            space_location = item.find(" ")
            document_name = item[2:space_location] # ignoring "./" at beginning of document path
            doc_cat = item[space_location+1:-1]

            # determining if category has been encountered
            if doc_cat not in self.Categories:
                self.Categories.append(doc_cat)
                self.Cat_vector[doc_cat] = [] # add an empty list to the category vector

            self.Cat_vector[doc_cat].append(document_name)

        print("Categorization complete")

    # will train the dataset
    def train(self):
        # compile the wordlist

        # compute the document vector for every document
        doc_vector = __TF_IDF(self.wordlist, self.Cat_vector)

        for category in Categories:
            for document in Cat_vector[category]:
                # add up the category vector to create the prototype vector
                
        print("Your system has been trained")

    # write train 
    def write_trained(self, out_filename):
        print("Mission Accomplished.\nThank you for choosing us " \
              "for your text categorization needs.")

    # will unpickle the object representing the trained system and load it up
    def load(self, trained_name):
        print("this will unpickle the required object(s)")

    def test(self):
        print("this is test")

    def __fill_wordlist(self):
        print("I'm gonna fill you up")
        
    def __TF_IDF(self, wordlist, Cat_vector): #figure out these parementers
        print("this is TF*IDF")

