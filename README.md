# Chechen Palochka (ӏ) iOS/macOS Text Replacement

This project provides a simple way to make typing Chechen words containing the Cyrillic letter “ӏ” (Palochka) easier on iOS and macOS devices, where this character is not available on the standard Russian keyboard.

## The Problem

The Chechen letter "ӏ" (U+04CF) is essential for writing in the Chechen language, but it's absent from the standard iOS/macOS Russian keyboard layout. This makes it cumbersome to type words containing this letter, requiring users to copy-paste the character or switch to a custom keyboard layout.

## The Solution

This script automates the creation of a text replacement list to solve this problem. It works by:

1.  **Processing a Wordlist**: It reads a list of real Chechen words from a `corpora_wordlist.tsv` file, sourced from the [Chechen Corpora](https://corpora.dosham.info).
2.  **Generating Shortcuts**: It creates simplified versions of words containing "ӏ" by replacing the letter with the number "1". For example, `хӏумма` becomes `х1умма`.
3.  **Exporting a `.plist` File**: It exports these shortcuts and their corresponding full phrases into a `replacements.plist` file. This file can be directly imported into the Text Replacement settings on macOS.

Once imported on a Mac, these text replacements automatically sync via iCloud to any iPhone or iPad signed in to the same Apple ID, making the shortcuts available across all your devices.

## How to Use

### Requirements

*   Python 3
*   pandas library (`pip install pandas`)

### Instructions

1.  **Get the Wordlist (Optional)**: If you want to generate replacements from the Chechen Corpora, download the `corpora_wordlist.tsv` file from their [website](http://corpora.chechenpro.ru/search/export.php?d=1&fmt=tsv) and place it in the root directory of this project.

2.  **Add Custom Replacements (Optional)**: You can add your own custom replacements by creating a file named `override.csv` in the root directory. This is useful for adding words not found in the corpora or for defining custom shortcuts.

    The file must have two columns: `Shortcut` and `Phrase`.

    **Example `override.csv`:**
    ```csv
    Shortcut,Phrase
    дог1а,догӏа
    ```
    *Note: Replacements in this file will take priority. If a shortcut exists in both the generated list and `override.csv`, the version from `override.csv` will be used.*

3.  **Run the Script**: Open your terminal, navigate to the project directory, and run the following command:
    ```sh
    python3 generate_replacements.py
    ```

4.  **Find the `.plist` File**: The script will create a `release` folder containing the `replacements.plist` file.

5.  **Import to macOS**:
    *   Open **System Settings** on your Mac.
    *   Go to **Keyboard**.
    *   Click on **Text Replacements...** under the *Text Input* section.
    *   Drag and drop the generated `replacements.plist` file directly into the text replacements window.

Your new text replacements will now be active on your Mac and will sync to your iOS devices shortly.
