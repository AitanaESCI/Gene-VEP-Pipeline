#!/bin/bash

<< Pipeline_Description
Pipeline for creating VCF file for a given gene and running VEP predictions

1. VCF Generation

    Input: Gene name
    Output: VCF file with all possible nonsynonymous variants

2. Variant Annotation

    Input: VCF file
    Output: VEP predictions + frequency data, etc

3. CSV Parsing

    Input: VEP predictions output file
    Output: Structured CSV file containing predictions

Pipeline_Description


# Generate VCF from a gene name
generate_vcf() {
    local gene_name=$1
    echo "Generating VCF file..."
    mkdir -p "/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name"
    python3 generate_vcf.py --gene_name $gene_name --output "/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vcf_output.vcf"
}


# Run VEP predictions on the VCF file
run_vep() {
    local input_vcf=$1
    local gene_name=$2
    local assembly=$3  # Assembly version: GRCh37 or GRCh38

    echo "Running VEP..."
    
    output_file="/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vep_predictions_${gene_name}_${assembly}.txt"

    /home/aitanadiaz/ensembl-vep/./vep -i "$input_vcf" -o "$output_file" --offline \
        --assembly $assembly \
        --symbol --transcript_version --ccds --protein --uniprot --canonical \
        --hgvs --fasta /home/aitanadiaz/ensembl-vep/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz \
        --af --af_1kg --af_gnomade --af_gnomadg --max_af \
        --sift b --polyphen b \
        --plugin AlphaMissense,file=/home/aitanadiaz/ensembl-vep/plugins/AlphaMissense_${assembly}.tsv.gz \
        --plugin Blosum62 \
        --plugin CADD,snv=/home/aitanadiaz/ensembl-vep/plugins/whole_genome_SNVs_${assembly}.tsv.gz \
        --plugin ClinPred,file=/home/aitanadiaz/ensembl-vep/plugins/ClinPred_${assembly}_tabbed.tsv.gz \
        --plugin dbNSFP,/home/aitanadiaz/ensembl-vep/plugins/dbNSFP5.1a.grch38.gz,VEST4_score,VEST4_rankscore,BayesDel_addAF_pred,BayesDel_addAF_score \
        --plugin EVE,file=/home/aitanadiaz/ensembl-vep/plugins/EVE/eve_merged.vcf.gz \
        --plugin PrimateAI,/home/aitanadiaz/ensembl-vep/plugins/PrimateAI_scores_v0.2_${assembly}_sorted.tsv.bgz \
        --plugin REVEL,file=/home/aitanadiaz/ensembl-vep/plugins/new_tabbed_revel_${assembly}.tsv.gz
        #--plugin BayesDel,file=/home/aitanadiaz/ensembl-vep/plugins/BayesDel_170824_addAF/BayesDel_170824_addAF_all_scores.txt.gz \
        #--plugin VARITY,file=/home/aitanadiaz/ensembl-vep/plugins/varity_all_predictions.tsv.gz
}


# Parse VEP output to CSV
parse_vep() {
    local gene_name=$1
    local vep_file="/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vep_predictions_${gene_name}_${assembly}.txt"
    local output_csv="/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vep_predictions_${gene_name}_${assembly}.csv"

    echo "Parsing VEP output..."
    python3 parsing_ClinVar.py "$vep_file" "$output_csv"
    echo "Output file is in $output_csv"
}


# Merge ClinVar original dataset with VEP output
merge_clinvar_vep() {
    local gene_name=$1
    local assembly=$2
    local clinvar_file="/home/aitanadiaz/Desktop/variant_pipeline/scripts/cleaned_ClinVar_dataset.csv"
    local vep_file="/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vep_predictions_${gene_name}_${assembly}.csv"
    local output_file="/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/merged_output_${gene_name}_${assembly}.csv"
    local log_file="/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/unmatched_variants_${gene_name}_${assembly}.txt"

    echo "Merging back with ClinVar dataset..."
    python3 merging_ClinVar.py "$gene_name" "$clinvar_file" "$vep_file" "$output_file" "$log_file"
    echo "Unmatched variants logged in $log_file"
}



main() {
    if [ $# -lt 1 ]; then
        echo "Usage: $0 <GENE LIST FILE or GENE NAME> [GRCh37|GRCh38|both]"
        exit 1
    fi

    local input=$1
    local assembly=${2:-both}

    if [ -f "$input" ]; then
        # process gene list from file
        while IFS= read -r gene_name || [ -n "$gene_name" ]; do
            gene_name=$(echo "$gene_name" | xargs)
            if [ -z "$gene_name" ]; then continue; fi
            echo "Processing gene: $gene_name"
            generate_vcf "$gene_name"
            if [[ "$assembly" == "GRCh37" || "$assembly" == "both" ]]; then
                run_vep "/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vcf_output.vcf" "$gene_name" GRCh37
                parse_vep "$gene_name"
            fi
            if [[ "$assembly" == "GRCh38" || "$assembly" == "both" ]]; then
                run_vep "/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vcf_output.vcf" "$gene_name" GRCh38
                parse_vep "$gene_name"
            fi
            merge_clinvar_vep "$gene_name" "$assembly"
        done < "$input"
    else
        # if input is a single gene name
        gene_name="$input"
        echo "Processing single gene: $gene_name"
        generate_vcf "$gene_name"
        if [[ "$assembly" == "GRCh37" || "$assembly" == "both" ]]; then
            run_vep "/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vcf_output.vcf" "$gene_name" GRCh37
            parse_vep "$gene_name"
        fi
        if [[ "$assembly" == "GRCh38" || "$assembly" == "both" ]]; then
            run_vep "/home/aitanadiaz/Desktop/variant_pipeline/output/$gene_name/vcf_output.vcf" "$gene_name" GRCh38
            parse_vep "$gene_name"
        fi
        merge_clinvar_vep "$gene_name" "$assembly"
    fi
}


main "$@"
