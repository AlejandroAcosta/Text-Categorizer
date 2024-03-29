# Text Categorizer class

import nltk, math, pickle, os

use_stoplist = True # using it reduces accuracy alone to ~82.39%
use_stemming = True  # porter stemming improved accuracy along to ~82.62%
use_POS_tagging = False # using it reduces speed and does not noticeably change accuracy
use_lower = False    # Makes no difference

# stoplist + stemming = 82.84% relatively speedy
# stoplist + stemming + lower = 82.39%
# stoplist + stemming + lower + POS = 81.94% slow as fuck
# stoplist + stemming + POS = 81.72% slow as fuck
# stoplist = 81.72% relatively speedy
# stemming = 81.72% relatively speedy
# POS =  81.94% slow as fuck
# lower =  82.39% relatively speedy
# none = 82.39% relatively speedy
class TC_System:
    """A Text Categorization System that implements training and testing functionality"""

    # Constants 
    __STOPLIST = set(nltk.corpus.stopwords.words('english'))

    # Variables defining the system 
    Categories = []     # vector of the different categories that exist
    Doc_list = []       # list of all the document names
    Prototype = {}      # prototype vector representing trained system
    Bag_o_words = []    # list of all words in corpus
    Doc_wordlist = {}   # wordlist associated with every document
    doc_path = ""       # base path for the file being read for training/testing docs
    __TF = {}           # Term Frequency for all words and all documents
    __IDF = {}          # Inverse Document Frequency for all documents

    # Constructor. Modifies the stoplist to remove tokens it doesn't need
    def __init__(self):
        self.__STOPLIST.update(["(", ",", ")", "'s", ".", "-", "--", "n't", \
                                "''", "``", ":", "reuters", "...", "<", ">" \
                                "'"])
        print("This is your captain speaking. Please enjoy your ride as we " \
              "utilize this text categorization system")
        
    def __str__(self):
        """prints the data members of the class for debugging purposes"""
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
        self.doc_path = os.path.basename(os.path.dirname(train_name))
        if(self.doc_path != ""):
            self.doc_path += "/"
            
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

    def load(self, trained_name):
        """ will unpickle the object representing the trained system and load it up"""
        f = open(trained_name, "rb")
        self.Categories = pickle.load(f)
        self.Prototype = pickle.load(f)
        f.close()
        #print("this will unpickle the required object(s)")

    def train(self, category_vector):
        """will train the dataset"""
        # compile the wordlist
        self.__make_wordlist()
        
        # compute the document vector for every document as a dictionary
        # mapping document names to corresponding document vector
        doc_vectors = self.__TF_IDF()

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

    def test(self, test_name):
        """ Will test the documents given to the structure it has learned. """
        # acquire the list of the documents then remove the dot from the filename
        test_file = open(test_name, "r")
        self.Doc_list = test_file.read().splitlines()
        self.Doc_list = [doc[1:] for doc in self.Doc_list]
        self.doc_path = os.path.basename(os.path.dirname(test_name))
        if(self.doc_path != ""):
            self.doc_path += "/"
        test_file.close()

        # create the wordlist from the document list
        self.__make_wordlist()

        # compute the document vector for every document as a dictionary
        # mapping document names to corresponding document vector
        doc_vectors = self.__TF_IDF()

        # calculate and return decision rule
        return self.__decision(doc_vectors)
        
    def write_trained(self, out_filename):
        """  write trained system to file. """
        f = open(out_filename, "wb")
        pickle.dump(self.Categories, f)
        pickle.dump(self.Prototype, f)
        f.close()

    def write_tested(self, out_filename, category_vector):
        """ Writes tested file to output in appropriate format. """
        out_file = open(out_filename, "w")
        for category in self.Categories:
            # adding the period in the filename back in
            category_vector[category] = \
                ["."+document for document in category_vector[category]]
            # formatting the data and writing it to the file
            for document in category_vector[category]:
                out_file.write(" ".join([document, category]))
                out_file.write("\n")
        out_file.close()     

    def __make_wordlist(self):
        """Looks at all the documents available and constructs a wordlist using nltk for assistance"""
        for doc_name in self.Doc_list:                
            # create empty word list for this document
            self.Doc_wordlist[doc_name] = []

            # create function reference for increased speed
            Bag_append = self.Bag_o_words.append
            Doc_append = self.Doc_wordlist[doc_name].append

            # read the file into a string then close the file
            document_path = self.doc_path + doc_name[1:]
            doc_file = open(document_path, "r")
            document = doc_file.read()
            doc_file.close()

            # Segment the document into sentences
            sentence_segmenter = nltk.data.load("tokenizers/punkt/english.pickle")
            doc_sentences = sentence_segmenter.tokenize(document.strip())

            # tokenize each sentence and construct wordlist with chosen added attributes
            for sentence in doc_sentences:
                tokens = nltk.word_tokenize(sentence)
                if use_POS_tagging:
                    tokens = nltk.pos_tag(tokens)
                for word in tokens:
                    if use_lower:   # option to lowercase the words
                        if use_POS_tagging: 
                            word_index = tokens.index(word)
                            word = (word[0].lower(), word[1])
                            tokens[word_index] = word
                        else:
                            word = word.lower()

                    if use_stemming:    # option to use stemming
                        st = nltk.stem.porter.PorterStemmer()
                        if use_POS_tagging: 
                            word_index = tokens.index(word)
                            word = (st.stem(word[0]), word[1])
                            tokens[word_index] = word
                        else:
                            word = st.stem(word)
                        
                    # if option to use stoplist is active use it. else don't
                    if use_stoplist:
                        if use_POS_tagging:
                            stopped = word[0] in self.__STOPLIST
                        else:
                            stopped = word in self.__STOPLIST
                    else:
                        stopped = False
                        
                    if not stopped and word not in self.Bag_o_words:
                        Bag_append(word) # self.Bag_o_words.append(word)
                        
                    # make wordlist for every document (with repeats)
                    if not stopped:
                        Doc_append(word) # self.Doc_wordlist[doc_name].append(word)
                        
    def __TF_IDF(self):#, wordlist, Cat_vector):
        """ Will compute the TF*IDF value and return the document vectors (containing word weights)"""    
        DF = {} # create an empty document frequency vector for words
        for document in self.Doc_list:
            Doc_count = self.Doc_wordlist[document].count
            for word in set(self.Doc_wordlist[document]):
                # computing TF
                try: # test to see if document has TF vector
                    self.__TF[document][word] = Doc_count(word)
                except KeyError: # create one if it doesn't and add the count
                    self.__TF[document] = {}
                    self.__TF[document][word] = Doc_count(word)

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
            for word in self.Doc_wordlist[document]:
                Doc_vectors[document][word] = \
                    self.__TF[document][word]*self.__IDF[word]
        return Doc_vectors            

    def __decision(self, d_prime):
        """ Applies the decision rule and places documents in appropriate category"""
        category_vector = {}    # dict of categories to list of docs        
        H = 0
        for document in self.Doc_list:
            doc_max = 0 # temp variable for finding max
            for category in self.Categories:
                # ||c|| = sqrt(sum(c_i^2))
                proto_mag = sum([val**2 for val in self.Prototype[category].values()])**0.5
                #proto_mag = sum(self.Prototype[category].values()**2)**0.5#||c||

                # calculating the similarity value
                for word in self.Doc_wordlist[document]:
                    try:
                        H += d_prime[document][word]*self.Prototype[category][word]
                    # except NameError: # H hasn't been initialized yet
                    #    H = d_prime[document][word]*self.Prototype[category][word]
                    except KeyError: # word doesn't show up in prototype vector
                        pass         # do nothing. treating non-present word as 0

                # normalizing the value
                H /= proto_mag

                # determining if this is max
                if H > doc_max:
                    doc_max = H
                    doc_cat = category

            try:
                category_vector[doc_cat].append(document)
            except KeyError:
                category_vector[doc_cat] = [document]

        return category_vector
    
if __name__ == "__main__":
    print("You ran this module directly. I'm afraid I can't let you do that.")
    input("Press the enter key to exit now.")
