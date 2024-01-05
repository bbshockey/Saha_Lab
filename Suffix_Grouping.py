import pandas as pd

# Load the CSV file
df = pd.read_csv('/Users/bjorn/Desktop/DavidAutomationCode/3heatmappys/ranked_terms.csv')

# Function to extract all suffixes from study names
def extract_all_suffixes(study_names):
    return [study.split('-')[-1] for study in study_names.split(', ') if '-' in study]

# Apply the function to get all suffixes for each term
df['All_Suffixes'] = df['Study Names'].apply(extract_all_suffixes)

# Function to check if all studies have the same suffix
def has_single_suffix_group(suffixes):
    return len(set(suffixes)) == 1

# Applying the function to filter the DataFrame
single_suffix_df = df[df['All_Suffixes'].apply(has_single_suffix_group)]

# Creating the final DataFrame with the required format
final_grouped_terms = []
for _, row in single_suffix_df.iterrows():
    term = row['Term']
    suffix = row['All_Suffixes'][0]  # Since all studies have the same suffix, pick the first one
    studies = ', '.join(set([study for study in row['Study Names'].split(', ') if study.endswith(suffix)]))
    final_grouped_terms.append({'Term': term, 'Studies': studies})

final_df = pd.DataFrame(final_grouped_terms)

# Save to CSV
final_df.to_csv('/path/to/output/terms_single_suffix_group.csv', index=False)
