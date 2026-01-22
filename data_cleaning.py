import pandas as pd
import numpy as np

print(" STARTING ROBUST DATA CLEANING...\n")

def clean_dataframe(df, df_name):
    print(f"Cleaning {df_name}...")
    original_count = len(df)

    # 1. Deduplication (Critical for large datasets)
    df.drop_duplicates(inplace=True)
    dedupe_count = len(df)
    if original_count > dedupe_count:
        print(f"   Dropped {original_count - dedupe_count:,} duplicate rows")

    # 2. Convert Dates
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # 3. Standardize Case (Handle "West Bengal ", "west bengal")
    # Convert to Title Case and strip whitespace
    df['state'] = df['state'].astype(str).str.strip().str.title()
    df['district'] = df['district'].astype(str).str.strip().str.title()

    # 4. Remove Non-Geographic Values / Cross-Column Leaks
    # Filter out rows where 'state' is a number (e.g., "100000")
    df = df[~df['state'].str.match(r'^\d+$')]
    
    # Filter out known districts that appear in the state column
    invalid_states = ['Darbhanga', 'Puttenahalli', 'Nan']
    df = df[~df['state'].isin(invalid_states)]

    # 5. COMPREHENSIVE STATE MAPPING (Fixing Typos & Legacy Names)
    state_mapping = {
        # Typos & Variations
        'West Bangal': 'West Bengal',
        'Westbengal': 'West Bengal',
        'West Bengli': 'West Bengal',
        'Wb': 'West Bengal',
        'Jammu&Kashmir': 'Jammu And Kashmir',
        'Jammu & Kashmir': 'Jammu And Kashmir',
        'Nct Of Delhi': 'Delhi',
        
        # Conjunction Differences
        'Andaman & Nicobar Islands': 'Andaman And Nicobar Islands',
        'Dadra & Nagar Haveli': 'Dadra And Nagar Haveli',
        'Daman & Diu': 'Daman And Diu',
        
        # Combined Territories (Standardizing to the new official merged name if you prefer, 
        # OR keeping them separate. Here we keep separate for historical consistency 
        # unless you want to merge them into "Dadra And Nagar Haveli And Daman And Diu")
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra And Nagar Haveli', 
        
        # Legacy Names (Standardize to CURRENT official names)
        'Orissa': 'Odisha',
        'Pondicherry': 'Puducherry',
        'Uttaranchal': 'Uttarakhand'
    }
    df['state'] = df['state'].replace(state_mapping)
    print(f"  Standardized State names (Fixed 'West Bengli', 'Orissa', etc.)")

    # 6. COMPREHENSIVE DISTRICT MAPPING
    district_mapping = {
        # Compounded vs Separated
        'Yamunanagar': 'Yamuna Nagar',
        'Karimnagar': 'Karim Nagar',
        'Ahmednagar': 'Ahmed Nagar',
        'Mahbubnagar': 'Mahabub Nagar',
        'Mahabubnagar': 'Mahabub Nagar',
        
        # Spelling Variations
        'Chamrajanagar': 'Chamarajanagar',
        'Villupuram': 'Viluppuram',
        'Thiruvananthapuram': 'Thiruvananthpuram',
        
        # Word Substitutions
        'South 24 Parganas': 'South Twenty Four Parganas',
        'North 24 Parganas': 'North Twenty Four Parganas'
    }
    df['district'] = df['district'].replace(district_mapping)
    print(f" Standardized District names (Fixed 'Yamunanagar', 'South 24 Parganas')")

    # 7. Final Clean-up: Drop Invalid Dates or Empty States
    before = len(df)
    df = df.dropna(subset=['state', 'district', 'date'])
    # Ensure pincode is string (preserves leading zeros if present)
    if 'pincode' in df.columns:
         df['pincode'] = df['pincode'].astype(str).str.replace(r'\.0$', '', regex=True)

    after = len(df)
    if dedupe_count > after:
        print(f" Removed {dedupe_count - after:,} rows with invalid/missing data")
    
    return df

# Execute the new cleaning function
enrol = clean_dataframe(enrol, "ENROLLMENT")
demo = clean_dataframe(demo, "DEMOGRAPHIC")
bio = clean_dataframe(bio, "BIOMETRIC")

print("\n" + "="*60)
print(" ROBUST DATA CLEANING COMPLETE!")
print("="*60)