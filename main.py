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
        num_bytes (str): Number of bytes to be scanned must be in (1, 2, 4, 8)

    Raises:
        ValueError: The number of bytes must be at least 1!
        ValueError: Only 1, 2, 4, or 8 bytes are supported.

    Returns:
        dict: _description_
    """
    if num_bytes < 1:
        raise ValueError("The number of bytes must be at least 1!")
    
    # Determine the format based on the number of bytes
    if num_bytes == 1:
        format_char = 'B'  # 8-bit unsigned integer
    elif num_bytes == 2:
        format_char = 'H'  # 16-bit unsigned integer
    elif num_bytes == 4:
        format_char = 'I'  # 32-bit unsigned integer
    elif num_bytes == 8:
        format_char = 'Q'  # 64-bit unsigned integer
    else:
        raise ValueError("Only 1, 2, 4, or 8 bytes are supported.")

    bytes_per_value = struct.calcsize(format_char)
    value_count = defaultdict(int) # a dictionary for counting meetings
    try:
        with open(filename, 'rb') as file:
            inform ("Show bar, it make proces slover? (Yes/No): ", end = "")
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

def plot_frequencies(linked_list, filename='frequency_plot.png', size = (12, 8)):
    frequencies = linked_list.get_frequencies()
    
    # Сортуємо значення за частотою (від найбільшої до найменшої)
    sorted_items = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    values, counts = zip(*sorted_items)

    # Створюємо графік
    plt.figure(figsize=size)  # Збільшені розміри фігури
    plt.bar(range(len(values)), counts, tick_label=values, color='skyblue')
    plt.xlabel('Numbers')
    plt.ylabel('Frequencys')
    plt.title('File Entropy')
    
    # Розміщуємо мітки на осі X так, щоб частоти відображались від найбільшої до найменшої
    plt.xticks(rotation=90, ha='right')  # Повертаємо мітки на осі X для кращої читабельності і вирівнюємо по правому краю
    plt.grid(axis='y')

    # Зберігаємо графік у файл
    plt.tight_layout()  # Автоматичне підлаштування розмірів, щоб уникнути накладання
    plt.savefig(filename, format='png')
    plt.close()  # Закриваємо графік, щоб звільнити пам'ять

    success(f"Saves to: {filename}")
def save_frequencies_to_file(linked_list, filename='frequencies_sorted.txt'):
    """Зберігає частоти значень у файл з деталізацією найрідше і найчастіше зустрічаних значень."""
    frequencies = linked_list.get_frequencies()
    
    # Знаходимо мінімальну і максимальну кількість зустрічань
    min_count = min(frequencies.values())
    max_count = max(frequencies.values())
    
    min_values = [value for value, count in frequencies.items() if count == min_count]
    max_values = [value for value, count in frequencies.items() if count == max_count]
    
    # Обчислення середнього арифметичного
    total_count = sum(frequencies.values())
    average_count = total_count / len(frequencies) if frequencies else 0

    with open(filename, 'w') as f:
        # Записуємо найрідше зустрічані значення
        f.write("Least Common Values:\n")
        for value in min_values:
            f.write(f"Values: {value}, qty: {min_count}\n")
        
        # Записуємо найчастіше зустрічані значення
        f.write("\nMost Common Values:\n")
        for value in max_values:
            f.write(f"Values: {value}, qty: {max_count}\n")
        
        # Різниця між мінімальним і максимальним значенням
        difference = max_count - min_count
        f.write(f"\nDifference Between Least Common and Most Frequently Encountered Values: \n===> {difference}\n")
        
        f.write(f"\nThe difference between the least and most frequently encountered values as a percentage of the largest: \n===> {(100/max_count)*difference} %\n")

        f.write(f"\nThe difference between the least and most frequently encountered values as a percentage of the mean: \n===> {(100/average_count)*difference} %\n")
        
        # f.write(f"Maximum number of appointments: {}")
        f.write(f"\n{'Values':<15}{'Frequency':<15}\n")
        f.write("-" * 30 + "\n")
        for value, count in frequencies.items():
            f.write(f"{str(value):<15}{str(count):<15}\n")


def get_numbers_tuple():
    input_string = input("")

    numbers = tuple(map(int, input_string.split(',')))

    return numbers



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
        if (num_bytes not in [1, 2, 4, 8]):
            raise("input error!")
    except:
        failed("It must be a number (1, 2, 4 or 8)!")
        sys.exit(1)

    linked_list = read_bytes_from_file(filename, num_bytes)

    success("Readed succesfuly!")
    # Сортуємо список
    inform ("Sorting...")
    linked_list.sort()
    success("Sorted succesfully!")
    # Виводимо відсортовані значення
    # print(linked_list.get_frequencies())
    inform ("Creating text file...")
    save_frequencies_to_file(linked_list, (result+filename+"_text_report"+".txt"))
    success(f"Creating succesfully as: {result+filename}_text_report.txt!")


    inform("Use castom graph size? (Yes/No): ", end = "")
    castom_size = input().lower()
    if (castom_size == "yes" or castom_size == 'y'):
        # Виводимо значення зв'язаного списку
        inform ("Enter your size (x, y):", end = "")
        s = get_numbers_tuple()
        inform ("Creating graph file...")
        plot_frequencies(linked_list, filename = (result+filename+f"_report_{s}_graph"+".png"), size = s)
        success("Creating and sawing succesfully!")

    else:
        # Виводимо значення зв'язаного списку
        inform ("Creating graph file...")
        plot_frequencies(linked_list, filename = (result+filename+"_report_graph"+".png"))
        plot_frequencies(linked_list, filename = (result+filename+"_Detalied_report_graph"+".png"), size = (40, 35))
        success("Creating and sawing succesfully!")

if __name__ == "__main__":
    hello()
    main ()
