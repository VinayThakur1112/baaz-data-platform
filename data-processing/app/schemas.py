SCHEMAS = {
    "customers": [
        "customerID", "companyName", "contactName",
        "contactTitle", "city", "country"
    ],
    "employees": [
        "employeeID", "employeeName", "title",
        "city", "country", "reportsTo"
    ],
    "orders": [
        "orderID", "customerID", "employeeID",
        "orderDate", "requiredDate", "shippedDate",
        "shipperID", "freight"
    ],
    "order_details": [
        "orderID", "productID", "unitPrice",
        "quantity", "discount"
    ],
    "products": [
        "productID", "productName", "quantityPerUnit",
        "unitPrice", "discontinued", "categoryID"
    ],
    "categories": [
        "categoryID", "categoryName", "description"
    ],
    "shippers": [
        "shipperID", "companyName"
    ]
}