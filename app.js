// Importing necessary modules
const express = require('express');

// Creating an Express app
const app = express();

// Define a route with a GET request
app.get('/api/status', (req, res) => {
    // Set the status code to 200 (OK)
    res.status(200);
    
    // Send a JSON response with a message
    res.json({ status_code: 200 });
});

// Define a route with a GET request for /api/order
app.get('/api/order', (req, res) => {
    // Extracting the order_number parameter from the query string
    const orderNumber = req.query.order_number;
    
    // If order_number is provided, return it as order_id in the response
    if (orderNumber) {
        // Set the status code to 200 (OK)
        res.status(200);
        
        // Send a JSON response with the order_id
        res.json({ order_id: orderNumber.replace("Data", "Order_Number_") });
    } else {
        // If order_number is not provided, return a 400 (Bad Request) status
        res.status(400).json({ error: 'Missing order_number parameter' });
    }
});

// Define a route for handling other routes (404 Not Found)
app.use((req, res, next) => {
    res.status(404).json({ message: 'Route not found' });
});

// Starting the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});