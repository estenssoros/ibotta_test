Ibotta Marketing Analyst Exercise

As you will have figured from the app, ibotta gathers a large amount of information about user attributes and behavior, including: demographics, geolocation, all in-app behavior (sessions, views, unlocks and verifications), and receipt capture and processing at the product level.

Part 1
The attached document titled “SQL_Data_v2” contains sample data from Ibotta’s internal database.  Each tab represents one table.  Using the tables provided, please write the SQL code necessary to pull the following information from the database (provide 1 query per question).

1.	A total count of receipt item ids (ID of the table) grouped by receipt id using the receipt items table.
2.	For each customer, select the most recent receipt date and the total receipt amount (if applicable) for that receipt.
3.	Select the top 100 customers with more than 10 receipts, assuming the table had our entire database of customers.
4.	For each retailer id, count the number of unique products purchased and the number of unique customers.
5.	For customer id 4162, list customer id, receipt id, and receipt date sorted by total (highest to lowest).  Also, please include a column that shows the rank of the receipt.

Part 2
In the separate csv file you will find sample data describing how customers behave in their first fourteen days. Each day’s activity is labeled based on the user behavior on that day, in order of decreasing importance:

Verify (funded/self-funded) – Completed a deal and received the cash
Engage (funded/self-funded) – Unlocked a deal
Session (and time in seconds) – Went onto the app, but did not unlock any deals
Gap – No app activity

The number of future redemptions is also provided.

a)	Build a predictive model in the tool of your choice, and explain what the key indicators of future redemption behaviors are. How accurate is your model? What other methods might you have used to improve accuracy?
b)	Describe how this data could be used to drive marketing communications during a customer’s first two weeks of activity.
