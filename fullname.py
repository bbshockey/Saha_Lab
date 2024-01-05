import pandas as pd
from Bio import Entrez
import time

Entrez.email = "bjornshockey@gmail.com"

def get_gene_name(entrez_id):
    try:
        handle = Entrez.efetch(db="gene", id=entrez_id, retmode="xml")
        records = Entrez.read(handle)
        if 'Entrezgene_prot' in records[0] and 'Prot-ref_desc' in records[0]['Entrezgene_prot']['Prot-ref']:
            return records[0]['Entrezgene_prot']['Prot-ref']['Prot-ref_desc']
        return "Name not found"
    except Exception as e:
        return f"Error: {e}"

# Load the CSV file
file_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/Updated_AllStudiesWithTerms6.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

def process_entrez_ids(entrez_ids):
    gene_names = []
    for entrez_id in entrez_ids.split(','):
        gene_name = get_gene_name(entrez_id.strip())
        gene_names.append(gene_name)
        time.sleep(0.3)  # To prevent overloading the server with requests
    return ', '.join(gene_names)

# Applying the function to the EntrezIDs column and creating a new column for the gene names
df['Full_Gene_Names'] = df['EntrezIDs'].apply(process_entrez_ids)

# Save the updated DataFrame to a new CSV file
df.to_csv('Fullnames_AllStudiesWithTerms.csv', index=False)
