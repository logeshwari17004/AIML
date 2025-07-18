import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def detect_duplicates(id_array, start_date="2025-07-01", visualize=False, show_summary=True):
    num_entries = len(id_array)
    dates = pd.date_range(start=start_date, periods=num_entries, freq="D")

    # Find first occurrence indices
    _, first_indices = np.unique(id_array, return_index=True)
    is_duplicate = np.ones_like(id_array, dtype=bool)
    is_duplicate[first_indices] = False  # Mark first occurrences as False

    # DataFrame for display and optional visualization
    df = pd.DataFrame({
        "Date": dates,
        "ID": id_array,
        "Is_Duplicate": is_duplicate
    })

    if show_summary:
        total_duplicates = np.sum(is_duplicate)
        unique_ids = len(np.unique(id_array))
        print(f"Total Entries: {num_entries}")
        print(f"Unique IDs   : {unique_ids}")
        print(f"Duplicates   : {total_duplicates}")

    if visualize:
        duplicate_counts = df[df["Is_Duplicate"]].groupby("ID").size().sort_values(ascending=False)
        if not duplicate_counts.empty:
            plt.figure(figsize=(10, 5))
            duplicate_counts.plot(kind="bar", color="skyblue", edgecolor="black")
            plt.title("Duplicate Entries Per ID")
            plt.xlabel("ID")
            plt.ylabel("Number of Duplicates")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
        else:
            print("No duplicates found to visualize.")


# Function to check duplicates in test cases
def find_duplicates(arr):
    seen = set()
    result = []
    for id in arr:
        if id in seen:
            result.append(True)
        else:
            seen.add(id)
            result.append(False)
    return np.array(result)


# Main execution
if __name__ == "__main__":
    T = int(input("Enter number of test cases: "))
    for _ in range(T):
        arr = np.array(list(map(int, input("Enter IDs space-separated: ").split())))
        output = find_duplicates(arr)
        print("Output:", output)

        # Optional: call detect_duplicates with extra analysis
        detect_duplicates(arr, visualize=True, show_summary=True)