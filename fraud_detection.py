import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("🔍 CELL 13: CROSS-DATASET INTEGRITY & FRAUD DETECTION")
print("="*70)
print("\n💡 HYPOTHESIS: If enrollments are real, they should have corresponding")
print("   demographic and biometric updates. Mismatches = potential fraud or")
print("   system failures.\n")

# ===================================================================
# PART 1: STATE-LEVEL INTEGRITY CHECK
# ===================================================================
print("="*70)
print("PART 1: STATE-LEVEL CROSS-DATASET ANALYSIS")
print("="*70)

# Aggregate all three datasets by state
s_enrol = enrol.groupby('state')['total_enrol'].sum()
s_demo = demo.groupby('state')['total_demo'].sum()
s_bio = bio.groupby('state')['total_bio'].sum()

# Create comprehensive integrity dataframe
integrity = pd.DataFrame({
    'Enrollments': s_enrol,
    'Demographic_Updates': s_demo,
    'Biometric_Updates': s_bio
}).fillna(0)

# Calculate total activity FIRST (before sorting)
integrity['Total_Activity'] = integrity['Enrollments'] + integrity['Demographic_Updates'] + integrity['Biometric_Updates']

# Calculate ratios
integrity['Demo_to_Enrol_Ratio'] = (integrity['Demographic_Updates'] / integrity['Enrollments']).replace([np.inf, -np.inf], 0)
integrity['Bio_to_Enrol_Ratio'] = (integrity['Biometric_Updates'] / integrity['Enrollments']).replace([np.inf, -np.inf], 0)
integrity['Bio_to_Demo_Ratio'] = (integrity['Biometric_Updates'] / integrity['Demographic_Updates']).replace([np.inf, -np.inf], 0)

# NOW sort by total activity
integrity = integrity.sort_values('Total_Activity', ascending=False)

print("\n📊 TOP 10 STATES BY TOTAL ACTIVITY:")
display(integrity[['Enrollments', 'Demographic_Updates', 'Biometric_Updates', 'Total_Activity']].head(10))

# ===================================================================
# PART 2: FRAUD PATTERN DETECTION
# ===================================================================
print("\n" + "="*70)
print("PART 2: FRAUD PATTERN IDENTIFICATION")
print("="*70)

# Define fraud patterns
fraud_patterns = []

# Pattern 1: Ghost Enrollments (High enrollment, low/no updates)
ghost_states = integrity[
    (integrity['Enrollments'] > 1000) & 
    (integrity['Demo_to_Enrol_Ratio'] < 0.3)
].copy()
if len(ghost_states) > 0:
    ghost_states['Fraud_Type'] = 'Ghost Enrollments (Low Updates)'
    fraud_patterns.append(ghost_states)

# Pattern 2: Phantom Updates (High updates, low/no enrollment)
phantom_states = integrity[
    (integrity['Demographic_Updates'] > 1000) & 
    (integrity['Demo_to_Enrol_Ratio'] > 10)
].copy()
if len(phantom_states) > 0:
    phantom_states['Fraud_Type'] = 'Phantom Updates (No New Enrollments)'
    fraud_patterns.append(phantom_states)

# Pattern 3: Biometric Mismatch (Bio vs Demo don't align)
bio_mismatch = integrity[
    (integrity['Biometric_Updates'] > 1000) & 
    (abs(integrity['Bio_to_Demo_Ratio'] - 1.0) > 0.5)
].copy()
if len(bio_mismatch) > 0:
    bio_mismatch['Fraud_Type'] = 'Biometric-Demographic Mismatch'
    fraud_patterns.append(bio_mismatch)

# Pattern 4: Complete Disconnect (All three datasets don't correlate)
disconnect_states = integrity[
    (integrity['Total_Activity'] > 5000) &
    ((integrity['Demo_to_Enrol_Ratio'] < 0.2) | (integrity['Demo_to_Enrol_Ratio'] > 5)) &
    ((integrity['Bio_to_Demo_Ratio'] < 0.5) | (integrity['Bio_to_Demo_Ratio'] > 2))
].copy()
if len(disconnect_states) > 0:
    disconnect_states['Fraud_Type'] = 'Complete System Disconnect'
    fraud_patterns.append(disconnect_states)

# Combine all fraud patterns (only if we have any)
if len(fraud_patterns) > 0:
    all_fraud = pd.concat(fraud_patterns, ignore_index=False)
    all_fraud = all_fraud[~all_fraud.index.duplicated(keep='first')]  # Remove duplicates
else:
    all_fraud = pd.DataFrame()  # Empty dataframe

print(f"\n🚨 FRAUD PATTERNS DETECTED: {len(all_fraud)} states flagged\n")

