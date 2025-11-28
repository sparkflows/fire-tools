# make_customers_parquet.py
import pandas as pd
from datetime import datetime, timedelta

data = []
base_time = datetime(2024, 1, 1, 12, 0, 0)
countries = ["US", "CA", "UK", "IN", "DE"]

for i in range(1, 11):
    data.append({
        "customer_id": i,
        "first_name": f"First{i}",
        "last_name": f"Last{i}",
        "email": f"customer{i}@example.com",
        "created_at": base_time + timedelta(days=i),
        "country": countries[i % len(countries)],
    })

df = pd.DataFrame(data)

# adjust this path to wherever your MCP server can see it
output_path = "/Users/dhruv/Documents/Dev/sparkflows/mcp/fire-tools/sparkflows-mcp-server/data/customers.parquet"
df.to_parquet(output_path, index=False)

print(f"Written {output_path}")
print(df.head())
