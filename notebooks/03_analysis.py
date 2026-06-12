import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Setup ─────────────────────────────────────────────────────
os.makedirs('visuals', exist_ok=True)
sns.set_theme(style='darkgrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'sans-serif'

COLORS = ['#4361ee','#f72585','#4cc9f0','#7209b7','#06d6a0','#fb8500']

# ── Load Data ─────────────────────────────────────────────────
df1 = pd.read_csv('data/cleaned/engagement_featured.csv')
df2 = pd.read_csv('data/cleaned/advertising_featured.csv')
df3 = pd.read_csv('data/cleaned/campaigns_featured.csv')

print("✅ Data loaded")
print(f"df1: {df1.shape} | df2: {df2.shape} | df3: {df3.shape}")

# ════════════════════════════════════════════════════════════════
# CHART 1 — Engagement Rate by Platform (Bar)
# ════════════════════════════════════════════════════════════════
print("\n📊 Chart 1: Engagement Rate by Platform...")

platform_eng = df1.groupby('Platform')['Engagement_Rate'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(platform_eng['Platform'], platform_eng['Engagement_Rate'],
              color=COLORS[:len(platform_eng)], edgecolor='white', linewidth=0.8)

for bar, val in zip(bars, platform_eng['Engagement_Rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{val:.2f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title('Average Engagement Rate by Platform', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Avg Engagement Rate (%)', fontsize=12)
ax.set_ylim(0, platform_eng['Engagement_Rate'].max() * 1.2)
plt.tight_layout()
plt.savefig('visuals/01_engagement_by_platform.png')
plt.close()
print("   ✅ Saved: visuals/01_engagement_by_platform.png")

# ════════════════════════════════════════════════════════════════
# CHART 2 — Content Type Performance (Horizontal Bar)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 2: Content Type Performance...")

content_perf = df1.groupby('Content_Type').agg(
    Avg_Engagement=('Engagement_Rate','mean'),
    Avg_Virality=('Virality_Score','mean'),
    Total_Posts=('Post_ID','count')
).sort_values('Avg_Engagement', ascending=True).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(content_perf['Content_Type'], content_perf['Avg_Engagement'],
               color=COLORS[:len(content_perf)], edgecolor='white')

for bar, val in zip(bars, content_perf['Avg_Engagement']):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}%', va='center', fontsize=10, fontweight='bold')

ax.set_title('Engagement Rate by Content Type', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Avg Engagement Rate (%)', fontsize=12)
ax.set_ylabel('Content Type', fontsize=12)
plt.tight_layout()
plt.savefig('visuals/02_content_type_performance.png')
plt.close()
print("   ✅ Saved: visuals/02_content_type_performance.png")

# ════════════════════════════════════════════════════════════════
# CHART 3 — Engagement Heatmap: Day vs Hour
# ════════════════════════════════════════════════════════════════
print("📊 Chart 3: Engagement Heatmap Day vs Hour...")

day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
heatmap_data = df1.groupby(['Day_of_Week','Hour_of_Day'])['Engagement_Rate'].mean().unstack()
heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])

fig, ax = plt.subplots(figsize=(16, 6))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, linewidths=0.3,
            cbar_kws={'label': 'Avg Engagement Rate (%)'}, ax=ax)
ax.set_title('Engagement Rate Heatmap — Day of Week vs Hour of Day',
             fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_ylabel('Day of Week', fontsize=12)
plt.tight_layout()
plt.savefig('visuals/03_engagement_heatmap.png')
plt.close()
print("   ✅ Saved: visuals/03_engagement_heatmap.png")

# ════════════════════════════════════════════════════════════════
# CHART 4 — Influencer Tier vs Engagement Rate (Box Plot)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 4: Influencer Tier vs Engagement...")

tier_order = ['Nano','Micro','Mid','Macro','Mega']
tier_order = [t for t in tier_order if t in df1['Influencer_Tier'].unique()]

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df1, x='Influencer_Tier', y='Engagement_Rate',
            order=tier_order, palette=COLORS, ax=ax)
