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
    trained_name = input("Please enter the name of your trained file.")
    test_name = input("Please enter the name of the data you're testing.")
    TC = TC_System()

    print("Please wait as I load the trained system...")
    TC.load(trained_name)
    print("Your system has been loaded.")

    print("Please wait as I process the data to be tested...")
    TC.test(test_name)
    print("Data tested")

    out_name = input("What would you like to call the tested data?") 
    print("Writing out your categorized data...")
    TC.write_tested(out_name)

main()
input("Thou hast finished")
