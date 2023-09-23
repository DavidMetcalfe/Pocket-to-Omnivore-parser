from bs4 import BeautifulSoup
import csv
import json

# Load the HTML file
file_path = 'ril_export.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Initialize BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Map HTML attributes to CSV columns
attribute_to_column = {
    'href': 'url',
    'time_added': 'save_at',
    'tags': 'labels'
}

# Find all H1 tags
h1_tags = soup.find_all('h1')
csv_data = []

# Loop through each H1 tag
for h1_tag in h1_tags:
    state = 'SUCCEEDED' if h1_tag.text == 'Unread' else 'ARCHIVED'
    ul_tag = h1_tag.find_next_sibling('ul')
    a_tags = ul_tag.find_all('a')

    # Extract data from each <a> tag
    for a_tag in a_tags:
        row = {'state': state}
        for attribute, column in attribute_to_column.items():
            value = a_tag.get(attribute, None)
            
            # Debug print line
            print(f"Read attribute '{attribute}' with value '{value}' mapped to column '{column}'.")

            if value is not None:
                # Wrap tags in square brackets if it has multiple values
                if attribute == 'tags' and ',' in value:
                    value = f'[{value}]'
                
                row[column] = value
        csv_data.append(row)

# Create the CSV file
csv_file_path = 'output.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url', 'state', 'labels', 'save_at', 'published_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header and rows
    writer.writeheader()
    for row in csv_data:
        writer.writerow(row)
    
