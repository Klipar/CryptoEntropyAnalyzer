import matplotlib.pyplot as plt
from Easy.massage import *

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
