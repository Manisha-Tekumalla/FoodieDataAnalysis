import pandas as pd
import json
import sqlite3
import re

def load_data():
    # 1. Load Orders (CSV)
    df_orders = pd.read_csv('orders - orders.csv')
    
    # 2. Load Users (JSON)
    with open('users.json', 'r') as f:
        users_data = json.load(f)
    df_users = pd.DataFrame(users_data)
    
    # 3. Load Restaurants (SQL parsing)
    with open('restaurants.sql', 'r') as f:
        sql_content = f.read()
    pattern = r"\((\d+),\s*'([^']*)',\s*'([^']*)',\s*([\d\.]+)\)"
    matches = re.findall(pattern, sql_content)
    df_rest = pd.DataFrame(matches, columns=['restaurant_id', 'restaurant_name', 'cuisine', 'rating'])
    df_rest['restaurant_id'] = df_rest['restaurant_id'].astype(int)
    df_rest['rating'] = df_rest['rating'].astype(float)
    
    return df_orders, df_users, df_rest

def run_analysis():
    df_orders, df_users, df_rest = load_data()
    
    # Merge datasets
    df_final = df_orders.merge(df_users, on='user_id').merge(df_rest, on='restaurant_id')
    
    print("--- HACKATHON INSIGHTS REPORT ---")
    
    # Insight 1: Top Revenue City for Gold Members
    gold_revenue = df_final[df_final['membership'] == 'Gold'].groupby('city')['total_amount'].sum()
    print(f"\n1. Top Gold Member City: {gold_revenue.idxmax()} (${gold_revenue.max():,.2f})")
    
    # Insight 2: Highest AOV Cuisine
    cuisine_aov = df_final.groupby('cuisine')['total_amount'].mean()
    print(f"2. Highest Avg Order Cuisine: {cuisine_aov.idxmax()} (${cuisine_aov.max():.2f})")
    
    # Insight 3: Gold Member Order Share
    gold_count = len(df_final[df_final['membership'] == 'Gold'])
    percent = (gold_count / len(df_final)) * 100
    print(f"3. Gold Member Order Share: {percent:.2f}%")
    
    # Export for visualization
    df_final.to_csv('final_merged_data.csv', index=False)
    print("\n[Success] Processed data saved to 'final_merged_data.csv'")

if __name__ == "__main__":
    run_analysis()