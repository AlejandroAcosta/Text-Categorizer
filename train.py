# Text Categorizer training file
#
# Run this on the training sequence for a particular corpus and
# the system will use Rocchio TF-IDF to train the system to these particular
# categories and output the trained system in a format that the testing program will be able to read

# import required modules
from TC_System import TC_System

# main method. Goes through the highest level logic of the system, calling functions to do the technical work
def main():
    # TC_provided/corpus1_train.labels OR
    # TC_provided/corpus2_train.labels OR
    # TC_provided/corpus3_train.labels are the training files for this project
    train_name = "TC_provided/corpus1_train.labels" #input("Please enter the name for your trainig file:\n")

    TC = TC_System()
    
    TC.categorize(train_name)
    
    
main()
input("Thou hast finished")
