
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore




feature_cols = ['age_0_5', 'age_5_17', 'age_18_greater', 'total_enrol', 
                'youth_pct', 'child_pct', 'adult_pct']

X = enrol[feature_cols].copy()
X = X.fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

contamination_levels = [0.01, 0.005, 0.001]  # 1%, 0.5%, 0.1%
results = {}

for contam in contamination_levels:
    iso = IsolationForest(
        contamination=contam, 
        random_state=42,
        n_estimators=100,
        max_samples='auto',
        max_features=1.0
    )
    predictions = iso.fit_predict(X_scaled)
    results[contam] = predictions
    
    n_anomalies = (predictions == -1).sum()
    print(f" Contamination {contam*100:.1f}%: Detected {n_anomalies:,} anomalies ({n_anomalies/len(enrol)*100:.3f}%)")

enrol['anomaly_score'] = results[0.005]


anomalies = enrol[enrol['anomaly_score'] == -1].copy()
normal = enrol[enrol['anomaly_score'] == 1].copy()

print(f"\n DETECTION RESULTS:")
print(f"   • Total records analyzed: {len(enrol):,}")
print(f"   • Anomalies detected: {len(anomalies):,} ({len(anomalies)/len(enrol)*100:.3f}%)")
print(f"   • Normal records: {len(normal):,} ({len(normal)/len(enrol)*100:.3f}%)")

comparison = pd.DataFrame({
    'Normal': normal[feature_cols].mean(),
    'Anomalies': anomalies[feature_cols].mean(),
    'Difference (%)': ((anomalies[feature_cols].mean() - normal[feature_cols].mean()) / normal[feature_cols].mean() * 100).round(2)
})

print("\n ANOMALY VS NORMAL COMPARISON:")
display(comparison)


print("\n" + "="*70)
print("PART 3: ANOMALY TYPE CLASSIFICATION")
print("="*70)

def classify_anomaly(row):
    """Classify why a record is anomalous"""
    reasons = []
    
    if row['total_enrol'] > enrol['total_enrol'].quantile(0.999):
        reasons.append('Extreme Volume')
    
    if row['age_18_greater'] > row['age_0_5']:
        reasons.append('Adult Spike')
    

    if row['age_5_17'] == 0 and row['total_enrol'] > 100:
        reasons.append('Missing Youth Data')
    
    if row['child_pct'] > 95:
        reasons.append('Extreme Child Bias')
    
    if row['total_enrol'] == 0:
        reasons.append('Zero Enrollment')
    
    if row['youth_pct'] > 50:  # Youth should be 32% normally
        reasons.append('Youth Overrepresentation')
    
    return ', '.join(reasons) if reasons else 'Other'

anomalies['anomaly_type'] = anomalies.apply(classify_anomaly, axis=1)


anomaly_type_counts = anomalies['anomaly_type'].value_counts()

print(f"\n ANOMALY TYPE BREAKDOWN:")
display(anomaly_type_counts)


print("\n" + "="*70)
print("PART 4: THE MOST SUSPICIOUS RECORDS")
print("="*70)


top_anomalies = anomalies.sort_values('total_enrol', ascending=False).head(10)

print("\n TOP 10 ANOMALOUS RECORDS (Highest Impact):")
display(top_anomalies[['date', 'state', 'district', 'pincode', 'total_enrol', 
                        'child_pct', 'youth_pct', 'adult_pct', 'anomaly_type']])


anomalous_pincodes = anomalies.groupby('pincode').size().sort_values(ascending=False).head(20)
print(f"\nTOP 20 PINCODES WITH MOST ANOMALOUS RECORDS:")
print(anomalous_pincodes)


print("\n" + "="*70)
print("PART 5: GEOGRAPHIC ANOMALY PATTERNS")
print("="*70)


state_anomaly_rate = enrol.groupby('state').apply(
    lambda x: (x['anomaly_score'] == -1).sum() / len(x) * 100
).sort_values(ascending=False)

print(f"\n STATES WITH HIGHEST ANOMALY RATES:")
display(state_anomaly_rate.head(15).to_frame(name='Anomaly Rate (%)'))


district_anomaly_count = anomalies.groupby(['state', 'district']).size().sort_values(ascending=False).head(20)
print(f"\n DISTRICTS WITH MOST ANOMALOUS RECORDS:")
display(district_anomaly_count.to_frame(name='Anomaly Count'))


print("\n" + "="*70)
print("PART 6: VISUAL ANOMALY ANALYSIS")
print("="*70)

fig, axes = plt.subplots(2, 3, figsize=(20, 12))


ax1 = axes[0, 0]
ax1.scatter(normal['age_0_5'], normal['age_5_17'], alpha=0.3, s=10, c='blue', label='Normal')
ax1.scatter(anomalies['age_0_5'], anomalies['age_5_17'], alpha=0.7, s=30, c='red', 
           edgecolors='black', linewidth=0.5, label='Anomaly')
ax1.set_xlabel('Age 0-5 Enrollments', fontweight='bold')
ax1.set_ylabel('Age 5-17 Enrollments', fontweight='bold')
ax1.set_title('Anomaly Detection: Age Distribution Space', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)


ax2 = axes[0, 1]
ax2.scatter(normal['total_enrol'], normal['youth_pct'], alpha=0.3, s=10, c='blue', label='Normal')
ax2.scatter(anomalies['total_enrol'], anomalies['youth_pct'], alpha=0.7, s=30, c='red',
           edgecolors='black', linewidth=0.5, label='Anomaly')
