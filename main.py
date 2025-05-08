from flask import Flask, render_template, request
from google.cloud import bigquery
import os

app = Flask(__name__)

# Instantiate BigQuery client
client = bigquery.Client()

# Query 1
QUERY_1 = """
SELECT
  FORMAT_DATE('%Y-%m', DATE(o.created_at)) AS order_month,
  u.gender,
  COUNT(DISTINCT o.user_id) AS active_customers,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue
FROM
  `thelook.orders` o
JOIN
  `thelook.order_items` oi ON o.order_id = oi.order_id
JOIN
  `thelook.users` u ON o.user_id = u.id
WHERE
  o.status = 'Complete'
GROUP BY
  order_month, u.gender
ORDER BY
  order_month, total_revenue DESC
"""

# Query 2
QUERY_2 = """
SELECT
  p.category AS product_category,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue,
  ROUND(SUM(p.cost), 2) AS total_cost,
  ROUND(SUM(oi.sale_price) - SUM(p.cost), 2) AS total_profit,
  COUNT(oi.id) AS items_sold
FROM
  `thelook.order_items` oi
JOIN
  `thelook.products` p ON oi.product_id = p.id
WHERE
  oi.status = 'Complete'
GROUP BY
  product_category
ORDER BY
  total_profit DESC
LIMIT 10
"""

@app.route('/')
def index():
    query = request.args.get('query', '')
    results = []

    if query == '1':
        job = client.query(QUERY_1)
        results = [dict(row) for row in job]
    elif query == '2':
        job = client.query(QUERY_2)
        results = [dict(row) for row in job]

    return render_template('index.html', data=results, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
