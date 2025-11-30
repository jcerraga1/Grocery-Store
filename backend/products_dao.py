from backend.sql_connection import get_sql_connection

def get_all_products(connection):

    cursor = connection.cursor()

    query = ("SELECT p.product_id, p.name, u.uom_name, p.price_per_unit "
             "FROM products p inner join uom u on p.uom_id = u.uom_id")

    cursor.execute(query)
    response = []

    for (product_id, name, uom_name, price_per_unit) in cursor:
        response.append(
            {"product_id": product_id,
             "name": name,
             "uom_name": uom_name,
             "price_per_unit": price_per_unit
             })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()

    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit) "
             "VALUES (%s, %s, %s)")

    data = (product["product_name"], product["uom_id"], product["price_per_unit"])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products "
             "WHERE product_id =" + str(product_id))

    cursor.execute(query)
    connection.commit()

def update_product(connection, product_id, new_price):
    cursor = connection.cursor()
    query = ("UPDATE products "
             "SET price_per_unit = %s "
             "WHERE product_id = %s")

    data = (new_price, product_id)
    cursor.execute(query, data)
    connection.commit()
    return cursor.rowcount

if __name__ == '__main__':
    connection = get_sql_connection()
    # insert_new_product(connection,{
    #     "name": "tomatoes",
    #     "uom_id": 2,
    #     "price_per_unit": 2.5
    # })

    # delete_product(connection, 8)

    # update_product(connection, 1, 4)
    # pp(get_all_products(connection))
    connection.close()