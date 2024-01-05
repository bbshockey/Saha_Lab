import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Load the data
file_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/ranked_terms.csv' 
csv_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/ranked_terms.csv' 

# Replace with your file path
data = pd.read_csv(file_path)
df = pd.read_csv(csv_path)

# Splitting the 'Study Names' into individual studies and counting unique genes per study
study_gene_count = defaultdict(set)
for _, row in df.iterrows():
    studies = row['Study Names'].split(', ')
    term = row['Term']
    for study in studies:
        study_gene_count[study].add(term)

# Counting the number of unique genes in each study and sorting the studies
study_unique_genes = {study: len(genes) for study, genes in study_gene_count.items()}
studies_list = sorted(study_unique_genes, key=study_unique_genes.get, reverse=True)

# Process the data to extract unique study names and terms associated with each study
study_terms = defaultdict(set)
for _, row in data.iterrows():
    term = row['Term']
    studies = row['Study Names'].split(', ')
    for study in studies:
        study_terms[study].add(term)

# Calculate the sum of shared terms for each study
shared_terms_sum = defaultdict(int)
for study1 in study_terms:
    for study2 in study_terms:
        if study1 != study2:
            shared_terms = len(study_terms[study1].intersection(study_terms[study2]))
            shared_terms_sum[study1] += shared_terms

# Sort studies based on the sum of shared terms
studies_list = sorted(shared_terms_sum, key=shared_terms_sum.get, reverse=True)

# Create a matrix for the heatmap
matrix_size = len(studies_list)
heatmap_matrix = np.zeros((matrix_size, matrix_size))

for i, study1 in enumerate(studies_list):
    for j, study2 in enumerate(studies_list):
        if i <= j:
            shared_terms = study_terms[study1].intersection(study_terms[study2])
            unique_terms = len(study_terms[study1]) + len(study_terms[study2]) - len(shared_terms)
            heatmap_matrix[i, j] = len(shared_terms) / unique_terms if unique_terms else 0
            heatmap_matrix[j, i] = heatmap_matrix[i, j]

# Generate and save the heatmap
plt.figure(figsize=(40, 40))
sns.set(style="white")
ax = sns.heatmap(heatmap_matrix, annot=True, cmap='YlGnBu', square=True, cbar_kws={'label': 'Shared Terms Count'})
ax.set_xticklabels(studies_list, rotation=90, ha="center")
ax.set_yticklabels(studies_list, rotation=0)
ax.set(title="Heatmap of Shared Genes Between Studies", xlabel="Study Names", ylabel="Study Names")
plt.tight_layout()
heatmap_image_path = 'HeatmapWeightedRatioGenes1.13.png'  # Replace with your desired file path
plt.savefig(heatmap_image_path)

