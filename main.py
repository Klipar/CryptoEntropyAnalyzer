import struct
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
from Easy.animations import *
from Easy.massage import *
from src.message import hello
import os

class Node:
    """Клас для вузла зв'язаного списку."""
    def __init__(self, value, count):
        self.value = value
        self.count = count
        self.next = None

class LinkedList:
    """Клас для зв'язаного списку."""
    def __init__(self):
        self.head = None

    def append(self, value, count):
        """Додає новий вузол до списку."""
        new_node = Node(value, count)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def get_frequencies(self):
        """Повертає словник частот значень."""
        frequencies = {}
        current = self.head
        while current:
            frequencies[current.value] = current.count
            current = current.next
        return frequencies

    def sort(self):
        """Сортує зв'язаний список за спаданням значення count."""
        # Використовуємо алгоритм сортування злиттям для сортування списку
        if not self.head or not self.head.next:
            return

        def merge_sort(node):
            if not node or not node.next:
                return node
            
            # Знайдемо середину списку
            slow, fast = node, node.next
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            
            # Розділяємо список на дві половини
            mid = slow.next
            slow.next = None

            # Рекурсивно сортуємо кожну половину
            left = merge_sort(node)
            right = merge_sort(mid)

            # Об'єднуємо відсортовані половини
            return merge(left, right)

        def merge(left, right):
            dummy = Node(0, 0)
            current = dummy
            while left and right:
                if left.count > right.count:
                    current.next = left
                    left = left.next
                else:
                    current.next = right
                    right = right.next
                current = current.next

            current.next = left if left else right
            return dummy.next

        # Оновлюємо голову списку
        self.head = merge_sort(self.head)

def Read_bytes_bucket (file, bytes_per_value, value_count, format_char):
    try: # the function misses all checks to increase the reading speed
        bytes_data = file.read(bytes_per_value)
        if bytes_data:
            value = struct.unpack(format_char, bytes_data)[0]
            value_count[value] += 1
            return bytes_data, value
        return bytes_data, 0
    except Exception as e:
        failed (f"Error while reading file: \n{e}")

def get_format_char(num_bytes: int) -> str:
    """Determine the format character based on the number of bytes."""
    format_mapping = {
        1: 'B',  # 8-bit unsigned integer
        2: 'H',  # 16-bit unsigned integer
        4: 'I',  # 32-bit unsigned integer
        8: 'Q'   # 64-bit unsigned integer
    }
    
    if num_bytes in format_mapping:
        return format_mapping[num_bytes]
    else:
        raise ValueError(f"Unsupported number of bytes: {num_bytes}. Only 1, 2, 4, or 8 bytes are supported.")

def read_bytes_from_file(filename: str, format_char: str, num_bytes: int) -> dict:
    """_summary_

    Args:
        filename (str): name of the file to be scanned
        format_char (str): format char (use func get_format_char() to it)
        num_bytes (int): Number of bytes to be scanned must be in (1, 2, 4, 8)

    Raises:
        ValueError: The number of bytes must be at least 1!
        ValueError: Only 1, 2, 4, or 8 bytes are supported.

    Returns:
        dict: _description_
    """
    bytes_per_value = struct.calcsize(format_char)
    value_count = defaultdict(int) # a dictionary for counting meetings
    try:
        with open(filename, 'rb') as file:
            inform ("Show bar (it make proces slower)? (Yes/No): ", end = "")
            show_bat = input().lower()
            if (show_bat == "yes" or show_bat == 'y'):
                val = (int(os.path.getsize(filename))/num_bytes)
                bar = LineProgresBar (MaxLength = 50, text = "Scaning", maxWalue = val, isShowPersent = True,  isShowWalue = True)

                while True: # I used 2 cycles to speed up the processing of large files
                    bytes_data, value = Read_bytes_bucket (file, bytes_per_value, value_count, format_char)
                    bar.ShoveAndUpdate (isreturn = False)
                    print(f'  [{value:0{bytes_per_value * 8}b}]', end="\r") 
                    
                    if len(bytes_data) < bytes_per_value:
                        print()
                        break
            else:
                while True:
                    bytes_data, value = Read_bytes_bucket (file, bytes_per_value, value_count, format_char)

                    if len(bytes_data) < bytes_per_value:
                        break
            return value_count
    except:
        failed (f"could not open the file: {filename}")
        sys.exit (1)

def plot_frequencies(frequencies: dict, filename: str = 'frequency_plot.png', size = (12, 8)):    
    # Sort values by frequency (from highest to lowest)
    sorted_items = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    values, counts = zip(*sorted_items)

    # Create a plot
    plt.figure(figsize=size)  # Increased figure sizes
    plt.bar(range(len(values)), counts, tick_label=values, color='skyblue')
    plt.xlabel('Numbers')
    plt.ylabel('Frequencies')
    plt.title('File Entropy')
    
    # Place the labels on the X-axis so that the frequencies are displayed from highest to lowest
    plt.xticks(rotation=90, ha='right')  # Rotate the labels on the X-axis for better readability and align them to the right edge
    plt.grid(axis='y')

    # Save the graph to a file
    plt.tight_layout()  # Automatic dimensional adjustment to avoid overlap
    plt.savefig(filename, format='png')
    plt.close()  # Close the chart to free up memory

    success(f"Saves to: {filename}")

def save_frequencies_to_file(frequencies: dict, filename: str) -> None:
    """Saves the frequencies of values to a file detailing the least frequent and most frequent values."""

    # Find the minimum and maximum number of meetings
    min_value, min_count = next(iter(frequencies.items()))
    max_value, max_count = next(reversed(frequencies.items()))

    # Calculating the arithmetic mean
    total_count = sum(frequencies.values())
    average_count = total_count / len(frequencies) if frequencies else 0

    with open(filename, 'w') as f:
        # Record the rarest and most frequent values
        f.write(f"Least and Most frequent Values:\nValues: {min_value}, qty: {min_count}\n")
        f.write(f"Values: {max_value}, qty: {max_count}\n\n")
        
        # The difference between the minimum and maximum value, in the context of the number of repetitions
        difference = max_count - min_count
        
        f.write(f"Distance delta between the frequency \nof occurrence of the rarest and most frequent values: \n===> {difference}\n")
        f.write(f"Distance delta between the frequency \nof occurrence of the rarest and most frequent values \nas a \npercentage of the largest: \n===> {(100/max_count)*difference} %\n")
        f.write(f"Distance delta between the frequency \nof occurrence of the rarest and most frequent values \nas a percentage of the mean: \n===> {round((100/average_count)*difference, 4)} %\n")
        
        f.write(f"\n{'Values':<15}{'Frequency':<15}\n")
        f.write("-" * 30 + "\n")
        for value, count in frequencies.items():
            f.write(f"{str(value):<15}{str(count):<15}\n")


def get_numbers_tuple():
    while 1:
        inform ("Enter your size (x, y):", end = "")
        input_string = input("")
        try:
            numbers = tuple(map(int, input_string.split(',')))
            if numbers[0] < 0 or numbers[1] < 0:
                raise ("Value erro. Some of the entered data is less than 0!")
            return numbers
        except:
            failed ("Data entered incorrectly!\nThese must be 2 numbers greater than 0.")



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
        # Виводимо значення зв'язаного списку
        inform ("Creating graph file...")
        plot_frequencies(values, filename = (result+filename+"_report_graph"+".png"))
        plot_frequencies(values, filename = (result+filename+"_Detalied_report_graph"+".png"), size = (40, 35))
        success("Creating and sawing succesfully!")

if __name__ == "__main__":
    hello()
    main ()
