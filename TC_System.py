# Text Categorizer class

import nltk

class TC_System:
    """A Text Categorization System that implements training and testing functionality"""

    # Constants 
    STOPLIST = set(nltk.corpus.stopwords.words('english'))

    # Variables defining the system
    Categories = []; # vector of the different categories that exist
    Cat_vector = []; # category vector
    Prototype = []; # prototype vector representing trained system

    # Constructor
    def __init__(self):
        print("This is your captain speaking. Please enjoy your ride as we " \
              "utilize this text categorization system")

    # prints the data members of the class for debuggin purposes
    def __str__():
        print(Categories)
        print(Cat_vector)
        
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
            doc_cat = item[space_location:]

            # determining if category has been encountered
            if doc_cat not in self.Categories:
                self.Categories.append(doc_cat)
                self.Cat_vector.append([]) # add an empty list to the category vector

            category_index = self.Categories.index(doc_cat)
            self.Cat_vector[category_index].append(document_name)

        for item in self.Cat_vector:
            print(item)

    # will unpickle the object representing the trained system and load it up
    def load(self, trained_name):
        print("this will unpickle the required object(s)")

    # will train the dataset
    def train(self):
        print("this is train")

    # will train 
    def write_trained(self, out_filename):
        print("this is write output")

    def test(self):
        print("this is test")
    
    def __IDF(self, documents): #figure out these parementers
        print("this is IDF")

    def __TF(self, documents): #figure out these parameters
        print("This is TF)
