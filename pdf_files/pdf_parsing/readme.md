# PDF Parsing
This section is parsing the PDF file to extract useful information concerning the dataset 

## Paper Processing

This file parse the pdf paper, break it down by paragraph and save those that include one of the keywords in a json file.

**Python call**:
```python
python paper_processing.py -p {path to access the directory} -i {input dir} -o {output dir} -t {number of threads}
```

**Example**:
```python
python paper_processing.py -p '' -i 'PDFs/' -o 'samples_with_keywords' -t 8
```
## Prodigy Processing

This file serialize the information into one jsonl file that could be used for annotation with the Prodigy library.

**Python call**:
```python
python prodigy_processing.py -p {path to access the directory that contains the docs created by the script above} -t {number of threads} -n {name we want to give to the generated file}
```

**Example**:
```python
python prodigy_preprocessing.py -p 'samples_with_keywords/'
```