ax.set_title('Engagement Rate by Influencer Tier', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Influencer Tier', fontsize=12)
ax.set_ylabel('Engagement Rate (%)', fontsize=12)
plt.tight_layout()
plt.savefig('visuals/04_influencer_tier_engagement.png')
plt.close()
print("   ✅ Saved: visuals/04_influencer_tier_engagement.png")

# ════════════════════════════════════════════════════════════════
# CHART 5 — Sentiment vs Engagement (Bar)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 5: Sentiment vs Engagement...")

sentiment_eng = df1.groupby('Sentiment')['Engagement_Rate'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(sentiment_eng['Sentiment'], sentiment_eng['Engagement_Rate'],
              color=['#06d6a0','#f72585','#4361ee'][:len(sentiment_eng)],
              edgecolor='white', linewidth=0.8, width=0.5)

for bar, val in zip(bars, sentiment_eng['Engagement_Rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.2f}%', ha='center', fontsize=12, fontweight='bold')

ax.set_title('Engagement Rate by Content Sentiment', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Sentiment', fontsize=12)
ax.set_ylabel('Avg Engagement Rate (%)', fontsize=12)
plt.tight_layout()
plt.savefig('visuals/05_sentiment_engagement.png')
plt.close()
print("   ✅ Saved: visuals/05_sentiment_engagement.png")

# ════════════════════════════════════════════════════════════════
# CHART 6 — ROI by Campaign Goal (df2)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 6: ROI by Campaign Goal...")

goal_roi = df2.groupby('Campaign_Goal')['ROI'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(goal_roi['Campaign_Goal'], goal_roi['ROI'],
              color=COLORS[:len(goal_roi)], edgecolor='white')

for bar, val in zip(bars, goal_roi['ROI']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

ax.set_title('Average ROI by Campaign Goal', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Campaign Goal', fontsize=12)
ax.set_ylabel('Average ROI (%)', fontsize=12)
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('visuals/06_roi_by_campaign_goal.png')
plt.close()
print("   ✅ Saved: visuals/06_roi_by_campaign_goal.png")

# ════════════════════════════════════════════════════════════════
# CHART 7 — ROI by Channel Used (df2)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 7: ROI by Channel...")

channel_roi = df2.groupby('Channel_Used').agg(
    Avg_ROI=('ROI','mean'),
    Avg_CTR=('CTR','mean'),
    Total_Campaigns=('Campaign_ID','count')
).sort_values('Avg_ROI', ascending=True).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(channel_roi['Channel_Used'], channel_roi['Avg_ROI'],
               color=COLORS[:len(channel_roi)], edgecolor='white')

for bar, val in zip(bars, channel_roi['Avg_ROI']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

ax.set_title('Average ROI by Channel Used', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Average ROI (%)', fontsize=12)
ax.set_ylabel('Channel', fontsize=12)
plt.tight_layout()
plt.savefig('visuals/07_roi_by_channel.png')
plt.close()
print("   ✅ Saved: visuals/07_roi_by_channel.png")

# ════════════════════════════════════════════════════════════════
# CHART 8 — Monthly ROI Trend (df2)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 8: Monthly ROI Trend...")

monthly_roi = df2.groupby(['Year','Month'])['ROI'].mean().reset_index()
monthly_roi['Period'] = monthly_roi['Year'].astype(str) + '-' + monthly_roi['Month'].astype(str).str.zfill(2)
monthly_roi = monthly_roi.sort_values(['Year','Month']).tail(24)  # last 24 months

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly_roi['Period'], monthly_roi['ROI'],
        color='#4361ee', linewidth=2.5, marker='o', markersize=5)
ax.fill_between(monthly_roi['Period'], monthly_roi['ROI'],
                alpha=0.15, color='#4361ee')
ax.set_title('Monthly ROI Trend (Last 24 Months)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Avg ROI (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visuals/08_monthly_roi_trend.png')
plt.close()
print("   ✅ Saved: visuals/08_monthly_roi_trend.png")

# ════════════════════════════════════════════════════════════════
# CHART 9 — Campaign Type Performance (df3)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 9: Campaign Type Performance...")

camp_perf = df3.groupby('Campaign_Type').agg(
    Avg_ROI=('ROI','mean'),
    Avg_CVR=('Conversion_Rate','mean'),
    Avg_CTR=('CTR','mean'),
    Avg_Efficiency=('Efficiency_Score','mean')
).round(2).sort_values('Avg_ROI', ascending=False).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
metrics = ['Avg_ROI','Avg_CVR','Avg_CTR']
titles  = ['Avg ROI (%)','Avg Conversion Rate (%)','Avg CTR (%)']

for ax, metric, title in zip(axes, metrics, titles):
    bars = ax.bar(camp_perf['Campaign_Type'], camp_perf[metric],
                  color=COLORS[:len(camp_perf)], edgecolor='white')
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=30)
    for bar, val in zip(bars, camp_perf[metric]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{val:.1f}', ha='center', fontsize=9, fontweight='bold')

fig.suptitle('Campaign Type — ROI, Conversion Rate & CTR',
             fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('visuals/09_campaign_type_performance.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: visuals/09_campaign_type_performance.png")

# ════════════════════════════════════════════════════════════════
# CHART 10 — Top 10 Locations by ROI (df3)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 10: Top 10 Locations by ROI...")

location_roi = df3.groupby('Location')['ROI'].mean().sort_values(ascending=False).head(10).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(location_roi['Location'], location_roi['ROI'],
              color=COLORS * 2, edgecolor='white')

for bar, val in zip(bars, location_roi['ROI']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{val:.1f}%', ha='center', fontsize=9, fontweight='bold')

ax.set_title('Top 10 Locations by Average ROI', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Location', fontsize=12)
ax.set_ylabel('Average ROI (%)', fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('visuals/10_top_locations_roi.png')
plt.close()
print("   ✅ Saved: visuals/10_top_locations_roi.png")

# ════════════════════════════════════════════════════════════════
# CHART 11 — Customer Segment vs Conversion Rate (df3)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 11: Customer Segment vs Conversion Rate...")

segment_cvr = df3.groupby('Customer_Segment')['Conversion_Rate'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(segment_cvr['Customer_Segment'], segment_cvr['Conversion_Rate'],
              color=COLORS * 3, edgecolor='white')

for bar, val in zip(bars, segment_cvr['Conversion_Rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.2f}%', ha='center', fontsize=9, fontweight='bold')

ax.set_title('Conversion Rate by Customer Segment', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Customer Segment', fontsize=12)
ax.set_ylabel('Avg Conversion Rate (%)', fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('visuals/11_segment_conversion_rate.png')
plt.close()
print("   ✅ Saved: visuals/11_segment_conversion_rate.png")

# ════════════════════════════════════════════════════════════════
# CHART 12 — Correlation Heatmap (df2)
# ════════════════════════════════════════════════════════════════
print("📊 Chart 12: Correlation Heatmap...")

corr_cols = ['Conversion_Rate','Acquisition_Cost','ROI','Clicks','Impressions','Engagement_Score','CTR','Cost_Per_Click']
corr_cols = [c for c in corr_cols if c in df2.columns]
corr = df2[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Correlation'})
ax.set_title('Correlation Matrix — Campaign Metrics', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('visuals/12_correlation_heatmap.png')
plt.close()
print("   ✅ Saved: visuals/12_correlation_heatmap.png")

# ════════════════════════════════════════════════════════════════
# PRINT BUSINESS INSIGHTS SUMMARY
# ════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("📌 KEY BUSINESS INSIGHTS")
print("="*60)

print("\n🔹 PLATFORM PERFORMANCE:")
print(platform_eng.to_string(index=False))

print("\n🔹 CAMPAIGN GOAL ROI:")
print(goal_roi.to_string(index=False))

print("\n🔹 CHANNEL ROI RANKING:")
print(channel_roi[['Channel_Used','Avg_ROI','Avg_CTR']].sort_values('Avg_ROI', ascending=False).to_string(index=False))

print("\n🔹 CAMPAIGN TYPE PERFORMANCE:")
print(camp_perf.to_string(index=False))

print("\n🔹 TOP 5 LOCATIONS BY ROI:")
print(location_roi.head(5).to_string(index=False))

print("\n" + "="*60)
print("✅ ALL 12 CHARTS SAVED IN visuals/ FOLDER")
print("="*60)