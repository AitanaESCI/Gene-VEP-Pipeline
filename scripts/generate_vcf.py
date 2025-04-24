import pandas as pd
import argparse
import warnings
warnings.simplefilter("ignore")


def create_vcf(variant_df, output_file="output.vcf"):
    """
    Create a VCF file from variant DataFrame
    
    Parameters:
        variant_df: DataFrame with columns Chromosome, ReferenceAlleleVCF, PositionVCF, AlternateAlleleVCF
        output_file: String, path to output VCF file
    """

    # Open file and write header
    with open(output_file, 'w') as f:
        # Iterate through DataFrame rows
        for _, row in variant_df.iterrows():
            # Extract values from DataFrame
            chrom = str(row['Chromosome'])
            pos = row['PositionVCF']
            ref = row['ReferenceAlleleVCF']
            alt = row['AlternateAlleleVCF']
            
            # Format chromosome number (add 'chr' prefix if needed)
            chrom = f"{chrom}" if not chrom.startswith('chr') else chrom
            
            # Create VCF line with mandatory fields
            vcf_line = f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t.\tPASS\t.\n"
            f.write(vcf_line)


def filter_variants_by_gene(variant_df, gene_name):
    return variant_df[variant_df['GeneSymbol'] == gene_name]




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate VCF file for a specific gene.')
    parser.add_argument('--gene_name', required=True, help='Gene name')
    parser.add_argument('--output', required=True, help='Output VCF file path')

    args = parser.parse_args()

    # Load cleaned variant data: ClinVar or Humsavar
    clinvar_data = pd.read_csv('/home/aitanadiaz/Desktop/variant_pipeline/scripts/cleaned_ClinVar_dataset.csv')

    # Filter variants by gene
    filtered_variants = filter_variants_by_gene(clinvar_data, args.gene_name)

    # Create VCF
    create_vcf(filtered_variants[['Chromosome', 'ReferenceAlleleVCF', 'PositionVCF', 'AlternateAlleleVCF']], args.output)
