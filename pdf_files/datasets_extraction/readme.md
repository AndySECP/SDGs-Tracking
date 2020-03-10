# Datasets extraction
Here, we are building a dataset extractor. The goal is to parse as many papers as possible. Identify where they are mention of datasets. Then, classify them as relevant for one or many of the SDGs. 

## Resources

The papers used here are extracted from aminer.

## Version 1

- From the 20GB txt file downloaded on the aminer page, we extract the title of papers
- A Google search of this paper is cresated (filtered on pdf with filetype:pdf)
- The top 5 results are kept
- The first actual pdf returned is downloaded
- Leveraging PyPDF4, a parser look at each page of this pdf and extract the ones with mention of 'data' or 'dataset[s]'
- Those pages are saved as json in a separate folder 
- The pdf is deleted

### Labeling part of the pages extracted

To build a binary classifier (whether or not the page contains relevant dataset mention), we first hand label a subset of those pages.

### Binary classifier

Then, we build a binary classifier on top of those labeled examples to extrapolate those labels to the rest of the dataset
- TF-IDF + Random Forest Classifier
- Word Embedding + Random Forest Classifier
- Adding Text / NLP based features

### Active Learning

Active Learning is leveraged to enlarge the set of labeled data and enable the model to reach better accuracy.
