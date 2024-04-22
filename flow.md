# Bot1
1. Once per alternating hour of Bot2, get rows from excel where "Bot Status" column == "Ready to Update"
    Either with an OData query or a loop in power automate
2. Add the value from that row's "Order #" column into a list
3. Do this for all rows
4. Loop through list
5. create a new entry into the db with order_number == column "Order #" and status == "created"

# Bot2
1. Once per alternating hour of Bot1, access db to get all entries where status == "created"
2. Extract the order_numbers and send it into webscraper
6. If it finds the order in Pro and updates it
7. Query the db by the order number to get the item id
8. Update the item so the status say "updated"
8. If it doesn't find it and can't update it, update the entry in the db with a status of "Error: Cannot find order in Pro"

# Bot3
1. Once per alternating hour of Bot1 and Bot2, Get rows from excel where "Bot Status" column == "Ready to Update"
    Either with an OData query or a loop in power automate
2. Add the value from that row's "Order #" column into a list
3. Do this for all rows
10. Loop through the list
11. Query the db where the "Owner #" column == order_number
11. If that entry exists and the status == "Updated"
12. Update the "Updated Status in Pro" column with the timestamp & update the "Bot Status" to "Updated" 
12. Else, update the "Updated Status in Pro" column with "No" and update the "Bot Status" to the status from the return list 