ax2.set_xlabel('Total Enrollments', fontweight='bold')
ax2.set_ylabel('Youth % (5-17)', fontweight='bold')
ax2.set_title('Anomaly Detection: Volume vs Youth %', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)
ax2.set_xscale('log')


ax3 = axes[0, 2]
if len(anomaly_type_counts) > 0:
    colors_anom = ['#e74c3c', '#e67e22', '#f39c12', '#16a085', '#2980b9']
    anomaly_type_counts.head(5).plot(kind='barh', ax=ax3, color=colors_anom[:len(anomaly_type_counts.head(5))],
                                      edgecolor='black')
    ax3.set_xlabel('Count', fontweight='bold')
    ax3.set_title('Top 5 Anomaly Types', fontsize=12, fontweight='bold')
    ax3.invert_yaxis()


ax4 = axes[1, 0]
state_anomaly_rate.head(20).plot(kind='barh', ax=ax4, color='coral', edgecolor='black')
ax4.set_xlabel('Anomaly Rate (%)', fontweight='bold')
ax4.set_title('Top 20 States by Anomaly Rate', fontsize=12, fontweight='bold')
ax4.invert_yaxis()


ax5 = axes[1, 1]
anomaly_time = enrol.groupby('year_month')['anomaly_score'].apply(lambda x: (x == -1).sum())
normal_time = enrol.groupby('year_month')['anomaly_score'].apply(lambda x: (x == 1).sum())
ax5.plot(anomaly_time.index, anomaly_time.values, marker='o', color='red', linewidth=2, label='Anomalies')
ax5.plot(normal_time.index, normal_time.values, marker='o', color='blue', linewidth=2, label='Normal', alpha=0.5)
ax5.set_xlabel('Month', fontweight='bold')
ax5.set_ylabel('Count', fontweight='bold')
ax5.set_title('Anomaly Trend Over Time', fontsize=12, fontweight='bold')
ax5.legend()
ax5.grid(alpha=0.3)
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)


ax6 = axes[1, 2]
data_box = [normal['total_enrol'], anomalies['total_enrol']]
bp = ax6.boxplot(data_box, labels=['Normal', 'Anomalies'], patch_artist=True,
                 boxprops=dict(facecolor='lightblue', edgecolor='black'),
                 medianprops=dict(color='red', linewidth=2),
                 whiskerprops=dict(color='black'),
                 capprops=dict(color='black'))
bp['boxes'][1].set_facecolor('salmon')
ax6.set_ylabel('Total Enrollments', fontweight='bold')
ax6.set_title('Enrollment Volume Distribution', fontsize=12, fontweight='bold')
ax6.set_yscale('log')
ax6.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('ml_anomaly_detection.png', dpi=300, bbox_inches='tight')
plt.show()



print(" ML ANOMALY DETECTION SUMMARY")


print(f"\n QUANTITATIVE FINDINGS:")
print(f"   • Records analyzed: {len(enrol):,}")
print(f"   • Anomalies detected: {len(anomalies):,} ({len(anomalies)/len(enrol)*100:.3f}%)")
print(f"   • Features used: {len(feature_cols)}")
print(f"   • Most common anomaly type: {anomaly_type_counts.index[0] if len(anomaly_type_counts) > 0 else 'N/A'}")

print(f"\n TOP ANOMALY CHARACTERISTICS:")
if len(anomalies) > 0:
    print(f"   • Avg enrollment (normal): {normal['total_enrol'].mean():,.0f}")
    print(f"   • Avg enrollment (anomalies): {anomalies['total_enrol'].mean():,.0f}")
    print(f"   • Difference: {((anomalies['total_enrol'].mean() / normal['total_enrol'].mean() - 1) * 100):+.1f}%")
    print(f"   • Avg child % (normal): {normal['child_pct'].mean():.1f}%")
    print(f"   • Avg child % (anomalies): {anomalies['child_pct'].mean():.1f}%")
    
print(f"\n GEOGRAPHIC CONCENTRATION:")
print(f"   • State with highest anomaly rate: {state_anomaly_rate.index[0]} ({state_anomaly_rate.iloc[0]:.2f}%)")
print(f"   • States with >1% anomaly rate: {len(state_anomaly_rate[state_anomaly_rate > 1])}")

print(f"\n KEY INSIGHTS:")
if 'Extreme Volume' in anomaly_type_counts.index:
    print(f" {anomaly_type_counts['Extreme Volume']} records show extreme enrollment volumes")
if 'Missing Youth Data' in anomaly_type_counts.index:
    print(f" {anomaly_type_counts['Missing Youth Data']} records missing youth (5-17) data")
if 'Adult Spike' in anomaly_type_counts.index:
    print(f"{anomaly_type_counts['Adult Spike']} records show unusual adult enrollment patterns")

print(" RECOMMENDATIONS:")
print("1. Investigate top 10 anomalous records for data entry errors")
print("2. Audit pincodes with recurring anomalous patterns")
print("3. Review states with >1% anomaly rate for systemic issues")
print("4. Implement automated anomaly flagging in enrollment system")
print("5. Cross-reference anomalies with fraud patterns from Cell 13")

anomalies_export = anomalies[['date', 'state', 'district', 'pincode', 'total_enrol', 
                               'age_0_5', 'age_5_17', 'age_18_greater', 'anomaly_type']]
anomalies_export.to_csv('detected_anomalies.csv', index=False)
print("\n'detected_anomalies.csv'")