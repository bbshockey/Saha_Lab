import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your CSV file
csv_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/Ranked_Genes2.csv'  # Replace with the actual path to your CSV file

# Reading the CSV file
df = pd.read_csv(csv_path)

# Splitting the 'Study Names' into individual studies and counting unique genes per study
study_gene_count = defaultdict(set)
for _, row in df.iterrows():
    studies = row['Study Names'].split(', ')
    term = row['Term']
    for study in studies:
        study_gene_count[study].add(term)

# Counting the number of unique genes in each study
study_unique_genes = {study: len(genes) for study, genes in study_gene_count.items()}

# Sorting studies based on the number of unique genes
sorted_studies = sorted(study_unique_genes, key=study_unique_genes.get, reverse=True)

# Creating a matrix for the heatmap with sorted studies
matrix_size = len(sorted_studies)
heatmap_matrix = np.zeros((matrix_size, matrix_size))

# Filling the heatmap matrix based on shared genes between studies
for i, study1 in enumerate(sorted_studies):
    for j, study2 in enumerate(sorted_studies):
        if i <= j:
            shared_genes = len(study_gene_count[study1].intersection(study_gene_count[study2]))
            heatmap_matrix[i, j] = shared_genes
            heatmap_matrix[j, i] = shared_genes  # Symmetric matrix

# Creating the heatmap
plt.figure(figsize=(20, 20))
sns.set(style="white")
ax = sns.heatmap(heatmap_matrix, annot=False, cmap='YlGnBu', square=True, cbar_kws={'label': 'Shared Terms Count'})
ax.set_xticklabels(sorted_studies, rotation=90, ha="center")
ax.set_yticklabels(sorted_studies, rotation=0)
ax.set(title="Heatmap of Shared Genes Between Studies", xlabel="Study Names", ylabel="Study Names")
plt.tight_layout()
heatmap_image_path = 'HeatmapPotential1.2.png'  # Replace with your desired file path
plt.savefig(heatmap_image_path)
#sns.heatmap(heatmap_matrix, annot=False, cmap="pink", xticklabels=sorted_studies, #yticklabels=sorted_studies)
#plt.title("Heatmap of Shared Genes Between Studies")
#plt.show()
