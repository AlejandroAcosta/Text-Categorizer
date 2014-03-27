# Text Categorizer training file
#
# Run this on the training sequence for a particular corpus and
# the system will use Rocchio TF-IDF to train the system to these particular
# categories and output the trained system in a format that the testing program will be able to read

# import required modules
from TC_System import TC_System

# main method. Goes through the highest level logic of the system, calling functions to do the technical work
def main():
    train_name = input("Please enter the name for your training file: ")

    TC = TC_System()

    print("Please wait as I process your corpus")
    Cat_vector = TC.categorize(train_name)
    print("Categorization complete")


    print("Your system is being trained...")
    TC.train(Cat_vector)
    print("Your system has been trained.")

    out_name = input("What name would you like to give the trained system?: ")
    TC.write_trained(out_name)

    print("Mission Accomplished.\nThank you for choosing us " \
      "for your text categorization needs.")  
    
main()
input("Your task has been shoved off this mortal coil\n")
