import struct
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
from Easy.animations import *
from Easy.massage import *

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

def read_bytes_from_file(filename, num_bytes):
    if num_bytes < 1:
        raise ValueError("Кількість байтів повинна бути не менше 1.")
    
    # Визначаємо формат на основі кількості байтів
    if num_bytes == 1:
        format_char = 'B'  # 8-бітне беззнакове ціле
    elif num_bytes == 2:
        format_char = 'H'  # 16-бітне беззнакове ціле
    elif num_bytes == 4:
        format_char = 'I'  # 32-бітне беззнакове ціле
    elif num_bytes == 8:
        format_char = 'Q'  # 64-бітне беззнакове ціле
    else:
        raise ValueError("Підтримуються лише 1, 2, 4 або 8 байтів.")

    bytes_per_value = struct.calcsize(format_char)  # Кількість байтів, необхідна для формату
    value_count = defaultdict(int)  # Словник для підрахунку зустрічей значень

    with open(filename, 'rb') as file:
        inform ("Show bar, it make proces slover? (Yes/No): ", end = "")
        show_bat = input().lower()
        if (show_bat == "yes" or show_bat == 'y'):
            val = (int(os.path.getsize(filename))/num_bytes)
            bar = LineProgresBar (MaxLength = 50, text = "Scaning", maxWalue = val, isShowPersent = True,  isShowWalue = True)
        while True:
            if (show_bat == "yes" or show_bat == 'y'):
                bar.ShoveAndUpdate (isreturn = False)
            # Читаємо задану кількість байтів
            bytes_data = file.read(bytes_per_value)
            if len(bytes_data) < bytes_per_value:
                # Якщо прочитано менше, ніж потрібно, виходимо з циклу
                if (show_bat == "yes" or show_bat == 'y'):
                    print(f'  [{value:0{bytes_per_value * 8}b}]', end="\r") 
                break
            
            # Перетворюємо байти у значення
            if num_bytes in [1, 2, 4, 8]:
                value = struct.unpack(format_char, bytes_data)[0]
                value_count[value] += 1
                if (show_bat == "yes" or show_bat == 'y'):
                    print(f'  [{value:0{bytes_per_value * 8}b}]', end="\r") 
            
    
    # Створюємо зв'язаний список
    linked_list = LinkedList()
    for value, count in value_count.items():
        linked_list.append(value, count)
    if (show_bat == "yes" or show_bat == 'y'):
        print()
    return linked_list

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


def hello ():
    print(colors.BEIGE + '''
 _____      _                           _____                                 
|  ___|    | |                         /  ___|                                
| |__ _ __ | |_ _ __ ___  _ __  _   _  \ `--.  ___ __ _ _ __  _ __   ___ _ __ 
|  __| '_ \| __| '__/ _ \| '_ \| | | |  `--. \/ __/ _` | '_ \| '_ \ / _ \ '__|
| |__| | | | |_| | | (_) | |_) | |_| | /\__/ / (_| (_| | | | | | | |  __/ |   
\____/_| |_|\__|_|  \___/| .__/ \__, | \____/ \___\__,_|_| |_|_| |_|\___|_|   
                         | |     __/ |                                        
                         |_|    |___/                                         
    
'''+ colors.END)



hello()

result = "Result/"
if not os.path.exists(result):
    # Якщо папка не існує, створюємо її
    os.makedirs(result)

# Перевіряємо, чи був переданий аргумент
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inform(f"Scaning file: {filename}")
else:
    inform("Please, enter file name: ", end = "")
    filename = input()
# Виклик функції з файлом і кількістю байтів
# filename = '1'  # Задайте назву вашого файлу
inform("Enter bach size in bites (1, 2, 4 or 8): ", end="")
num_bytes = int(input())
# num_bytes = 1
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


