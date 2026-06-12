import pandas as pd
import numpy as np
import os

# ── Load Raw Data ─────────────────────────────────────────────
df1 = pd.read_csv('data/raw/social_media_engagement.csv')
df2 = pd.read_csv('data/raw/social_media_advertising.csv')
df3 = pd.read_csv('data/raw/marketing_campaign_perf.csv')

print("✅ Loaded successfully")
print(f"df1: {df1.shape} | df2: {df2.shape} | df3: {df3.shape}")

# ════════════════════════════════════════════════════════════════
# CLEAN DATASET 1 — Social Media Engagement
# ════════════════════════════════════════════════════════════════
print("\n🔧 Cleaning Dataset 1...")

# Fix datetime
df1['Timestamp'] = pd.to_datetime(df1['Timestamp'], dayfirst=True)

# Check nulls
print("Nulls:\n", df1.isnull().sum())

# Remove duplicates
before = len(df1)
df1.drop_duplicates(subset='Post_ID', inplace=True)
print(f"Duplicates removed: {before - len(df1)}")

# Fix data types
df1['Has_Media']    = df1['Has_Media'].astype(bool)
df1['Is_Verified']  = df1['Is_Verified'].astype(bool)
df1['Engagement_Rate'] = pd.to_numeric(df1['Engagement_Rate'], errors='coerce')

# Add time features from Timestamp
df1['Year']         = df1['Timestamp'].dt.year
df1['Month']        = df1['Timestamp'].dt.month
df1['Month_Name']   = df1['Timestamp'].dt.strftime('%B')
df1['Quarter']      = df1['Timestamp'].dt.quarter
df1['Week']         = df1['Timestamp'].dt.isocalendar().week.astype(int)

# Remove outliers in Likes, Views using IQR
for col in ['Likes', 'Views', 'Comments', 'Shares']:
    Q1 = df1[col].quantile(0.25)
    Q3 = df1[col].quantile(0.75)
    IQR = Q3 - Q1
    before = len(df1)
    df1 = df1[df1[col].between(Q1 - 3*IQR, Q3 + 3*IQR)]
    print(f"Outliers removed in {col}: {before - len(df1)}")

print(f"✅ df1 cleaned: {df1.shape}")

# ════════════════════════════════════════════════════════════════
# CLEAN DATASET 2 — Advertising Campaigns
# ════════════════════════════════════════════════════════════════
print("\n🔧 Cleaning Dataset 2...")

df2['Date'] = pd.to_datetime(df2['Date'], dayfirst=True)

# Check nulls
print("Nulls:\n", df2.isnull().sum())

# Remove duplicates
before = len(df2)
df2.drop_duplicates(inplace=True)
print(f"Duplicates removed: {before - len(df2)}")

# Fix numeric columns
df2['Conversion_Rate']  = pd.to_numeric(df2['Conversion_Rate'], errors='coerce')
df2['Acquisition_Cost'] = pd.to_numeric(df2['Acquisition_Cost'], errors='coerce')
df2['ROI']              = pd.to_numeric(df2['ROI'], errors='coerce')
df2['Clicks']           = pd.to_numeric(df2['Clicks'], errors='coerce')
df2['Impressions']      = pd.to_numeric(df2['Impressions'], errors='coerce')

# Drop rows where ROI or Impressions is null (critical columns)
df2.dropna(subset=['ROI', 'Impressions', 'Clicks'], inplace=True)

# Logical check: Clicks can't exceed Impressions
df2 = df2[df2['Clicks'] <= df2['Impressions']]

# Add time features
df2['Year']       = df2['Date'].dt.year
df2['Month']      = df2['Date'].dt.month
df2['Month_Name'] = df2['Date'].dt.strftime('%B')
df2['Quarter']    = df2['Date'].dt.quarter

print(f"✅ df2 cleaned: {df2.shape}")

# ════════════════════════════════════════════════════════════════
# CLEAN DATASET 3 — Marketing Campaigns
# ════════════════════════════════════════════════════════════════
print("\n🔧 Cleaning Dataset 3...")

df3['Date'] = pd.to_datetime(df3['Date'], dayfirst=True)

# Check nulls
print("Nulls:\n", df3.isnull().sum())

# Remove duplicates
before = len(df3)
df3.drop_duplicates(inplace=True)
print(f"Duplicates removed: {before - len(df3)}")

# Fix numeric columns
df3['Conversion_Rate']  = pd.to_numeric(df3['Conversion_Rate'], errors='coerce')
df3['Acquisition_Cost'] = pd.to_numeric(df3['Acquisition_Cost'], errors='coerce')
df3['ROI']              = pd.to_numeric(df3['ROI'], errors='coerce')
df3['Clicks']           = pd.to_numeric(df3['Clicks'], errors='coerce')
df3['Impressions']      = pd.to_numeric(df3['Impressions'], errors='coerce')

df3.dropna(subset=['ROI', 'Conversion_Rate'], inplace=True)
df3 = df3[df3['Clicks'] <= df3['Impressions']]

# Add time features
df3['Year']       = df3['Date'].dt.year
df3['Month']      = df3['Date'].dt.month
df3['Month_Name'] = df3['Date'].dt.strftime('%B')
df3['Quarter']    = df3['Date'].dt.quarter

print(f"✅ df3 cleaned: {df3.shape}")

# ════════════════════════════════════════════════════════════════
# SAVE CLEANED FILES
# ════════════════════════════════════════════════════════════════
os.makedirs('data/cleaned', exist_ok=True)

df1.to_csv('data/cleaned/engagement_cleaned.csv', index=False)
df2.to_csv('data/cleaned/advertising_cleaned.csv', index=False)
df3.to_csv('data/cleaned/campaigns_cleaned.csv', index=False)

print("\n✅ ALL 3 DATASETS CLEANED & SAVED!")
print(f"df1 → {df1.shape}")
print(f"df2 → {df2.shape}")
print(f"df3 → {df3.shape}")