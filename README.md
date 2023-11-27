# File Search and Analysis Tool

This Python script searches for specified terms within all files and filenames in the current directory and its subdirectories. It also identifies archives and encrypted files based on their extensions. The results are outputted in two CSV files: one for the term search results and another for the special file types (archives and encrypted).

## Features
- Searches for specified terms in file content and filenames.
- Identifies and lists archives and potentially encrypted files.
- Outputs results in two separate CSV files.
- Excludes the search terms file from the analysis.
- Handles multiple text file encodings and binary files.

## Usage
1. Place your search terms, each on a new line, in `search.txt`.
2. Run the script in the directory where you want to perform the search.
3. Check `search_results.csv` for the term search results and `special_files.csv` for archives and encrypted files.

## Requirements
This script uses standard Python libraries. No additional installations are required.

For more information on how to use or contribute to this tool, please see the sections below.

## Contributing
Contributions to enhance the functionality of this script are welcome. Please feel free to fork this repository and submit pull requests.

## License
This project is open-source and available under the [MIT License](LICENSE).
