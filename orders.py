import csv
from select import select
from unicodedata import digit
from couriers import load_couriers
import os
from dotenv import load_dotenv
import csv
import psycopg2
from products import retrieve_products, update_product_price
from couriers import print_courier_list
from db import get_connection


FIELDNAMES = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']

def print_order_menu():
    print('\n ---------- Order Menu ---------')
    print('|\t\t\t\t|')
    print('| 1. Print Order Table\t|')
    print('| 2. Add Order to Table\t|')
    print("| 3. Update an Order's Status\t|")
    print("| 4. Update an Order's Details\t|")
    print('| 5. Delete an Order\t\t|')
    print('| 0. Exit to Main Menu\t\t|')
    print('| \t\t\t\t|')
    print('--------------------------------')



def print_status():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT * FROM status
                """)
                statuses = cur.fetchall()
                for status in statuses:
                    print(status)
                return statuses
    except Exception as e:
        print(f'Error: {e}')
        return []



def print_orders():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM orders
                    ORDER BY order_id ASC        
                """)

                orders = cur.fetchall()
                if orders:
                    for order in orders:
                        print(order)
                else:
                    print('No orders')
                return orders
    except Exception as e:
        print(f'Error: {e}')
        return []

print_orders()

 # Updates the status of an order based off of ID

def update_order_status(select_id, upd_status):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE orders
                    SET status_id = %s
                    WHERE order_id = %s
                """, (upd_status, select_id))
                conn.commit()
                print(f'Order {select_id} updated to status {upd_status}')
                return True
    except Exception as e:
        print(f'Error updating order status: {e}')
        return False

def add_order():
    while True:
        try:
            new_customer_name = input('What is the new customer\'s name? ')
            new_customer_address = input('What is the address of the customer? ')
            new_customer_phone = int(input('What is the phone number of the customer? '))
            retrieve_products()
            #NEEDS TO BE CHANGED TO WORK WITH STRINGS
            new_order_product = (input("Please select your products using the ID comma seperated: "))
            print_courier_list()
            new_order_courier =  int(input("Please choose your courier using the ID "))
            insert_order(new_customer_name, new_customer_address, new_customer_phone, new_order_product, new_order_courier)
            break
        except: 
            print("Invalid Input")
            cursor.close()
            break

def load_orders():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM orders
                    ORDER BY order_id ASC
                """)
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return [dict(zip(columns, row)) for row in rows]
    except Exception as error:
        print(f'Unable to load orders: {error}')
        return []


def save_orders(orders=None):
    if orders is None:
        orders = load_orders()
    if not orders:
        print('No orders to save.')
        return
    try:
        with open('Orders.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=orders[0].keys())
            writer.writeheader()
            for order in orders:
                writer.writerow({key: order.get(key, '') for key in orders[0].keys()})
        print('Orders saved to Orders.csv')
    except Exception as error:
        print(f'Unable to save orders: {error}')


def delete_order():
    print_orders()
    delete_id = input("Enter the id of the order to delete: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = """DELETE FROM orders
                WHERE order_id = %s"""
            
                cur.execute(sql, (delete_id,))
                print("Order deleted")

    except Exception as e:
        print(f"Error: {e}")



# change
def order_menu():
    while True:
        print_order_menu()
        choice = input('Please select an option: ')
        if choice == '0':
            save_orders()
            break
        elif choice == '1':
             print_orders()
        elif choice == '2':
            add_order()
        elif choice == '3':
            while True:
                try:
                    orders = print_orders()
                    if not orders:
                        break

                    select_id = input("Please select an id to update: ").strip()
                    if not select_id.isdigit():
                        print("Please enter a valid id")
                        break
                    select_id = int(select_id)
                    if select_id <= 0 or not any(order[0] == select_id for order in orders):
                        print("Invalid order id")
                        break

                    print(f"Order selected: {select_id}")
                    statuses = print_status()
                    if not statuses:
                        break

                    upd_status = input("Please select a new status id: ").strip()
                    if not upd_status.isdigit():
                        print("Invalid Input")
                        break
                    upd_status = int(upd_status)
                    if upd_status <= 0 or not any(status[0] == upd_status for status in statuses):
                        print("Invalid status id")
                        break

                    update_order_status(select_id, upd_status)
                    break
                except Exception as e:
                    print(f"Invalid Input: {e}")
                    break
        # elif choice == '4':
        #     update_order_details(order_list, couriers, products)
        elif choice == '5':
            delete_order()
        else:
            print('Invalid input')


load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")
conn_string = f'host={host_name} dbname={database_name} user={user_name} password={user_password}'

try:
    with psycopg2.connect(conn_string) as connection:

        # print('Opening cursor...')
        cursor = connection.cursor()
except:
    print("WARNING - Failed to connect to database ")

def insert_order(new_customer_name, new_customer_address, new_customer_phone, new_order_product, new_order_courier):
    cursor = connection.cursor()
    insert = '''
    INSERT INTO orders (customer_name, customer_address, customer_phone, courier_id, status_id, products_id)
    VALUES (%s,%s,%s,%s,1,%s)
    '''

    cursor.execute(insert, (new_customer_name, new_customer_address, new_customer_phone, new_order_courier,new_order_product))
    connection.commit()

    cursor.close()