if len(all_fraud) > 0:
    print("📋 SUSPICIOUS STATES (Detailed Breakdown):")
    # FIX APPLIED HERE: Sort first, then select columns
    display(all_fraud.sort_values('Total_Activity', ascending=False)[[
        'Enrollments', 'Demographic_Updates', 'Biometric_Updates', 
        'Demo_to_Enrol_Ratio', 'Bio_to_Enrol_Ratio', 'Fraud_Type'
    ]])
else:
    print("✅ No major fraud patterns detected at state level.")

# ===================================================================
# PART 3: DISTRICT-LEVEL DEEP DIVE (Ghost Districts)
# ===================================================================
print("\n" + "="*70)
print("PART 3: DISTRICT-LEVEL FRAUD CHECK (Ghost Districts)")
print("="*70)

# Aggregate by district
d_enrol = enrol.groupby(['state', 'district'])['total_enrol'].sum().reset_index()
d_demo = demo.groupby(['state', 'district'])['total_demo'].sum().reset_index()
d_bio = bio.groupby(['state', 'district'])['total_bio'].sum().reset_index()

# Merge all three
district_integrity = d_enrol.merge(d_demo, on=['state', 'district'], how='outer', suffixes=('_enrol', '_demo'))
district_integrity = district_integrity.merge(d_bio, on=['state', 'district'], how='outer')
district_integrity = district_integrity.fillna(0)

# Rename columns
district_integrity.columns = ['state', 'district', 'enrollments', 'demographic_updates', 'biometric_updates']

# Calculate ratios (handle division by zero)
district_integrity['demo_ratio'] = district_integrity.apply(
    lambda x: x['demographic_updates'] / x['enrollments'] if x['enrollments'] > 0 else 0, axis=1
)
district_integrity['bio_ratio'] = district_integrity.apply(
    lambda x: x['biometric_updates'] / x['enrollments'] if x['enrollments'] > 0 else 0, axis=1
)

# Find ghost districts (enrollment > 100 but ratio < 0.1)
ghost_districts = district_integrity[
    (district_integrity['enrollments'] > 100) & 
    (district_integrity['demo_ratio'] < 0.1)
].sort_values('enrollments', ascending=False)

print(f"\n🚨 GHOST DISTRICTS DETECTED: {len(ghost_districts)}")
print("   (High enrollments but almost NO demographic updates = suspicious)\n")

if len(ghost_districts) > 0:
    print("📋 TOP 20 GHOST DISTRICTS:")
    display(ghost_districts[['state', 'district', 'enrollments', 'demographic_updates', 'demo_ratio']].head(20))

# Find dead districts (zero activity across all datasets)
dead_districts = district_integrity[
    (district_integrity['enrollments'] == 0) & 
    (district_integrity['demographic_updates'] == 0) & 
    (district_integrity['biometric_updates'] == 0)
]

print(f"\n💀 COMPLETELY DEAD DISTRICTS: {len(dead_districts)}")
print("   (Zero activity across all three datasets = service delivery failure)\n")

if len(dead_districts) > 0 and len(dead_districts) <= 20:
    print("📋 DEAD DISTRICTS:")
    display(dead_districts[['state', 'district']])
elif len(dead_districts) > 20:
    print(f"📋 Sample of DEAD DISTRICTS (showing first 20 of {len(dead_districts)}):")
    display(dead_districts[['state', 'district']].head(20))

# ===================================================================
# PART 4: VISUALIZATIONS
# ===================================================================
print("\n" + "="*70)
print("PART 4: VISUAL EVIDENCE")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Chart 1: State-level ratios (sorted by Demo/Enrol ratio)
integrity_sorted = integrity.sort_values('Demo_to_Enrol_Ratio')
ax1 = axes[0, 0]
x = np.arange(len(integrity_sorted))
width = 0.35
ax1.bar(x - width/2, integrity_sorted['Demo_to_Enrol_Ratio'], width, label='Demo/Enrol', color='steelblue', alpha=0.8)
ax1.bar(x + width/2, integrity_sorted['Bio_to_Enrol_Ratio'], width, label='Bio/Enrol', color='coral', alpha=0.8)
ax1.axhline(1, color='red', linestyle='--', linewidth=2, label='1:1 Expected')
ax1.axhline(0.2, color='orange', linestyle=':', linewidth=2, label='Fraud Threshold (0.2)')
ax1.set_xlabel('States (sorted by ratio)', fontweight='bold')
ax1.set_ylabel('Ratio (Updates per Enrollment)', fontweight='bold')
ax1.set_title('Cross-Dataset Ratios by State', fontsize=14, fontweight='bold')
ax1.legend()
ax1.set_xticks([])

# Chart 2: Scatter plot - Enrollments vs Demographic Updates
ax2 = axes[0, 1]
scatter = ax2.scatter(integrity['Enrollments'], integrity['Demographic_Updates'], 
                     s=integrity['Biometric_Updates']/100, alpha=0.6, c=integrity['Demo_to_Enrol_Ratio'],
                     cmap='RdYlGn', edgecolors='black', linewidth=0.5)
