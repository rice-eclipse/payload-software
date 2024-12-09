import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_dual_axis_csv(file1, file2):
    try:
        # Load the first CSV file
        data1 = pd.read_csv(file1)
        if data1.shape[1] < 2:
            print(f"Error: {file1} must have at least two columns.")
            return

        # Load the second CSV file
        data2 = pd.read_csv(file2)
        if data2.shape[1] < 2:
            print(f"Error: {file2} must have at least two columns.")
            return

        # Extract data for plotting
        x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
        x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]

        # Create the plot
        fig, ax1 = plt.subplots(figsize=(8, 6))

        # Plot data from the first CSV file on the primary y-axis
        ax1.plot(x1, y1, label=f"{data1.columns[1]} (from {os.path.basename(file1)})", color='blue')
        ax1.set_xlabel(data1.columns[0])
        ax1.set_ylabel(data1.columns[1], color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True)

        # Create a second y-axis for the second CSV file
        ax2 = ax1.twinx()
        ax2.plot(x2, y2, label=f"{data2.columns[1]} (from {os.path.basename(file2)})", color='green')
        ax2.set_ylabel(data2.columns[1], color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        # Add title and legend
        fig.suptitle(f"{data1.columns[0]} vs {data1.columns[1]} and {data2.columns[1]}")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        # Show the plot
        plt.tight_layout()
        plt.show()

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Error: One of the provided CSV files is empty: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # hard code the file paths, (the line below it is for user input csv files)
    file1 = r'./test-system/generatedData/GenAccelData.csv'
    # file1 = input("Enter the path to the first CSV file: ").strip()
    file2 = r'./test-system\generatedData\GenAltData.csv'
    # file2 = input("Enter the path to the second CSV file: ").strip()

    # Validate file existence
    if not os.path.isfile(file1):
        print(f"Error: File '{file1}' does not exist.")
    elif not os.path.isfile(file2):
        print(f"Error: File '{file2}' does not exist.")
    else:
        # Plot the data from the two files
        plot_dual_axis_csv(file1, file2)
