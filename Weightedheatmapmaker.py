import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def create_heatmap_with_summed_shared_terms(csv_path, output_file_path):
    data = pd.read_csv(csv_path)

    # Prepare a dictionary to hold the terms for each study
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
    sorted_studies = sorted(shared_terms_sum, key=shared_terms_sum.get, reverse=True)

    # Create a matrix for the heatmap based on the sorted studies
    matrix_size = len(sorted_studies)
    heatmap_matrix = np.zeros((matrix_size, matrix_size))

    for i, study1 in enumerate(sorted_studies):
        for j, study2 in enumerate(sorted_studies):
            shared_terms = len(study_terms[study1].intersection(study_terms[study2]))
            heatmap_matrix[i, j] = shared_terms

# Print each study name and the sum of its shared terms
    for study in sorted_studies:
        print(f"Study: {study}, Sum of shared terms: {shared_terms_sum[study]}")


    # Generate and save the heatmap
    plt.figure(figsize=(20, 20))
    sns.set(style="white")
    ax = sns.heatmap(heatmap_matrix, annot=False, cmap='YlGnBu', square=True, cbar_kws={'label': 'Shared Terms Count'})
    ax.set_xticklabels(sorted_studies, rotation=90, ha="center")
    ax.set_yticklabels(sorted_studies, rotation=0)
    ax.set(title="Heatmap of Summed Shared Genes Between Studies", xlabel="Study Names", ylabel="Study Names")
    plt.tight_layout()
    plt.savefig(output_file_path)

    return output_file_path

# Specify the path to your CSV file and the desired output file path
csv_file_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/Ranked_Genes2.csv'
output_heatmap_path = 'HeatmapWeighted1.2.png'

# Run the function
create_heatmap_with_summed_shared_terms(csv_file_path, output_heatmap_path)
