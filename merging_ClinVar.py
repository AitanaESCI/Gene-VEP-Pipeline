import pandas as pd
import sys

def merge_clinvar(gene_name, clinvar_path, vep_path, output_path, log_path):
    clinvar_df = pd.read_csv(clinvar_path, low_memory=False)
    clinvar_df = clinvar_df[clinvar_df['GeneSymbol'] == gene_name]
    vep_df = pd.read_csv(vep_path)

    with open(log_path, "w") as log_file:
        log_file.write("Unmatched Variants Log\n")

    merged_rows = []
    for index, clinvar_row in clinvar_df.iterrows():
        matching_vep = vep_df[vep_df['Feature'] == clinvar_row['Feature']]
        
        if len(matching_vep) > 1:
            matching_vep = matching_vep[matching_vep['Existing_variation'] == clinvar_row['Existing_variation']]
        
        if len(matching_vep) > 1:
            matching_vep = matching_vep[matching_vep['Codons'] == clinvar_row['Codons']]
        
        if len(matching_vep) > 1:
            matching_vep['NaN_count'] = matching_vep.isna().sum(axis=1)
            matching_vep = matching_vep.sort_values(by='NaN_count').iloc[0:1]
        
        if not matching_vep.empty:
            merged_row = {**clinvar_row.to_dict(), **matching_vep.iloc[0].to_dict()}
            merged_rows.append(merged_row)
        else:
            with open(log_path, "a") as log_file:
                log_file.write(f"Variant in row {index} could not be merged\n")
    
    merged_df = pd.DataFrame(merged_rows)
    merged_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 merge_clinvar.py <gene_name> <clinvar_path> <vep_path> <output_path> <log_path>")
        sys.exit(1)

    gene_name = sys.argv[1]
    clinvar_path = sys.argv[2]
    vep_path = sys.argv[3]
    output_path = sys.argv[4]
    log_path = sys.argv[5]

    merge_clinvar(gene_name, clinvar_path, vep_path, output_path, log_path)
