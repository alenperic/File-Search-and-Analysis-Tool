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

def is_archive_or_encrypted(file_path):
    archive_extensions = ['.zip', '.rar', '.tar', '.7z', '.gz']
    encrypted_extensions = ['.aes', '.gpg', '.enc']
    if any(file_path.endswith(ext) for ext in archive_extensions):
        return 'Archive'
    elif any(file_path.endswith(ext) for ext in encrypted_extensions):
        return 'Encrypted'
    else:
        return None

def search_files(directory, terms, output_file, special_files_output, encodings, exclude_file):
    found = set()
    term_bytes = [bytes(term, 'utf-8') for term in terms]
    special_files = []

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Term', 'File', 'Encoding', 'Found In'])

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                if file_path == exclude_file:
                    continue

                file_type = is_archive_or_encrypted(file_path)
                if file_type:
                    special_files.append([file_type, file_path])

                # Check filename for terms
                for term in terms:
                    if term in file and (term, file_path, 'filename') not in found:
                        csvwriter.writerow([term, file_path, 'N/A', 'Filename'])
                        found.add((term, file_path, 'filename'))

                # Check file content for terms
                is_text_file = any(file_path.endswith(ext) for ext in ['.txt', '.py', '.java', '.html', '.csv', '.json'])
                if is_text_file:
                    for encoding in encodings:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                                for term in terms:
                                    if term in content and (term, file_path, encoding) not in found:
                                        csvwriter.writerow([term, file_path, encoding, 'Content'])
                                        found.add((term, file_path, encoding))
                                break
                        except UnicodeDecodeError:
                            continue
                else:
                    # Handle as binary file
                    term_found, mode = search_binary_file(file_path, terms, term_bytes)
                    if term_found and (term_found, file_path, mode) not in found:
                        csvwriter.writerow([term_found, file_path, mode, 'Binary Content'])
                        found.add((term_found, file_path, mode))

    # Write special files to a separate CSV
    with open(special_files_output, 'w', newline='', encoding='utf-8') as special_csv:
        csvwriter = csv.writer(special_csv)
        csvwriter.writerow(['Type', 'File Location'])
        for file in special_files:
            csvwriter.writerow(file)

def main():
    terms_file_path = "search.txt"
    directory_to_search = os.getcwd()
    output_file_path = "search_results.csv"
    special_files_output = "special_files.csv"
    encodings = ['utf-8', 'iso-8859-1', 'cp1252', 'utf-16']

    terms_to_search = read_search_terms(terms_file_path)

    search_files(directory_to_search, terms_to_search, output_file_path, special_files_output, encodings, os.path.join(directory_to_search, terms_file_path))
    print(f"Search complete. Results saved in {output_file_path}")
    print(f"Special files (archives and encrypted) saved in {special_files_output}")

if __name__ == "__main__":
    main()
