print("="*60)
print("📊 UNIVARIATE ANALYSIS: DISTRICT-LEVEL DISTRIBUTION")
print("="*60)

# Aggregate by district
district_enrol = enrol.groupby(['state', 'district']).agg({
    'total_enrol': 'sum',
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
}).reset_index()

district_enrol = district_enrol.sort_values('total_enrol', ascending=False)

print(f"\n📊 Total districts: {len(district_enrol)}")
print(f"📊 Total enrollments: {district_enrol['total_enrol'].sum():,}")
print(f"📊 Average per district: {district_enrol['total_enrol'].mean():,.0f}")
print(f"📊 Median per district: {district_enrol['total_enrol'].median():,.0f}")

print("\n📈 TOP 20 DISTRICTS BY ENROLLMENT:")
display(district_enrol.head(20))

print("\n📉 BOTTOM 20 DISTRICTS BY ENROLLMENT:")
display(district_enrol.tail(20))

# Find districts with very low enrollment
threshold_low = 100
low_enrollment = district_enrol[district_enrol['total_enrol'] < threshold_low]
print(f"\n🚨 DISTRICTS WITH <{threshold_low} ENROLLMENTS:")
print(f"Count: {len(low_enrollment)}")
display(low_enrollment)

# Visualize distribution
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Top 20 districts
district_enrol.head(20).plot(
    x='district', 
    y='total_enrol', 
    kind='barh', 
    ax=axes[0], 
    color='steelblue',
    legend=False
)
axes[0].set_title('Top 20 Districts by Enrollment', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Total Enrollments', fontsize=12)
axes[0].set_ylabel('District', fontsize=12)
axes[0].invert_yaxis()

# Distribution histogram
axes[1].hist(district_enrol['total_enrol'], bins=50, color='coral', edgecolor='black', alpha=0.7)
axes[1].set_title('Distribution of District Enrollments', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Total Enrollments', fontsize=12)
axes[1].set_ylabel('Number of Districts', fontsize=12)
axes[1].axvline(district_enrol['total_enrol'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
axes[1].axvline(district_enrol['total_enrol'].median(), color='green', linestyle='--', linewidth=2, label='Median')
axes[1].legend()

plt.tight_layout()
plt.savefig('district_analysis.png', dpi=300, bbox_inches='tight')
plt.show()