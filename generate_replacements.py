import os
import pandas as pd
import plistlib
import csv

# --- Configuration ---
# Path to the wordlist file from Chechen Corpora.
# This file is expected to be in the root of the repository.
WORDLIST_PATH = "/Users/gushmazuko/Code/Personal/Repos/ce-transliteration-tools/exports/palochka_words.tsv"

# The name of the generated CSV file.
CSV_OUTPUT_PATH = "./chechen_replacements.csv"

# Optional: A file for custom, manually-defined replacements.
# These will override any generated replacements with the same shortcut.
# Format: A CSV with 'Shortcut' and 'Phrase' columns.
OVERRIDE_CSV_PATH = "./override.csv"

# The directory where the final .plist file will be saved.
RELEASE_DIR = "./release"

# The final .plist file to be imported into iOS/macOS.
PLIST_OUTPUT_PATH = os.path.join(RELEASE_DIR, "replacements.plist")

# Number of word replacements to generate from the wordlist, sorted by frequency.
NUM_REPLACEMENTS = 200


def create_release_directory():
    """Create the release directory if it doesn't exist."""
    if not os.path.exists(RELEASE_DIR):
        print(f"Creating release directory at: {RELEASE_DIR}")
        os.makedirs(RELEASE_DIR)


def generate_csv_from_wordlist():
    """Generate a CSV file of word replacements from the source wordlist."""
    if not os.path.exists(WORDLIST_PATH):
        print(f"Warning: Wordlist file not found at {WORDLIST_PATH}. Skipping CSV generation.")
        # Create an empty CSV so the rest of the script doesn't fail
        with open(CSV_OUTPUT_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Shortcut', 'Phrase'])
        return

    print(f"Reading wordlist from: {WORDLIST_PATH}")
    # Read the TSV file into a pandas DataFrame.
    df = pd.read_csv(WORDLIST_PATH, sep="\t", header=0, names=["word", "count"])

    # Sort words by frequency in descending order.
    df.sort_values(by="count", ascending=False, inplace=True)

    # Filter for words containing the Chechen letter 'ӏ'.
    filtered_words = df[df["word"].str.contains("ӏ")].drop_duplicates(subset="word")

    # Create the 'Shortcut' by replacing 'ӏ' with '1'.
    filtered_words["Shortcut"] = filtered_words["word"].str.replace("ӏ", "1", regex=False)
    
    # Rename the 'word' column to 'Phrase' for clarity.
    filtered_words = filtered_words[["Shortcut", "word"]].rename(columns={"word": "Phrase"})

    # Limit the number of replacements.
    limited_words = filtered_words.head(NUM_REPLACEMENTS)

    # Save the replacements to a CSV file.
    limited_words.to_csv(CSV_OUTPUT_PATH, index=False)
    print(f"Successfully generated {CSV_OUTPUT_PATH} with {len(limited_words)} replacements.")


def generate_plist():
    """Generate a .plist file by combining generated and override replacements."""
    
    final_replacements = {}

    # 1. Read custom replacements from override.csv, if it exists.
    # These take priority.
    if os.path.exists(OVERRIDE_CSV_PATH):
        print(f"Reading custom replacements from: {OVERRIDE_CSV_PATH}")
        with open(OVERRIDE_CSV_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Shortcut' in row and 'Phrase' in row and row['Shortcut'] and row['Phrase']:
                    final_replacements[row['Shortcut']] = row['Phrase']
        print(f"Loaded {len(final_replacements)} custom replacements.")
    
    # 2. Read the main generated replacements file.
    if not os.path.exists(CSV_OUTPUT_PATH):
        print(f"Error: Generated CSV file not found at {CSV_OUTPUT_PATH}. Cannot generate plist.")
        return

    print(f"Reading generated replacements from: {CSV_OUTPUT_PATH}")
    with open(CSV_OUTPUT_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        generated_count = 0
        for row in reader:
            # Add only if the shortcut doesn't already exist from the override file.
            if 'Shortcut' in row and 'Phrase' in row and row['Shortcut'] not in final_replacements:
                final_replacements[row['Shortcut']] = row['Phrase']
                generated_count += 1
    
    print(f"Added {generated_count} generated replacements.")

    # 3. Convert the combined dictionary to the list format required by plistlib.
    plist_data = []
    # Sort by shortcut for a consistent output file
    for shortcut in sorted(final_replacements.keys()):
        plist_data.append({
            'phrase': final_replacements[shortcut],
            'shortcut': shortcut
        })

    # 4. Write the final .plist file.
    with open(PLIST_OUTPUT_PATH, 'wb') as plistfile:
        plistlib.dump(plist_data, plistfile)

    print(f"Successfully generated {PLIST_OUTPUT_PATH} with {len(plist_data)} total replacements.")


def main():
    """Main function to run the script."""
    create_release_directory()
    generate_csv_from_wordlist()
    generate_plist()


if __name__ == "__main__":
    main()
