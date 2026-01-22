print(" FEATURE ENGINEERING...\n")

# ENROLLMENT: Create total and derived columns
enrol['total_enrol'] = enrol['age_0_5'] + enrol['age_5_17'] + enrol['age_18_greater']
enrol['youth_pct'] = (enrol['age_5_17'] / enrol['total_enrol'] * 100).round(2)
enrol['child_pct'] = (enrol['age_0_5'] / enrol['total_enrol'] * 100).round(2)
enrol['adult_pct'] = (enrol['age_18_greater'] / enrol['total_enrol'] * 100).round(2)
enrol['month'] = enrol['date'].dt.to_period('M')
enrol['year_month'] = enrol['date'].dt.strftime('%Y-%m')
print("✅ Enrollment features created")

# DEMOGRAPHIC: Create total and derived columns
demo['total_demo'] = demo['demo_age_5_17'] + demo['demo_age_17_']
demo['demo_youth_pct'] = (demo['demo_age_5_17'] / demo['total_demo'] * 100).round(2)
demo['month'] = demo['date'].dt.to_period('M')
demo['year_month'] = demo['date'].dt.strftime('%Y-%m')
print("✅ Demographic features created")

# BIOMETRIC: Create total and derived columns
bio['total_bio'] = bio['bio_age_5_17'] + bio['bio_age_17_']
bio['bio_youth_pct'] = (bio['bio_age_5_17'] / bio['total_bio'] * 100).round(2)
bio['month'] = bio['date'].dt.to_period('M')
bio['year_month'] = bio['date'].dt.strftime('%Y-%m')
print("✅ Biometric features created")

# Display date ranges
print("\n" + "="*60)
print("📅 DATE RANGES:")
print(f"Enrollment: {enrol['date'].min()} to {enrol['date'].max()}")
print(f"Demographic: {demo['date'].min()} to {demo['date'].max()}")
print(f"Biometric: {bio['date'].min()} to {bio['date'].max()}")
print("="*60)

# Display sample
print("\n📊 Sample of cleaned enrollment data:")
display(enrol[['date', 'state', 'district', 'total_enrol', 'youth_pct', 'child_pct', 'adult_pct']].head())