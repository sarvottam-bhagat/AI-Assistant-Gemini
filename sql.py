import sqlite3

# Connect to SQlite
connection = sqlite3.connect("student.db")

# Create a cursor object to insert record, create table
cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE GHEE_PRODUCTS (
    PRODUCT_NAME VARCHAR(50),
    SALES_COUNT INT,
    PRICE DECIMAL(10, 2),
    CATEGORY VARCHAR(50)
);
"""
cursor.execute(table_info)

# Insert Some records
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Organic Cow Ghee', '500', '25.99', 'Organic')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Pure Buffalo Ghee', '300', '30.99', 'Buffalo')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Desi Cow Ghee', '700', '27.99', 'Desi')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('A2 Cow Ghee', '450', '35.99', 'A2')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Herbal Infused Ghee', '200', '45.99', 'Herbal')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Gir Cow Ghee', '600', '40.99', 'Gir')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Nutritional Ghee', '350', '29.99', 'Nutritional')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Ayurvedic Ghee', '400', '50.99', 'Ayurvedic')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Traditional Ghee', '550', '22.99', 'Traditional')''')
cursor.execute('''INSERT INTO GHEE_PRODUCTS VALUES('Cultured Ghee', '250', '38.99', 'Cultured')''')


# Display All the records
print("The inserted records are")
data = cursor.execute('''SELECT * FROM GHEE_PRODUCTS''')
for row in data:
    print(row)

# Commit your changes in the database
connection.commit()
connection.close()

#What is the average price of all ghee products?
#List all ghee products in the 'Organic' category.
#Which ghee products have a sales count greater than 400?
#What is the total sales count for all ghee products?
#Show me the details of the ghee product with the highest price.
#List all ghee products sorted by their sales count in descending order.
#How many different categories of ghee products are available?
#Show all ghee products that belong to the 'Ayurvedic' or 'Herbal' category.
#What is the name of the least expensive ghee product?
#Show the total number of ghee products available.