# KeyLexBundles

`keylexbundles` provides a Python function `compute_keyness` to compute **4-gram lexical bundle keyness** between a target and a reference corpus.

---

## Install and Usage

First, to install keylexbundles, use pip in terminal:

```bash
pip install keylexbundles
```

Once installed, import the package in your python code by running the following code:

```python
import keylexbundles
```

Once imported, call the function with two required arguments: `target_path` and `reference_path` and an optional arguement `output_file`:

```python
keylexbundles.compute_keyness(target_path="data/target/", reference_path="data/reference/", output_file="output.csv")
```

| argument                                      | Description                                                             |
| --------------------------------------------- | ----------------------------------------------------------------------- |
| `target_path`                            | Folder/directory with .txt files for a target corpus                         |
| `reference_path`            | Folder/directory with .txt files for a target corpus                                      |
| `output_file`                   | (Optional) Name of the CSV file to save results to. Defaults to "output.csv".         |



---

## Features
- Accepts two folders that contain .txt files for a target corpus and a reference corpus 
- Extracts 4-gram bundles (contiguous sequences of 4 tokens)

Computes:
- Whole-corpus frequency keyness: log-likelihood (G²) using raw whole-corpus token counts
- Text dispersion keyness: log-likelihood (G²) using text dispersion (i.e., the number of texts in which a bundle occurs)
- Mean text frequency keyness: Cohen's *d* (standardized difference of mean normalized per-text frequencies)

Outputs a CSV with metrics below, sorted primary by text dispersion keyness and secondary by raw whole-corpus token counts in a target corpus

---
## Output CSV Columns

| Column                                        | Description                                                             |
| --------------------------------------------- | ----------------------------------------------------------------------- |
| `lexical bundle`                              | Lexical bundle                                                          |
| `whole-corpus frequency keyness`              | Log-likelihood (G²) based on whole-corpus frequency                     |
| `text dispersion keyness`                     | Log-likelihood (G²) based on text dispersion                            |
| `mean text frequency keyness`                 | Cohen's *d*                                                             |
| `raw frequency (target)`                      | token count in target corpus                                            |
| `normed frequency (target)`                   | token frequency per 1,000 words in target corpus                        |
| `text dispersion (target)`                    | Number of texts where bundle appears in target corpus                   |
| `mean of normed frequency (target)`           | Mean per-text normalized frequency in target corpus                     |
| `sd of normed frequency (target)`             | Standard deviation of per-text normalized frequency in target corpus    |
| `raw frequency (reference)`                   | raw token count in reference corpus                                     |
| `normed frequency (reference)`                | token frequency per 1,000 words in reference corpus                     |
| `text dispersion (reference)`                 | Number of texts where bundle appears in reference corpus                |
| `mean of normed frequency (reference)`        | Mean per-text normalized frequency in reference corpus                  |
| `sd of normed frequency (reference)`          | Standard deviation of per-text normalized frequency in reference corpus |

---

## Citation
If you use **keylexbundles** in your research, please cite it as:  
Larsson, T., Kim, T., & Egbert, J. (2025). Introducing and comparing two techniques for key lexical bundles analysis. *Research Methods in Applied Linguistics, 4*(3), 100245. https://doi.org/10.1016/j.rmal.2025.100245
