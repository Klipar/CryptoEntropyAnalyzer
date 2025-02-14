from src.data_processing_and_visualization import plot_frequencies, save_frequencies_to_file
from src.data_mining import read_bytes_from_file, get_format_char
from src.communication import hello, get_numbers_tuple
from Easy.animations import *
from Easy.massage import *
import sys
import os

def main ():
    result = "Result/"
    if not os.path.exists(result):
        try:
            os.makedirs(result)
        except:
            failed("Failed to create a directory to save the result in the current directory.")
            sys.exit(1)

    # Check if the argument was passed. Request it if the argument is not provided.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        inform(f"Scaning file: {filename}")
    else:
        inform("Please, enter file name: ", end = "")
        filename = input()

    if not os.path.isfile(filename):
        failed("No such file was found in this directory. You may need to specify the full path.")
        sys.exit(1)

    inform("Enter bach size in bites (1, 2, 4 or 8): ", end="")
    try:
        num_bytes = int(input())
        format_char = get_format_char(num_bytes)
    except:
        failed("It must be a number (1, 2, 4 or 8)!")
        sys.exit(1)
    
    values = read_bytes_from_file(filename, format_char, num_bytes)
    success("Readed succesfuly!")
    
    inform ("Sorting...")
    values = dict(sorted(values.items(), key=lambda item: item[1])) # sorted from smallest to largest
    success("Sorted succesfully!")
    
    inform ("Creating text file...")
    save_frequencies_to_file(values, (result+filename+"_text_report"+".txt"))
    success(f"Creating succesfully as: {result+filename}_text_report.txt!")

    inform("Use castom graph size? (Yes/No): ", end = "")
    castom_size = input().lower()
    if (castom_size == "yes" or castom_size == 'y'):
        s = get_numbers_tuple()
        inform ("Creating graph file...")
        plot_frequencies(values, filename = (result+filename+f"_report_{s}_graph"+".png"), size = s)
        success("Creating and sawing succesfully!")

    else:
        # Print the value of the linked list
        inform ("Creating graph file...")
        plot_frequencies(values, filename = (result+filename+"_report_graph"+".png"))
        plot_frequencies(values, filename = (result+filename+"_Detalied_report_graph"+".png"), size = (40, 35))
        success("Creating and sawing succesfully!")

if __name__ == "__main__":
    hello()
    main ()
