import pandas as pd
import matplotlib.pyplot as plt

def generate_average_repair_time_chart(excel_file='cmms.xlsx', output_file='average_repair_time_by_asset_type.png'):
    """
    Generates a bar chart showing the average repair time by asset type.

    Args:
        excel_file (str): Path to the input Excel file.
        output_file (str): Path to save the generated chart image.
    """
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"Error: The file '{excel_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return

    # Calculate the average MeanTimeTillRepair for each AssetType
    average_repair_time = df.groupby('AssetType')['MeanTimeTillRepair'].mean().sort_values(ascending=False)

    # Create the bar chart
    plt.figure(figsize=(12, 7))
    average_repair_time.plot(kind='bar', color='skyblue')
    plt.title('Average Repair Time by Asset Type')
    plt.xlabel('Asset Type')
    plt.ylabel('Average Repair Time (Hours)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Adjust layout to prevent labels from being cut off

    # Save the chart
    try:
        plt.savefig(output_file)
        print(f"Chart saved successfully to '{output_file}'")
    except Exception as e:
        print(f"An error occurred while saving the chart: {e}")
    finally:
        plt.close() # Close the plot to free up memory

def generate_problem_description_frequency_chart(excel_file='cmms.xlsx', output_file='problem_description_frequency.png'):
    """
    Generates a bar chart showing the frequency of common issues (ProblemDescription).

    Args:
        excel_file (str): Path to the input Excel file.
        output_file (str): Path to save the generated chart image.
    """
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"Error: The file '{excel_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return

    # Count the occurrences of each unique ProblemDescription
    problem_frequency = df['ProblemDescription'].value_counts().sort_values(ascending=False)

    # Create the bar chart
    plt.figure(figsize=(12, 7))
    problem_frequency.plot(kind='bar', color='lightcoral')
    plt.title('Common Issues/Problem Description Frequency')
    plt.xlabel('Problem Description')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Adjust layout to prevent labels from being cut off

    # Save the chart
    try:
        plt.savefig(output_file)
        print(f"Chart saved successfully to '{output_file}'")
    except Exception as e:
        print(f"An error occurred while saving the chart: {e}")
    finally:
        plt.close() # Close the plot to free up memory

def generate_cost_of_parts_by_asset_type_chart(excel_file='cmms.xlsx', output_file='cost_of_parts_by_asset_type.png'):
    """
    Generates a bar chart showing the cost of parts by asset type.

    Args:
        excel_file (str): Path to the input Excel file.
        output_file (str): Path to save the generated chart image.
    """
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"Error: The file '{excel_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return

    # Calculate the sum of CostOfParts for each AssetType
    cost_of_parts = df.groupby('AssetType')['CostOfParts'].sum().sort_values(ascending=False)

    # Create the bar chart
    plt.figure(figsize=(12, 7))
    cost_of_parts.plot(kind='bar', color='lightgreen')
    plt.title('Cost of Parts by Asset Type')
    plt.xlabel('Asset Type')
    plt.ylabel('Total Cost of Parts')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Adjust layout to prevent labels from being cut off

    # Save the chart
    try:
        plt.savefig(output_file)
        print(f"Chart saved successfully to '{output_file}'")
    except Exception as e:
        print(f"An error occurred while saving the chart: {e}")
    finally:
        plt.close() # Close the plot to free up memory
