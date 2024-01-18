import csv

def cardinality_items(filename):
    # Initialize an empty set to store unique items
    unique_items = set()

    # Read the CSV file
    with open(filename, 'r') as file:
        # Iterate through each row in the CSV file
        reader = csv.reader(file)
        for row in reader:
            # Skip empty rows
            if not row:
                continue

            # Extract items from the row and add them to the set

            unique_items.update(item.strip() for item in row)

    # Return the cardinality of the set of unique items
    return len(unique_items)


def all_itemsets(unique_items, N):
    # Ensure N is a valid value
    if N <= 0 or N > len(unique_items):
        raise ValueError("Invalid value for N")

    # Helper function to generate combinations
    def generate_combinations(start, current_itemset):
        if len(current_itemset) == N:
            all_itemsets.append(current_itemset.copy())
            return

        for i in range(start, len(unique_items)):
            current_itemset.append(unique_items[i])
            generate_combinations(i + 1, current_itemset)
            current_itemset.pop()

    all_itemsets = []
    generate_combinations(0, [])

    return all_itemsets

# Example usage:
unique_items = ["ham", "cheese", "bread"]
N = 1
result = all_itemsets(unique_items, N)
print(result)



# Example usage:
filename = "basket_data.csv"  # Replace with the actual filename
result = cardinality_items(filename)
print("Cardinality of grocery items:", result)

