# Text Categorizer testing file
#
# After training the system for your particular corpus, run this system
# and it will load the trained system and apply it to a set of documents
# in order to categorize them. It will output the categories in the same format
# as the initial training set

#import required modules
from TC_System import TC_System

# main method. Goes through highest level logic of the system
def main():
    trained_name = input("Please enter the name of your trained file: ")
    TC = TC_System()

    print("Please wait as I load the trained system...")
    TC.load(trained_name)
    print("Your system has been loaded.")

    test_name = input("Please enter the name of the testing file: ")
    print("Please wait as I process the data to be tested...")
    category_vector = TC.test(test_name)
    print("Data tested")
    
    out_name = input("What would you like to call your results?: ") 
    print("Writing out your categorized data...")
    TC.write_tested(out_name, category_vector)

main()
input("Your task has been shuffled off the mortal coil\n")
