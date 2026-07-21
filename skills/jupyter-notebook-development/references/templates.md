# Notebook Templates

The templates below are flexible guides, not rigid requirements. Cells 1-3 (Title/Introduction, Library Imports, Configuration) are mandatory in every notebook. Beyond that, add, remove, or reorder cells based on the actual workflow.

## Generic

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Title and Introduction |
| 2 | Code | Library Imports |
| 3 | Code | Configuration |
| ... | ... | ... |
| ... | Markdown | Conclusion |

## Machine Learning / Deep Learning

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Title, Introduction, Research Objective |
| 2 | Code | Library Imports |
| 3 | Code | Configuration (Seed, Batch Size, Epochs, Dataset Path) |
| 4 | Markdown | Dataset Description |
| 5 | Code | Load Dataset |
| 6 | Code | Quick Dataset Exploration |
| 7-10 | Code | Cleaning, Preprocessing, Augmentation, Feature Engineering |
| 11 | Markdown | Model Architecture |
| 12 | Code | Model Definition |
| 13 | Code | Compile Model |
| 14 | Code | Training |
| 15 | Code | Training History Visualization |
| 16 | Code | Model Evaluation |
| 17 | Code | Confusion Matrix / Classification Report |
| 18 | Code | Save Model |
| 19 | Code | Inference |
| 20 | Markdown | Conclusion |

## Web Crawling / Web Scraping

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Introduction |
| 2 | Code | Library Imports |
| 3 | Code | Configuration (`MAX_AGE_DAYS`, `DELAY_RANGE`, `HEADERS`, paths) |
| 4 | Markdown | Target Website |
| 5 | Code | Session or Request Setup |
| 6 | Code | Crawling / Download Loop |
| 7 | Code | Data Parsing |
| 8 | Code | Data Validation |
| 9 | Code | Export CSV / JSON / Database |
| 10 | Markdown | Summary |

## Exploratory Data Analysis (EDA)

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Introduction |
| 2 | Code | Library Imports |
| 3 | Code | Configuration |
| 4 | Code | Load Dataset |
| 5 | Code | Dataset Information |
| 6 | Code | Missing Values |
| 7 | Code | Descriptive Statistics |
| 8 | Code | Data Distribution |
| 9 | Code | Correlation |
| 10 | Code | Outliers |
| 11 | Code | Visualization |
| 12 | Markdown | Insights |

## Data Cleaning / Preprocessing

| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | Introduction |
| 2 | Code | Library Imports |
| 3 | Code | Configuration |
| 4 | Code | Load Dataset |
| 5 | Code | Missing Values |
| 6 | Code | Duplicate Handling |
| 7 | Code | Encoding |
| 8 | Code | Normalization or Scaling |
| 9 | Code | Feature Selection |
| 10 | Code | Export Dataset |
| 11 | Markdown | Summary |
