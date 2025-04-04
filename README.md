# Gene-VEP-Pipeline
This repository provides a modular pipeline that takes a gene name or a list of genes as input and returns pathogenicity predictions using VEP (Variant Effect Predictor). The input variants are sourced from a cleaned dataset, available in the [ClinVar Data Cleaning repository](https://github.com/AitanaESCI/ClinVar-Data-Cleaning).


### 🧬 Purpose
This pipeline allows users to:
  - Select variants related to specific genes.
  - Format them into VCF for VEP annotation.
  - Parse and merge VEP output with original variant info.
  - Produce a final dataset with filtered predictions.


### 📁 Repository structure
```bash
├── scripts/
│   ├── generate_vcf.py             # Generates VCF for selected gene(s)
│   ├── parsing_ClinVar.py          # Parses VEP output for ClinVar
│   ├── final_merge.py              # Final merge with predictions
│   ├── merging_ClinVar.py          # Helper: merges extra annotations
│   ├── test.py                     # Command-line interface example
│   ├── pipeline.sh                 # Bash wrapper to run the full pipeline
│   └── ...
├── output/                         # Example output files
└── unique_GeneSymbols.txt          # All available gene names

```


### 🔗 Dataset requirement
This pipeline depends on a cleaned ClinVar dataset prepared in the ClinVar-Data-Cleaning repository.
To use this pipeline:
  - Clone both repositories.
  - Download the _cleaned_ClinVar_dataset.csv_ from the ClinVar repository.
  - Place it into _scripts/_ directory.


### ⚙️ Usage
```python3
# Step 1: Prepare a text file with gene symbols (e.g., my_genes.txt) or directly input a gene name
# Step 2: Specify the desired assembly into which retrieve the predictions
# Step 3: Run the full pipeline

./pipeline.sh my_genes.txt GRCh38

./pipeline.sh BRCA1 GRCh38
```

