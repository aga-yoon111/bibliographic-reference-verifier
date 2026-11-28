## Bibliografic Reference Verifier 
(we will add them as the modules are completed)

# Bibtex Processing Module
Responsible for reading, processing and writing
BibTeX bibliographic references.

### Features

- Reads .bib files.
- Extracts bibliographic entries.
- Converts entries into Python dictionaries.
- Preserves original bibliographic information.
- Applies approved metadata updates.
- Generates a new enriched BibTeX file.

### Main Functions

#### load_bibtex_file(file_path)

Input:
- Path to a .bib file.

Output:
- Parsed BibTeX library.
- List of organized bibliographic records.

#### write_enriched_bibtex(
    library,
    approved_updates,
    output_path,
    input_path
)

Input:
- Original parsed library.
- Approved metadata updates.
- Output file path.
- Original input file path.

Output:
- A new enriched BibTeX file.
