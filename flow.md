# Bot1
1. Once per hour, get rows from excel where "BotStatus" column == "Ready to Update" with an OData query
4. Loop through rows
5. Make an http request to localhost:5000 which is port forwarded through Ngrok
6. This will accept the value from the "Order #" column and find and update that order to "Invoice Sent" in ProABD
7. Then it will update the "BotStatus" column to say "Updated: <date>"
8. If an error occurs or if the order is not found, it will update the "BotStatus" column to say "Error: <date>"
9. If the order is not found, it will update the "BotStatus" column to say "Error: No result found"
10. This will happen for all sheets

# Bot2
1. Once per day, another flow will look for any items that have a "BotStatus" column that says "Updated: <date>"
2. It will compile them into an email to be sent to Jess
