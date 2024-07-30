import random
from datetime import datetime
transaction_history = []
invent = {}

def add_product():
    n=input("enter the product name: ").lower()
    existing=None
    for pid,details in invent.items():
        if details['name'].lower()==n:
            existing=pid
            break
    if existing:
        print(f"Product with the name '{n}' already exists. Please choose a different name.")
    else:
        pid='P'+str(random.randint(1000, 9999))
        q=int(input("enter product quantity: "))
        bp=float(input("enter the buying price: "))
        per=int(input("enter the selling percentage: "))
        sp=bp+((per/100)*bp)
        invent[pid]={'name':n,'quantity':q,'buying_price':bp,'selling_price':sp}
        print(f"PRODUCT ADDED SUCCESSFULLY : {pid}")

def dsply():
    if len(invent)==0:
        print("~LIST IS EMPTY~")
    else:
        print("\t\t\t****PRODUCT INVENTORY**** ")
        header="{:<13}{:<20}{:<10}{:<15}{:<15}".format("PRODUCT ID","PRODUCT NAME","QUANTITY","BUYING PRICE","SELLING PRICE")
        print(header)
        for pid,details in invent.items():
            p_info="{:<13}{:<20}{:<10}{:<15.2f}{:<15.2f}".format(pid,details['name'],details['quantity'],details['buying_price'],details['selling_price'])
            print(p_info)
def update(product_id,new_quantity):
    if product_id in invent:
        invent[product_id]['quantity']=new_quantity
        print(f"Quantity for {invent[product_id]['name']} updated to {new_quantity}")
    else:
        print("PRODUCT NOT FOUND !!")

def update_product(product_id):
    if product_id in invent:
        per=int(input("enter new percentage of sp : "))
        invent[product_id]['selling_price']=invent[product_id]['buying_price']+((per/100)*invent[product_id]['buying_price'])
        print(f"Selling price for {invent[product_id]['name']} updated to {invent[product_id]['selling_price']}")
    else:
        print("PRODUCT NOT FOUND !!")


def buy_product():
    product_id=input("Enter product ID to buy: ")
    if product_id in invent:
        quantity_bought=int(input("Enter quantity bought: "))
        new_quantity=invent[product_id]['quantity']+quantity_bought
        invent[product_id]['quantity']=new_quantity
        print(f"Bought {quantity_bought} units of {invent[product_id]['name']}. New quantity: {new_quantity}")
        update(product_id,new_quantity)
        transaction_details = (product_id,invent[product_id]['name'],'buy',quantity_bought,None,datetime.now().strftime("%Y-%m-%d"))
        transaction_history.append(transaction_details)
    else:
        print("PRODUCT NOT FOUND !!")


def sell_product():
    i=input("Enter product ID or name to sell: ")
    product_id = None
    if i in invent:
        product_id=i
    else:
        for pid,details in invent.items():
            if details['name'].lower()==i.lower():
                product_id = pid
                break

    if product_id is not None:
        if invent[product_id]['quantity']==0:
            print("~OUT OF STOCK !!!!")
        else:
            quantity_sold=int(input("Enter quantity sold: "))
            if quantity_sold<=invent[product_id]['quantity']:
                invent[product_id]['quantity']-=quantity_sold
                total_revenue=quantity_sold*invent[product_id]['selling_price']
                gross_rev=quantity_sold*invent[product_id]['buying_price']
                prof=total_revenue-gross_rev
                print(f"Sold {quantity_sold} units of {invent[product_id]['name']} for Rs:{total_revenue:.2f}")
                print(f'Profit={prof}')
                update(product_id, invent[product_id]['quantity'])
                transaction_details=(product_id,invent[product_id]['name'],'sell',quantity_sold,prof,datetime.now().strftime("%Y-%m-%d"))
                transaction_history.append(transaction_details)
                if invent[product_id]['quantity'] <= 10:
                    Restock_alert(product_id)
            else:
                print("INSUFFICIENT STOCK FOR SALE !!")
    else:
        print("PRODUCCT NOT FOUND ")

def Restock_alert(product_id):
    if product_id in invent:
        threshold=10
        current_quantity=invent[product_id]['quantity']
        if current_quantity<=threshold:
            print(f"ALERT : Stock for {invent[product_id]['name']} is below the threshold ({threshold}). PLEASE RESTOCK!!!!")
    else:
        print("PRODUCT NOT FOUND !!!")

def delete(product_id):
    if product_id in invent:
        del invent[product_id]
        print("PROODUCT DELETED !!!!")
    else:
        print("PRODUCT NOT FOUND !!!!")


def Generate_sale_report(month):
    if len(transaction_history)==0:
        print("  NO HISTORY... ")
    else:
        print(f"\n\t\t\t****SALES REPORT FOR THE MONTH {month}:****")
        print("------------------------------------------------------------------------------------------------------")
        print("{:<13}{:<20}{:<20}{:<10}{:<15}{:<15}".format("PRODUCT ID","PRODUCT NAME","TYPE","QUANTITY","PROFIT","DATE"))
        print("------------------------------------------------------------------------------------------------------")
        for transaction_details in transaction_history:
            p_id=transaction_details[0]
            p_name=transaction_details[1]
            t_type=transaction_details[2]
            quantity=transaction_details[3]
            profit=transaction_details[4]
            t_date=transaction_details[5]
            date=datetime.strptime(t_date,"%Y-%m-%d").strftime("%d-%m-%Y")
            t_month=datetime.strptime(t_date,"%Y-%m-%d").strftime("%m")
            if t_month==month:
                if t_type=='buy':
                    pf='N/A' if profit is None else f"{profit:.2f}"
                    print("{:<13}{:<20}{:<20}{:<10}{:<15}{:<15}".format(p_id,p_name,t_type,quantity,pf,date))
                elif t_type=='sell':
                    print("{:<13}{:<20}{:<20}{:<10}{:<15}{:<15}".format(p_id,p_name,t_type,quantity,profit,date))
            else:
                print(" NO HISTORY ...")
                break

while True:
    print("1.Add product\n2.Sell product\n3.Buy product\n4.Update product\n5.Display\n6.Delete product\n7.sales report\n8.exit ")
    ch=int(input("enter your choice : "))
    if ch==1:
        add_product()
    elif ch==2:
        sell_product()
    elif ch==3:
        buy_product()
    elif ch==4:
        pid=input("enter the product id : ")
        update_product(pid)
    elif ch==5:
        dsply()
    elif ch==6:
        pid=input("enter product id you want to delete : ")
        delete(pid)
    elif ch==7:
        month=input("Enter the month (MM): ")
        Generate_sale_report(month)
    elif ch==8:
        print("EXITING .....")
        break
