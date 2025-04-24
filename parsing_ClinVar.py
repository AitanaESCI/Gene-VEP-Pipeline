import pandas as pd
import sys
import re

def extract_extra_fields(extra):
    """Extract key value pairs from the Extra column."""
    if pd.isna(extra):
        return {}
    return dict(item.split('=') for item in extra.split(';') if '=' in item)

def split_prediction_score(value):
    """Split predictor scores formatted as 'tolerated(0.24)' into label and score."""
    if pd.isna(value):
        return 'NA', 'NA'
    match = re.match(r'([^()]+)\(([\d.]+)\)', str(value))
    if match:
        return match.group(1), match.group(2)
    return value, 'NA'

def parse_vest4_score(vest4_value):
    """Extract the highest VEST4 score from a comma separated list."""
    scores = [float(score) if score != '.' and score != 'NA' else 0 for score in vest4_value.split(',')]
    return max(scores)

def process_vep_output(df):
    """Transform VEP output by extracting fields from Extra column and renaming columns."""

    extra_fields = ['SYMBOL', 'HGNC_ID', 'CANONICAL', 'SWISSPROT', 'UNIPARC', 'UNIPROT_ISOFORM', 
                    'SIFT', 'PolyPhen', 'am_class', 'am_pathogenicity', 'BayesDel_addAF_pred',
                    'BayesDel_addAF_score', 'CADD_PHRED', 'CADD_RAW', 'ClinPred', 'VEST4_rankscore', 
                    'VEST4_score', 'EVE_CLASS', 'EVE_SCORE', 'PrimateAI', 'REVEL']

    extracted = df['Extra'].apply(lambda x: extract_extra_fields(x) if pd.notna(x) else {})

    for field in extra_fields:
        df[field] = extracted.apply(lambda x: x.get(field, 'NA'))

    #print(df.head())

    df[['SIFT_label', 'SIFT_score']] = df['SIFT'].apply(lambda x: pd.Series(split_prediction_score(x)))
    df[['PolyPhen_label', 'PolyPhen_score']] = df['PolyPhen'].apply(lambda x: pd.Series(split_prediction_score(x)))

    rename_mapping = {
        'am_class': 'AM_label',
        'am_pathogenicity': 'AM_score',
        'BayesDel_addAF_pred': 'BayesDel_label',
        'BayesDel_addAF_score': 'BayesDel_score',
        'CADD_PHRED': 'CADD_PHRED_score',
        'CADD_RAW': 'CADD_RAW_score',
        'ClinPred': 'ClinPred_score',
        'VEST4_rankscore': 'VEST4_rankscore',
        'EVE_CLASS': 'EVE_label',
        'EVE_SCORE': 'EVE_score',
        'PrimateAI': 'PrimateAI_score',
        'REVEL': 'REVEL_score',
        'SYMBOL': 'GeneSymbol'
    }
    df.rename(columns=rename_mapping, inplace=True)

    #print(df.columns)

    df['VEST4_score'] = df['VEST4_score'].apply(parse_vest4_score)

    selected_columns = [
        'Existing_variation', 'Location', 'Gene', 'Feature', 'Feature_type', 
        'Canonical', 'Consequence', 'Swissprot', 'Uniparc', 'Uniprot_isoform',
        'cDNA_position', 'CDS_position', 'Protein_position', 'Amino_acids', 
        'Codons', 'GeneSymbol', 'HGNC_ID', 'SIFT_label', 'SIFT_score', 
        'PolyPhen_label', 'PolyPhen_score', 'BayesDel_label', 'BayesDel_score', 
        'CADD_PHRED_score', 'CADD_RAW_score', 'ClinPred_score', 'VEST4_score', 
        'VEST4_rankscore', 'EVE_label', 'EVE_score', 'REVEL_score', 
        'PrimateAI_score', 'AM_label', 'AM_score'
    ]

    df = df.reindex(columns=selected_columns, fill_value='NA')

    return df

def parse_vep_output(input_file, output_file):
    """Read VEP output, process it, and save as CSV."""

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # find header row (starts with #Uploaded_variation)
    header_idx = next(i for i, line in enumerate(lines) if line.startswith("#Uploaded_variation"))

    # read data while skipping metadata lines
    df = pd.read_csv(input_file, sep='\t', skiprows=header_idx, dtype=str)

    #print(df.head())

    df = process_vep_output(df)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parse_vep_output(sys.argv[1], sys.argv[2])
