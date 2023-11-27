import os
import csv

def read_search_terms(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def search_binary_file(file_path, terms, term_bytes):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            for term, byte_seq in zip(terms, term_bytes):
                if byte_seq in content:
                    return term, 'binary'
        return None, None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

def search_files(directory, terms, content_output_file, name_output_file, encodings):
    content_found = set()
    name_found = set()
    term_bytes = [bytes(term, 'utf-8') for term in terms]

    with open(content_output_file, 'w', newline='', encoding='utf-8') as content_csvfile, \
         open(name_output_file, 'w', newline='', encoding='utf-8') as name_csvfile:
        
        content_csvwriter = csv.writer(content_csvfile)
        content_csvwriter.writerow(['Term', 'File', 'Encoding'])

        name_csvwriter = csv.writer(name_csvfile)
        name_csvwriter.writerow(['Term', 'File', 'Encoding'])

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                # Check filename for terms
                for term in terms:
                    if term in file and (term, file_path) not in name_found:
                        name_csvwriter.writerow([term, file_path, 'filename'])
                        name_found.add((term, file_path))

                # Check file content for terms
                if any(file_path.endswith(ext) for ext in ['.txt', '.py', '.java', '.html', '.csv', '.json']):  # Add more text extensions as needed
                    for encoding in encodings:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                                for term in terms:
                                    if term in content and (term, file_path) not in content_found:
                                        content_csvwriter.writerow([term, file_path, encoding])
                                        content_found.add((term, file_path))
                                break
                        except UnicodeDecodeError:
                            continue
                else:
                    # Handle as binary file
                    term_found, mode = search_binary_file(file_path, terms, term_bytes)
                    if term_found and (term_found, file_path) not in content_found:
                        content_csvwriter.writerow([term_found, file_path, mode])
                        content_found.add((term_found, file_path))

def main():
    terms_file_path = "search.txt"
    directory_to_search = os.getcwd()
    content_output_file_path = "content_search_results.csv"
    name_output_file_path = "name_search_results.csv"
    encodings = ['utf-8', 'iso-8859-1', 'cp1252', 'utf-16']

    terms_to_search = read_search_terms(terms_file_path)

    search_files(directory_to_search, terms_to_search, content_output_file_path, name_output_file_path, encodings)
    print(f"Search complete. Content results saved in {content_output_file_path}")
    print(f"Filename results saved in {name_output_file_path}")

if __name__ == "__main__":
    main()
