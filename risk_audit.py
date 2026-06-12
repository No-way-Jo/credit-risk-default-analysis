import os
# If running locally outside Kaggle, automatically fetch the dataset file
if not os.path.exists('credit_risk_dataset.csv'):
    print("Downloading source portfolio dataset...")
    os.system('wget -q https://githubusercontent.com') # Pulls a public copy cleanly
-------------------------------------------------------------------------------------
import pandas as pd
import duckdb
import os

# 1. Automatically find the CSV file in your connected dataset
file_path = None
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        if filename.endswith('.csv'):
            file_path = os.path.join(dirname, filename)
            break

print(f"Dynamically connected to file at: {file_path}")

# 2. Load the dataset into your dataframe
df = pd.read_csv(file_path)

# 3. Clean column names to make sure they are SQL-friendly
df.columns = df.columns.str.strip()

# 4. Create the SQL translation function
def run_sql(query):
    return duckdb.query(query).to_df()

# Display a structural preview
print(f"Dataset successfully loaded with {df.shape[0]} records!")
df.head(3)
-------------------------------------------------------------------------------------
query_grade_escalation = """
WITH TotalLoans AS (
    SELECT loan_grade, COUNT(*) as volume_issued
    FROM df
    GROUP BY loan_grade
),
DefaultedLoans AS (
    SELECT loan_grade, COUNT(*) as volume_defaulted
    FROM df
    WHERE loan_status = 1
    GROUP BY loan_grade
)
SELECT 
    t.loan_grade, 
    t.volume_issued, 
    COALESCE(d.volume_defaulted, 0) as volume_defaulted,
    ROUND((COALESCE(d.volume_defaulted, 0) * 100.0 / t.volume_issued), 2) as default_rate_percentage
FROM TotalLoans t
LEFT JOIN DefaultedLoans d ON t.loan_grade = d.loan_grade
ORDER BY t.loan_grade ASC;
"""
run_sql(query_grade_escalation)
-------------------------------------------------------------------------------------
query_leverage_exposure = """
WITH RiskSectors AS (
    SELECT *,
        CASE 
            WHEN loan_percent_income >= 0.40 THEN 'Critical Debt Burden (40%+)'
            WHEN loan_percent_income >= 0.25 THEN 'High Debt Burden (25-39%)'
            ELSE 'Manageable Debt Burden (<25%)'
        END as Leverage_Tier
    FROM df
)
SELECT 
    Leverage_Tier,
    COUNT(*) as Loan_Count,
    ROUND(AVG(person_income), 2) as Avg_Income,
    SUM(CASE WHEN loan_status = 1 THEN loan_amnt ELSE 0 END) as Total_Capital_At_Loss,
    ROUND(SUM(CASE WHEN loan_status = 1 THEN loan_amnt ELSE 0 END) * 100.0 / SUM(loan_amnt), 2) as Capital_Loss_Pct
FROM RiskSectors
GROUP BY Leverage_Tier
ORDER BY Capital_Loss_Pct DESC;
"""

# Execute the query and print the table
run_sql(query_leverage_exposure)
-------------------------------------------------------------------------------------
# Save the summary metrics to your Kaggle Output folder
df_grades = run_sql(query_grade_escalation)
df_leverage = run_sql(query_leverage_exposure)

df_grades.to_csv('credit_grade_risk_matrix.csv', index=False)
df_leverage.to_csv('leverage_loss_exposure.csv', index=False)
print("Success! Summary files are ready for download in your Output panel.")
