import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel(r'C:\flightradar\CALLSIGNS.xls')

# Extract the first three characters from each callsign
df['First_3_Letters'] = df['Callsign'].str[:3]

# Remove duplicate entries
filtered_letters = df['First_3_Letters'].drop_duplicates()

# Save the filtered letters to a new Excel file
filtered_letters.to_excel("filtered_callsigns.xlsx", index=False)
