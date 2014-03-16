# Text Categorizer class

import nltk, math

class TC_System:
    """A Text Categorization System that implements training and testing functionality"""

    # Constants 
    STOPLIST = set(nltk.corpus.stopwords.words('english'))

    # Variables defining the system 
    Categories = [] # vector of the different categories that exist
    Cat_vector = {} # category vector: contains list of documents
                    # corresponding to each category
    Prototype = {} # prototype vector representing trained system
    Bag_o_words = [] # list of all words in corpus
    Doc_wordlist = {} # wordlist associated with every document
    __TF = {} # Term Frequency for all words and all documents
    __IDF = {} # Inverse Document Frequency for all documents

    # Constructor
    def __init__(self):
        print("This is your captain speaking. Please enjoy your ride as we " \
              "utilize this text categorization system")
        
    def __str__(self):
        """prints the data members of the class for debugging purposes"""
        rep = str(self.Bag_o_words) + str(self.__TF)
        return rep
        
    def categorize(self, train_name):
        """open file, read from it, and then close it"""
        train_file = open(train_name, "r")
        documents = train_file.readlines()
        train_file.close()

        # determine which categories exist
        # ASSUMING ONLY SPACE THAT EXISTS SEPARATES FILE NAME AND CATEGORY
        for item in documents:
            # parsing the string
            space_location = item.find(" ")
            document_name = item[1:space_location] # ignoring "." at beginning of document path
            doc_cat = item[space_location+1:-1]

            # determining if category has been encountered
            if doc_cat not in self.Categories:
                self.Categories.append(doc_cat)
                self.Cat_vector[doc_cat] = [] # add an empty list to the category vector

            self.Cat_vector[doc_cat].append(document_name)

        print("Categorization complete")

    def train(self):
        """will train the dataset"""
        # compile the wordlist
        self.__make_wordlist()
        
        # compute the document vector for every document as a dictionary
        # mapping document names to corresponding document vector
        doc_vectors = self.__TF_IDF(self.Bag_o_words, self.Cat_vector)

##        for category in Categories:
##            prototype[category] = []
##            for document in Cat_vectors[category]:
##                for i in range(len(doc_vectors[document])):
##                    prototype[category][i] += doc_vectors[document][i]

                # add up the category vector to create the prototype vector
                
        print("Your system has been trained")

    def write_trained(self, out_filename):
        """  write trained system to file. """
        print("Mission Accomplished.\nThank you for choosing us " \
              "for your text categorization needs.")

    def load(self, trained_name):
        """ will unpickle the object representing the trained system and load it up"""
        print("this will unpickle the required object(s)")

    def test(self):
        """ Will test the documents given to the structure it has learned. """
        print("this is test")

    def __make_wordlist(self):
        """Looks at all the documents available and constructs a wordlist using nltk for assistance"""
        for category in self.Categories:
            for doc_name in self.Cat_vector[category]:
                # create empty word list for this document
                self.Doc_wordlist[doc_name] = []
                
                # read the file into a string then close the file
                doc_path = "TC_provided" + doc_name
                doc_file = open(doc_path, "r")
                document = doc_file.read()
                doc_file.close()

                # Segment the document into sentences
                sentence_segmenter = nltk.data.load("tokenizers/punkt/english.pickle")
                doc_sentences = sentence_segmenter.tokenize(document.strip())

                # tokenize each sentence
                for sentence in doc_sentences:
                    tokens = nltk.word_tokenize(sentence)
                    for word in tokens:
                        if word not in self.Bag_o_words:
                            self.Bag_o_words.append(word)
                            
                        # make wordlist for every document (with repeats)
                        self.Doc_wordlist[doc_name].append(word) 
                            

        # strip words in the stoplist from the bag-o-words and document word vectors
        for stop_sign in self.STOPLIST:
            try:
                self.Bag_o_words.remove(stop_sign)
            except ValueError: # raised if stop_sign not in bag-o-words
                pass
                        
                
    def __fill_wordlist(self):
        """ Will populate the word list used by the system"""
        print("I'm gonna fill you up")
        
    def __TF_IDF(self, wordlist, Cat_vector):
        """ Will compute the TF*IDF value and return the document vectors (containing word weights)"""    
        for category in self.Categories:
            for document in self.Cat_vector[category]:
                DF = {} # create an empty document frequency vector for words
                for word in self.Bag_o_words:
                    # computing TF
                    try: # test to see if document has TF vector
                        len(self.__TF[document])
                    except KeyError: # create one if it doesn't
                        self.__TF[document] = {}
                    finally: # and finally add the wordcount to it
                        self.__TF[document][word] = self.Doc_wordlist[document].count(word)

                    # computing DF
                    if word in Doc_wordlist[document]:
                        try:    # increment the DF since word in doc
                            DF[word] += 1
                        except KeyError: # initialize DF to 1
                            DF[word] = 1
                            
                # compute IDF
                for word in self.Bag_o_words:
                   # self.__IDF =
        print("this is TF*IDF")

