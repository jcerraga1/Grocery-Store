import datetime
from backend.sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
                "(customer_name, total, datetime) "
                "VALUES (%s, %s, %s)")

    order_data = (order['customer_name'], order['grand_total'], datetime.datetime.now())
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price) "
                           "VALUES (%s, %s, %s, %s)")
    order_details_data = []
    for order_details_item in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_details_item['product_id']),
            float(order_details_item['quantity']),
            float(order_details_item['total_price'])
        ])

    cursor.executemany(order_details_query, order_details_data)
    connection.commit()
    return order_id

def get_all_orders(connection):
    cursor = connection.cursor()

    query = ("SELECT datetime, order_id, customer_name, total FROM orders")

    cursor.execute(query)
    response = []

    for (datetime, order_id, customer_name, total) in cursor:
        response.append({
            'datetime': datetime,
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total
        })
    return response

if __name__ == "__main__":
    connection = get_sql_connection()
    print(insert_order(connection, {
        'customer_name': 'Jani',
        'grand_total': 33,
        'datetime': datetime.datetime.now(),
        'order_details':[
        {
            'product_id': 1,
            'quantity': 2,
            'total_price': 6
        },
        {
            'product_id': 9,
            'quantity': 3,
            'total_price': 27
        }]
    }))
    connection.close()