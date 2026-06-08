import orders 
import products
import couriers


#courier_list = couriers.load_couriers()

def print_main_menu():
    print(" ------ Main Menu ------")
    print("|\t\t\t|")
    print("| 1. Products Menu\t|")
    print("| 2. Courier Menu \t|")
    print("| 3. Order Menu \t|")
    print("| 0. Exit\t\t|")
    print("|\t\t\t|")
    print("------------------------")

while True:
    print_main_menu()
    user_input = input("Enter option: ")

    if user_input == "0":
        saveconf = input("Do you want to save your changes y/n: ")
        if saveconf == "y":
            #couriers.save_couriers(courier_list)
            #products.save_products(products_list)
            print("Saving and Exiting app...")
            exit()
            break

        elif saveconf == "n":
            print("Exiting app...")
            exit()
            break
        
        else:  
            print ("Invalid Input")
    
    elif user_input == "1":
        products.product_menu()

    elif user_input== "2":
        couriers.courier_menu()
        
    elif user_input == "3":
        orders.order_menu()
        # print(orders.__file__)
        # print(dir(orders))

    else:
        print("Invalid input ")
