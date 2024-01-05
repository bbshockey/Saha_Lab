import pandas as pd
from collections import Counter

# Load the data
file_path = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/Updated_AllStudiesWithTerms2.csv'  # Replace with the path to your CSV file
data = pd.read_csv(file_path)

# Combine terms from all studies into a single list
all_terms = []
study_terms_map = {}  # Dictionary to store study names for each term
for index, row in data.iterrows():
    terms = row['Terms']
    study_name = row['Abbreviated.Name']
    if isinstance(terms, str):
        term_list = terms.split(', ')
        all_terms.extend(term_list)
        for term in term_list:
            study_names = study_terms_map.get(term, [])
            study_names.append(study_name)
            study_terms_map[term] = study_names

# Count the occurrences of each term
term_counts = Counter(all_terms)

# Sort the term-count pairs by count in descending order
sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)

# Create a DataFrame to store the ranked list
ranked_df = pd.DataFrame(sorted_terms, columns=['Term', 'Count'])

# Add a column with study names for each term
ranked_df['StudyNames'] = ranked_df['Term'].apply(lambda term: ', '.join(study_terms_map.get(term, [])))

# Save the ranked list to a CSV file
output_csv = '/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/ranked_terms.csv'  # Replace with your desired output file path
ranked_df.to_csv(output_csv, index=False)

print(f"Ranked list of terms saved to {output_csv}")