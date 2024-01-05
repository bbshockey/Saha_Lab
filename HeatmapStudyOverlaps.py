import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict


# Load the data
file_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/Ranked_Genes2.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Process the data to extract unique study names and terms associated with each study
all_studies = set()
study_terms = defaultdict(set)
for _, row in data.iterrows():
    term = row['Term']
    studies = row['Study Names'].split(', ')
    all_studies.update(studies)
    for study in studies:
        study_terms[study].add(term)

# Create a matrix for the heatmap
studies_list = sorted(list(all_studies))
matrix_size = len(studies_list)
heatmap_matrix = np.zeros((matrix_size, matrix_size))

for i, study1 in enumerate(studies_list):
    for j, study2 in enumerate(studies_list):
        if i <= j:
            shared_terms = len(study_terms[study1].intersection(study_terms[study2]))
            heatmap_matrix[i, j] = shared_terms
            heatmap_matrix[j, i] = shared_terms

# Generate and save the heatmap
plt.figure(figsize=(20, 20))
sns.set(style="white")
ax = sns.heatmap(heatmap_matrix, annot=False, cmap='YlGnBu', square=True, cbar_kws={'label': 'Shared Terms Count'})
ax.set_xticklabels(studies_list, rotation=90, ha="center")
ax.set_yticklabels(studies_list, rotation=0)
ax.set(title="Heatmap of Shared Genes Between Studies", xlabel="Study Names", ylabel="Study Names")
plt.tight_layout()
heatmap_image_path = 'HeatmapAlphabeticalGenes1.5.png'  # Replace with your desired file path
plt.savefig(heatmap_image_path)
plt.close()

