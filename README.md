# Gene VEP Pipeline
This repository provides a pipeline that takes a gene name or a list of genes as input and returns pathogenicity predictions using VEP (Variant Effect Predictor). The input variants are sourced from a cleaned dataset, available in the [ClinVar data cleaning](https://github.com/AitanaESCI/ClinVar-Data-Cleaning) repo.


## Purpose
This pipeline allows users to:
  - Select variants related to specific genes.
  - Format them into VCF for VEP annotation.
  - Parse and merge VEP output with original variant info.
  - Produce a final dataset with filtered predictions.


## Repository structure
```bash
├── scripts/
│   ├── pipeline.sh 
│   ├── generate_vcf.py 
│   ├── parsing_ClinVar.py
│   └── merging_ClinVar.py 
└── output/
    └── BRCA1/
        ├── vcf_output.vcf
        ├── vep_predictions_BRCA1_GRCh38.txt
        ├── vep_predictions_BRCA1_GRCh38.txt_summary.html
        ├── vep_predictions_BRCA1_GRCh38.csv
        ├── unmatched_variants_BRCA1_GRCh38.txt
        └── merged_output_BRCA1_GRCh38.csv
```

## Dataset overview

#### 1. `scripts/`

This directory contains the core components of the pipeline:
*	`pipeline.sh`: main shell script that organizes the full pipeline — from gene selection to final output.
* `generate_vcf.py`: extracts variants for the selected gene(s) from the cleaned ClinVar dataset and formats them into VCF for VEP processing.
* `parsing_ClinVar.py`: parses the raw VEP output, extracting relevant annotation fields and converting them into a structured `.csv` file.
* `merging_ClinVar.py`: merges parsed VEP predictions with the original ClinVar variant data to produce the final annotated dataset.


#### 2. `output/`

This directory contains an example result to demonstrate pipeline output. Each gene query creates a subfolder named after the gene. For example, the `BRCA1/` folder includes:
* `vcf_output.vcf`: input file used for VEP, containing selected gene variants.
* `vep_predictions_<GENE>_<ASSEMBLY>.txt`: raw VEP output with annotations.
* `vep_predictions_<GENE>_<ASSEMBLY>.txt_summary.html`: VEP’s summary report.
* `vep_predictions_<GENE>_<ASSEMBLY>.csv`: parsed and filtered VEP output in table format.
* `unmatched_variants_<GENE>_<ASSEMBLY>.txt`: list of variants not matched during processing.
* `merged_output_<GENE>_<ASSEMBLY>.csv`: final dataset combining original ClinVar info with parsed VEP annotations.


## Dataset requirement
This pipeline depends on a cleaned dataset prepared in the [ClinVar data cleaning](https://github.com/AitanaESCI/ClinVar-Data-Cleaning) repo.
To use this pipeline:
  - Clone both repositories.
  - Download the `cleaned_ClinVar_dataset.csv` from the ClinVar repository.
  - Place it into `scripts/` directory.


## Usage
```bash
# Step 1: Prepare a text file with gene symbols (e.g., my_genes.txt) or directly input a gene name
# Step 2: Specify the desired assembly to retrieve predictions
# Step 3: Run the pipeline

./pipeline.sh my_genes.txt GRCh38
./pipeline.sh BRCA1 GRCh38
```

**Note**: this pipeline requires a local installation of the VEP command line tool.
You will also need to install certain VEP plugins to retrieve full annotations.
See the `pipeline.sh` script for details on which plugins are expected