# Add 1:1 line
max_val = max(integrity['Enrollments'].max(), integrity['Demographic_Updates'].max())
ax2.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='1:1 Line')
ax2.set_xlabel('New Enrollments', fontweight='bold')
ax2.set_ylabel('Demographic Updates', fontweight='bold')
ax2.set_title('Enrollment vs Updates (Size = Biometric Activity)', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax2, label='Demo/Enrol Ratio')

# Chart 3: Distribution of ratios
ax3 = axes[1, 0]
# Filter out extreme outliers for better visualization
ratios_filtered = integrity['Demo_to_Enrol_Ratio'][integrity['Demo_to_Enrol_Ratio'] < 20]
ax3.hist(ratios_filtered, bins=30, color='teal', alpha=0.7, edgecolor='black')
ax3.axvline(1, color='red', linestyle='--', linewidth=2, label='Ideal (1:1)')
ax3.axvline(0.2, color='orange', linestyle=':', linewidth=2, label='Fraud Threshold')
ax3.axvline(5, color='purple', linestyle=':', linewidth=2, label='Stagnation Threshold')
ax3.set_xlabel('Demo-to-Enrollment Ratio', fontweight='bold')
ax3.set_ylabel('Number of States', fontweight='bold')
ax3.set_title('Distribution of Cross-Dataset Ratios', fontsize=14, fontweight='bold')
ax3.legend()
ax3.grid(alpha=0.3)

# Chart 4: Fraud type breakdown
ax4 = axes[1, 1]
if len(all_fraud) > 0:
    fraud_counts = all_fraud['Fraud_Type'].value_counts()
    colors_fraud = ['#ff6b6b', '#ee5a6f', '#c44569', '#774c60']
    fraud_counts.plot(kind='barh', ax=ax4, color=colors_fraud[:len(fraud_counts)], edgecolor='black')
    ax4.set_xlabel('Number of States', fontweight='bold')
    ax4.set_title('Fraud Pattern Breakdown', fontsize=14, fontweight='bold')
    ax4.invert_yaxis()
else:
    ax4.text(0.5, 0.5, 'No Major Fraud Patterns Detected', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='green')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')

plt.tight_layout()
plt.savefig('cross_dataset_fraud_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ===================================================================
# PART 5: SUMMARY REPORT
# ===================================================================
print("\n" + "="*70)
print("📊 FRAUD DETECTION SUMMARY REPORT")
print("="*70)

print(f"\n🔢 QUANTITATIVE FINDINGS:")
print(f"   • Total states analyzed: {len(integrity)}")
print(f"   • States flagged for fraud patterns: {len(all_fraud)}")
print(f"   • Ghost districts (high enrol, low updates): {len(ghost_districts)}")
print(f"   • Dead districts (zero activity): {len(dead_districts)}")

print(f"\n📈 RATIO STATISTICS:")
print(f"   • Mean Demo/Enrol ratio: {integrity['Demo_to_Enrol_Ratio'].mean():.2f}")
print(f"   • Median Demo/Enrol ratio: {integrity['Demo_to_Enrol_Ratio'].median():.2f}")
print(f"   • States with ratio <0.2 (ghost risk): {len(integrity[integrity['Demo_to_Enrol_Ratio'] < 0.2])}")
print(f"   • States with ratio >5 (stagnation): {len(integrity[integrity['Demo_to_Enrol_Ratio'] > 5])}")

print(f"\n💡 KEY INSIGHTS:")
if len(all_fraud) > 0:
    print(f"   🚨 {len(all_fraud)} states show suspicious cross-dataset patterns")
    most_common_fraud = all_fraud['Fraud_Type'].value_counts().index[0]
    print(f"   🚨 Primary fraud type: {most_common_fraud}")
else:
    print(f"   ✅ State-level data integrity appears normal")
    
if len(ghost_districts) > 0:
    print(f"   🚨 {len(ghost_districts)} districts flagged as 'ghost enrollments'")
    top_ghost = ghost_districts.iloc[0]
    print(f"   🚨 Top ghost district: {top_ghost['district']}, {top_ghost['state']} ({top_ghost['enrollments']:,.0f} enrollments)")
    
if len(dead_districts) > 0:
    print(f"   ⚠️  {len(dead_districts)} districts have ZERO activity (service failure)")

print("\n" + "="*70)
print("💼 RECOMMENDATIONS:")
print("="*70)
print("1. Audit flagged districts for enrollment authenticity")
print("2. Investigate states with extreme ratios (<0.2 or >5)")
print("3. Deploy mobile camps to 'dead districts'")
print("4. Implement real-time cross-dataset validation rules")
print("5. Monitor ghost districts monthly for pattern evolution")
print("="*70)