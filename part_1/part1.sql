 -- 1.	A total count of receipt item ids (ID of the table) grouped by receipt id using the receipt items table.

SELECT receipt_id,
       count(*) AS cnt
FROM receipt_items
GROUP BY receipt_id
ORDER BY cnt DESC;

 -- 2.	For each customer, select the most recent receipt date and the total receipt amount (if applicable) for that receipt.

SELECT sub.customer_id,
       sub.rec_date,
       rec.total
FROM
    (SELECT customer_id,
            max(created_at) AS rec_date
     FROM receipts
     WHERE total IS NOT NULL
     GROUP BY customer_id) AS sub
JOIN receipts AS rec ON rec.customer_id = sub.customer_id
AND sub.rec_date = rec.created_at;

 -- 3.	Select the top 100 customers with more than 10 receipts, assuming the table had our entire database of customers.

SELECT customer_id,
       COUNT(*) AS COUNT
FROM receipts
GROUP BY customer_id
HAVING COUNT(*) > 10
ORDER BY COUNT DESC LIMIT 100;

 -- 4. For each retailer id, count the number of unique products purchased and the number of unique customers.

SELECT f.retailer_id,
       f.unique_customers,
       j.unique_products
FROM
    (SELECT sub1.retailer_id,
            sum(sub1.customer_count) AS unique_customers
     FROM
         (SELECT retailer_id,
                 COUNT(customer_id) AS customer_count
          FROM receipts
          GROUP BY retailer_id,
                   customer_id) AS sub1
     GROUP BY sub1.retailer_id) AS f
JOIN
    (SELECT rec.retailer_id,
            sum(prod.product_count) AS unique_products
     FROM
         (SELECT receipt_id,
                 count(*) AS product_count
          FROM receipt_items
          GROUP BY receipt_id,
                   product_number) AS prod
     JOIN receipts AS rec ON rec.id = prod.receipt_id
     GROUP BY rec.retailer_id) AS j ON j.retailer_id = f.retailer_id;

 -- 5.	For customer id 4162, list customer id, receipt id, and receipt date sorted by total (highest to lowest).  Also, please include a column that shows the rank of the receipt.

SELECT f.customer_id,
       f.receipt_id,
       f.created_at,
       f.total,
       RANK() OVER (ORDER BY f.total DESC) AS rank
FROM
    (SELECT customer_id,
            id AS receipt_id,
            created_at,
            total
     FROM receipts
     WHERE customer_id = 118) AS f;
