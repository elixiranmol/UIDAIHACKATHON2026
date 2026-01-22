print(" UNIVARIATE ANALYSIS: STATE-WISE ENROLLMENT")

# Aggregate by state
state_enrol = enrol.groupby('state').agg({
    'total_enrol': 'sum',
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
}).sort_values('total_enrol', ascending=False)

# Calculate percentages
state_enrol['child_pct'] = (state_enrol['age_0_5'] / state_enrol['total_enrol'] * 100).round(2)
state_enrol['youth_pct'] = (state_enrol['age_5_17'] / state_enrol['total_enrol'] * 100).round(2)
state_enrol['adult_pct'] = (state_enrol['age_18_greater'] / state_enrol['total_enrol'] * 100).round(2)

print("\n📈 TOP 15 STATES BY ENROLLMENT:")
display(state_enrol.head(15))

print("\n📉 BOTTOM 10 STATES BY ENROLLMENT:")
display(state_enrol.tail(10))

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Top 15 states
state_enrol['total_enrol'].head(15).plot(kind='barh', ax=axes[0], color='steelblue')
axes[0].set_title('Top 15 States by Total Enrollment', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Total Enrollments', fontsize=12)
axes[0].invert_yaxis()

# Bottom 10 states
state_enrol['total_enrol'].tail(10).plot(kind='barh', ax=axes[1], color='coral')
axes[1].set_title('Bottom 10 States by Total Enrollment', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Total Enrollments', fontsize=12)
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig('state_wise_enrollment.png', dpi=300, bbox_inches='tight')
plt.show()

# Summary statistics
print("\n" + "="*60)
print("📊 SUMMARY STATISTICS:")
print(f"Total states: {len(state_enrol)}")
print(f"Total enrollments: {state_enrol['total_enrol'].sum():,}")
print(f"Average per state: {state_enrol['total_enrol'].mean():,.0f}")
print(f"Median per state: {state_enrol['total_enrol'].median():,.0f}")
print(f"Std deviation: {state_enrol['total_enrol'].std():,.0f}")
print("="*60)