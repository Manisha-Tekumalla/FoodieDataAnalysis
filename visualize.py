import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

def create_all_charts():
    # 1. Load Data
    df_orders = pd.read_csv('orders - orders.csv')
    with open('users.json', 'r') as f:
        users_data = json.load(f)
    df_users = pd.DataFrame(users_data)

    # 2. Merge Data
    df_merged = pd.merge(df_orders, df_users, on='user_id')
    sns.set_theme(style="whitegrid")

    # --- CHART 1: TOTAL REVENUE (Shows Bangalore is #1) ---
    plt.figure(figsize=(10, 6))
    total_rev = df_merged.groupby('city')['total_amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=total_rev, x='city', y='total_amount', hue='city', palette='viridis', legend=False)
    plt.title('Total Revenue by City (Overall)', fontsize=15, fontweight='bold')
    plt.ylabel('Revenue ($)')
    plt.savefig('total_revenue.png')
    plt.close()

    # --- CHART 2: GOLD VS REGULAR (Shows Chennai leads Gold) ---
    plt.figure(figsize=(10, 6))
    member_rev = df_merged.groupby(['city', 'membership'])['total_amount'].sum().reset_index()
    sns.barplot(data=member_rev, x='city', y='total_amount', hue='membership', palette='magma')
    plt.title('Gold vs Regular Membership Revenue', fontsize=15, fontweight='bold')
    plt.ylabel('Revenue ($)')
    plt.savefig('membership_breakdown.png')
    plt.close()

    print("Success! Both 'total_revenue.png' and 'membership_breakdown.png' are ready.")

if __name__ == "__main__":
    create_all_charts()