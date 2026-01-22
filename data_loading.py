
print(" Loading Enrollment Data...")
enrol_files = [
    'aadhar enrollment.csv',
    'aadhar enrollment 2.csv',
    'aadhar enrollment 3.csv'
]

enrol_dfs = []
for file in enrol_files:
    df = pd.read_csv(file)
    enrol_dfs.append(df)
    print(f" Loaded {file}: {len(df):,} rows")

enrol = pd.concat(enrol_dfs, ignore_index=True)
print(f"\nTotal Enrollment records: {len(enrol):,}\n")

# Load Demographic data (5 files)
print(" Loading Demographic Data...")
demo_files = [
    'demograph.csv',
    'demograph2.csv',
    'demograph3.csv',
    'demograph4.csv',
    'demograph5.csv'
]

demo_dfs = []
for file in demo_files:
    df = pd.read_csv(file)
    demo_dfs.append(df)
    print(f" Loaded {file}: {len(df):,} rows")

demo = pd.concat(demo_dfs, ignore_index=True)
print(f"\n Total Demographic records: {len(demo):,}\n")

# Load Biometric data (4 files)
print(" Loading Biometric Data...")
bio_files = [
    'biometric.csv',
    'biometric1.csv',
    'biometric3.csv',
    'biometric4.csv'
]

bio_dfs = []
for file in bio_files:
    df = pd.read_csv(file)
    bio_dfs.append(df)
    print(f" Loaded {file}: {len(df):,} rows")

bio = pd.concat(bio_dfs, ignore_index=True)
print(f"\nTotal Biometric records: {len(bio):,}\n")


print(f" SUMMARY:")
print(f"   Enrollment: {len(enrol):,} records")
print(f"   Demographic: {len(demo):,} records")
print(f"   Biometric: {len(bio):,} records")

print("📋 ENROLLMENT DATA STRUCTURE")
print(f"Shape: {enrol.shape}")
print(f"\nColumns: {list(enrol.columns)}")
print(f"\nData types:\n{enrol.dtypes}")
print(f"\nFirst 5 rows:")
display(enrol.head())
print(f"\nBasic stats:")
display(enrol.describe())

print("📋 DEMOGRAPHIC DATA STRUCTURE")

print(f"Shape: {demo.shape}")
print(f"\nColumns: {list(demo.columns)}")
display(demo.head())


print("📋 BIOMETRIC DATA STRUCTURE")
print(f"Shape: {bio.shape}")
print(f"\nColumns: {list(bio.columns)}")
display(bio.head())