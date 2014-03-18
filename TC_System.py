# Text Categorizer class

import nltk, math, pickle

class TC_System:
    """A Text Categorization System that implements training and testing functionality"""

    # Constants 
    __STOPLIST = set(nltk.corpus.stopwords.words('english'))

    # Variables defining the system 
    Categories = [] # vector of the different categories that exist
    Doc_list = []   # list of all the document names
    #Cat_vector = {} # category vector: contains list of documents
                    # corresponding to each category
    Prototype = {} # prototype vector representing trained system
    Bag_o_words = [] # list of all words in corpus
    Doc_wordlist = {} # wordlist associated with every document
    __TF = {} # Term Frequency for all words and all documents
    __IDF = {} # Inverse Document Frequency for all documents

    # Constructor. Modifies the stoplist to remove tokens it doesn't need
    def __init__(self):
        self.__STOPLIST.update(["(", ",", ")", "'s", ".", "-", "--", "n't", \
                                "''", "``", ":", "reuters", "...", "<", ">"])
        print("This is your captain speaking. Please enjoy your ride as we " \
              "utilize this text categorization system")
        
    def __str__(self):
        """prints the data members of the class for debugging purposes"""
        #print(Doc_wordlist)
        out_file = open("testout.txt","w")
        for doc in self.Doc_wordlist:
            out_file.write(doc + str(self.Doc_wordlist[doc]))
            out_file.write("\n")
        out_file.write("\n")
        out_file.close()
        rep = str("written to testout.txt")
        return rep
        
    def categorize(self, train_name):
        """open file, read from it, and then close it"""
        train_file = open(train_name, "r")
        documents = train_file.readlines()
        train_file.close()

        # category vector containing dictionary mapping categories to documents
        # associated with it
        Cat_vector = {}
        
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
                Cat_vector[doc_cat] = [] # add an empty list to the category vector

            # adding to category vector
            Cat_vector[doc_cat].append(document_name)

            # adding to master document list
            self.Doc_list.append(document_name)
            
        return Cat_vector
        
    def train(self, category_vector):
        """will train the dataset"""
        # compile the wordlist
        self.__make_wordlist()
        
        # compute the document vector for every document as a dictionary
        # mapping document names to corresponding document vector
        doc_vectors = self.__TF_IDF()#self.Bag_o_words, self.Cat_vector)

       # add up the category vector to create the prototype vector
        for category in self.Categories:
            self.Prototype[category] = {}
            #print(category)
            for document in category_vector[category]:
               # print(document)
                for word in set(self.Doc_wordlist[document]):
                    #print(word)
                    try: # add to the prototype vector
                        #print(doc_vectors[document][word])
                        self.Prototype[category][word] += doc_vectors[document][word]
                    except KeyError: # initialize if not yet done
                        #print(doc_vectors[document][word])
                        self.Prototype[category][word] = doc_vectors[document][word]


    def write_trained(self, out_filename):
        """  write trained system to file. """
        f = open(out_filename, "wb")
        pickle.dump(self.Categories, f)
        pickle.dump(self.Prototype, f)
        f.close()
        print("Mission Accomplished.\nThank you for choosing us " \
              "for your text categorization needs.")

    def load(self, trained_name):
        """ will unpickle the object representing the trained system and load it up"""
        f = open(trained_name, "rb")
        self.Categories = pickle.load(f)
        self.Prototype = pickle.load(f)
        f.close()
        print("this will unpickle the required object(s)")

    def test(self):
        """ Will test the documents given to the structure it has learned. """
    
        print("this is test")

    def write_tested(self, out_filename):
        """ Writes tested file to output in appropriate format. """
        pass

    def __make_wordlist(self):
        """Looks at all the documents available and constructs a wordlist using nltk for assistance"""
        for doc_name in self.Doc_list:                
            # create empty word list for this document
            self.Doc_wordlist[doc_name] = []

            # create function reference for increased speed
            Bag_append = self.Bag_o_words.append
            Doc_append = self.Doc_wordlist[doc_name].append

            # read the file into a string then close the file
            doc_path = "TC_provided" + doc_name
            doc_file = open(doc_path, "r")
            document = doc_file.read()
            doc_file.close()

            # Segment the document into sentences
            sentence_segmenter = nltk.data.load("tokenizers/punkt/english.pickle")
            doc_sentences = sentence_segmenter.tokenize(document.strip())

            # tokenize each sentence and construct wordlist sans stoplist words
            for sentence in doc_sentences:
                tokens = nltk.word_tokenize(sentence)
                for word in tokens:
                    word = word.lower()
                    stopped = word in self.__STOPLIST
                    if not stopped and word not in self.Bag_o_words:
                        Bag_append(word) # self.Bag_o_words.append(word)
                        
                    # make wordlist for every document (with repeats)
                    if not stopped:
                        Doc_append(word) # self.Doc_wordlist[doc_name].append(word)                         
                        
    def __TF_IDF(self):#, wordlist, Cat_vector):
        """ Will compute the TF*IDF value and return the document vectors (containing word weights)"""    
        DF = {} # create an empty document frequency vector for words
        for document in self.Doc_list:
            for word in self.Bag_o_words:
                # computing TF
                try: # test to see if document has TF vector
                    len(self.__TF[document])
                except KeyError: # create one if it doesn't
                    self.__TF[document] = {}
                finally: # and finally add the wordcount to it
                    self.__TF[document][word] = self.Doc_wordlist[document].count(word)

                # computing DF
                if word in self.Doc_wordlist[document]:
                    try:    # increment the DF since word is in document
                        DF[word] += 1
                    except KeyError: # initialize DF to 1
                        DF[word] = 1
                            
        # compute IDF
        D_bar = len(self.Doc_wordlist) # |D| : number of documents
        for word in self.Bag_o_words:
            # print(word)
            try:
                self.__IDF[word] = math.log(D_bar/DF[word])
            except ZeroDivisionError:
                print(word)
                self.__IDF[word] = -1

        # compute document word weights
        Doc_vectors = {}
        for document in self.Doc_list:
            Doc_vectors[document] = {} # creating empty dictionary
            for word in self.Bag_o_words:
                Doc_vectors[document][word] = \
                    self.__TF[document][word]*self.__IDF[word]

        return Doc_vectors            

if __name__ == "__main__":
    print("You ran this module directly. I'm afraid I can't let you do that.")
    input("Press the enter key to exit now.")
