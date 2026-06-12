import pandas as pd
import numpy as np
import os

# ── Load Cleaned Data ─────────────────────────────────────────
df1 = pd.read_csv('data/cleaned/engagement_cleaned.csv')
df2 = pd.read_csv('data/cleaned/advertising_cleaned.csv')
df3 = pd.read_csv('data/cleaned/campaigns_cleaned.csv')

print("✅ Loaded successfully")
print(f"df1: {df1.shape} | df2: {df2.shape} | df3: {df3.shape}")

# ════════════════════════════════════════════════════════════════
# FEATURES — Dataset 1 (Engagement)
# ════════════════════════════════════════════════════════════════
print("\n⚙️  Engineering features for df1...")

# Total interactions
df1['Total_Interactions'] = df1['Likes'] + df1['Comments'] + df1['Shares'] + df1['Saves']

# Virality score
df1['Virality_Score'] = (
    (df1['Shares'] * 3 + df1['Comments'] * 2 + df1['Likes']) /
    (df1['Follower_Count'] + 1) * 100
).round(4)

# Save rate
df1['Save_Rate'] = (
    df1['Saves'] / df1['Views'].replace(0, np.nan) * 100
).round(4)

# View to engagement ratio
df1['View_to_Engagement'] = (
    df1['Total_Interactions'] / df1['Views'].replace(0, np.nan) * 100
).round(4)

# Performance tier
df1['Performance_Tier'] = pd.cut(
    df1['Engagement_Rate'],
    bins=[-np.inf, 1, 3, 6, np.inf],
    labels=['Low', 'Average', 'Good', 'Viral']
)

# Content score
df1['Content_Score'] = (
    df1['Engagement_Rate'] * 0.4 +
    df1['Virality_Score']  * 0.3 +
    df1['Save_Rate'].fillna(0) * 0.3
).round(4)

# Time bucket from Hour_of_Day
df1['Time_Bucket'] = pd.cut(
    df1['Hour_of_Day'],
    bins=[-1, 6, 12, 17, 20, 24],
    labels=['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night']
)

print(f"✅ df1 features done: {df1.shape}")
print(f"   New columns: Total_Interactions, Virality_Score, Save_Rate, View_to_Engagement, Performance_Tier, Content_Score, Time_Bucket")

# ════════════════════════════════════════════════════════════════
# FEATURES — Dataset 2 (Advertising)
# ════════════════════════════════════════════════════════════════
print("\n⚙️  Engineering features for df2...")

# CTR
df2['CTR'] = (
    df2['Clicks'] / df2['Impressions'].replace(0, np.nan) * 100
).round(4)

# Cost Per Click
df2['Cost_Per_Click'] = (
    df2['Acquisition_Cost'] / df2['Clicks'].replace(0, np.nan)
).round(4)

# ROI Segment
df2['ROI_Segment'] = pd.cut(
    df2['ROI'],
    bins=[-np.inf, 0, 100, 300, np.inf],
    labels=['Loss', 'Low', 'Good', 'Excellent']
)

# Extract Age Group and Gender from Target_Audience
df2['Age_Group'] = df2['Target_Audience'].str.extract(r'(\d{2}-\d{2}|\d{2}\+)')
df2['Gender']    = df2['Target_Audience'].str.extract(r'(Men|Women|All)')
df2['Gender']    = df2['Gender'].fillna('All')

# Campaign efficiency score
df2['Efficiency_Score'] = (
    df2['Conversion_Rate'] * 0.5 +
    df2['ROI'] * 0.3 +
    df2['Engagement_Score'] * 0.2
).round(4)

print(f"✅ df2 features done: {df2.shape}")
print(f"   New columns: CTR, Cost_Per_Click, ROI_Segment, Age_Group, Gender, Efficiency_Score")

# ════════════════════════════════════════════════════════════════
# FEATURES — Dataset 3 (Campaigns)
# ════════════════════════════════════════════════════════════════
print("\n⚙️  Engineering features for df3...")

# CTR
df3['CTR'] = (
    df3['Clicks'] / df3['Impressions'].replace(0, np.nan) * 100
).round(4)

# Cost Per Click
df3['Cost_Per_Click'] = (
    df3['Acquisition_Cost'] / df3['Clicks'].replace(0, np.nan)
).round(4)

# ROI Segment
df3['ROI_Segment'] = pd.cut(
    df3['ROI'],
    bins=[-np.inf, 0, 100, 300, np.inf],
    labels=['Loss', 'Low', 'Good', 'Excellent']
)

# Extract Age Group and Gender from Target_Audience
df3['Age_Group'] = df3['Target_Audience'].str.extract(r'(\d{2}-\d{2}|\d{2}\+)')
df3['Gender']    = df3['Target_Audience'].str.extract(r'(Men|Women|All)')
df3['Gender']    = df3['Gender'].fillna('All')

# Campaign efficiency score
df3['Efficiency_Score'] = (
    df3['Conversion_Rate'] * 0.5 +
    df3['ROI'] * 0.3 +
    df3['Engagement_Score'] * 0.2
).round(4)

print(f"✅ df3 features done: {df3.shape}")
print(f"   New columns: CTR, Cost_Per_Click, ROI_Segment, Age_Group, Gender, Efficiency_Score")

# ════════════════════════════════════════════════════════════════
# SAVE ALL FILES
# ════════════════════════════════════════════════════════════════
os.makedirs('data/cleaned', exist_ok=True)
os.makedirs('tableau_exports', exist_ok=True)

# Save featured files
df1.to_csv('data/cleaned/engagement_featured.csv', index=False)
df2.to_csv('data/cleaned/advertising_featured.csv', index=False)
df3.to_csv('data/cleaned/campaigns_featured.csv', index=False)

# Save Tableau exports
df1.to_csv('tableau_exports/engagement_tableau.csv', index=False)
df2.to_csv('tableau_exports/advertising_tableau.csv', index=False)
df3.to_csv('tableau_exports/campaigns_tableau.csv', index=False)

print("\n" + "="*55)
print("✅ FEATURE ENGINEERING COMPLETE!")
print("="*55)
print(f"📁 data/cleaned/engagement_featured.csv  → {df1.shape}")
print(f"📁 data/cleaned/advertising_featured.csv → {df2.shape}")
print(f"📁 data/cleaned/campaigns_featured.csv   → {df3.shape}")
print(f"📁 tableau_exports/ → 3 files ready for Tableau")