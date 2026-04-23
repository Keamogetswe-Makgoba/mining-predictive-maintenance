import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv('predictive_maintenance.csv')
    print("✅ Data loaded successfully!")
    
    
    print("\n--- First 5 Rows of Mining Data ---")
    print(df.head())
    
    
    print("\n--- Missing Values Check ---")
    print(df.isnull().sum())

except FileNotFoundError:
    print("❌ Error: The file 'predictive_maintenance.csv' was not found in this folder.")


print("\n--- Statistical Summary ---")
print(df.describe())


print("\n--- Failure Counts ---")
print(df['Target'].value_counts())


failed_machines = df[df['Target'] == 1]
healthy_machines = df[df['Target'] == 0]

print(f"\nAverage Torque for Healthy: {healthy_machines['Torque [Nm]'].mean():.2f}")
print(f"Average Torque for Failed: {failed_machines['Torque [Nm]'].mean():.2f}")

plt.figure(figsize=(8, 6))
df.boxplot(column='Torque [Nm]', by='Target')


plt.title('Torque Distribution: Healthy (0) vs. Failed (1)')
plt.suptitle('') 
plt.xlabel('Machine Status (0=Healthy, 1=Failed)')
plt.ylabel('Torque [Nm]')


plt.savefig('torque_comparison.png')
print("\n✅ Chart saved as 'torque_comparison.png'!")


df['Temp Diff'] = df['Process temperature [K]'] - df['Air temperature [K]']

print("\n--- Temperature Difference Analysis ---")
print(f"Avg Temp Diff for Healthy: {df[df['Target'] == 0]['Temp Diff'].mean():.2f} K")
print(f"Avg Temp Diff for Failed: {df[df['Target'] == 1]['Temp Diff'].mean():.2f} K")

plt.figure(figsize=(10, 6))
plt.scatter(df['Torque [Nm]'], df['Air temperature [K]'], c=df['Target'], cmap='coolwarm', alpha=0.5)
plt.title('Torque vs. Air Temperature (Red = Failed)')
plt.xlabel('Torque [Nm]')
plt.ylabel('Air Temperature [K]')
plt.colorbar(label='Failure (1=Yes, 0=No)')
plt.savefig('torque_vs_temp.png')
print("\n✅ Scatter plot saved as 'torque_vs_temp.png'!")


print("\n--- Breakdown of Failure Types ---")

real_failures = df[df['Failure Type'] != 'No Failure']
failure_summary = real_failures['Failure Type'].value_counts()
print(failure_summary)


plt.figure(figsize=(10, 6))
failure_summary.plot(kind='bar', color='salmon')
plt.title('Frequency of Specific Mining Equipment Failures')
plt.xlabel('Failure Reason')
plt.ylabel('Number of Occurrences')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('failure_types_bar_chart.png')
print("\n✅ Bar chart saved as 'failure_types_bar_chart.png'!")