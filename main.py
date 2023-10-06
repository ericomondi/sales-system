from flask import Flask, render_template, request, redirect, url_for
from flask import  flash
from dbservice import get_data, insert_product, insert_sale, remaining_stock
# import pygal


app = Flask(__name__)   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.context_processor
def stock_quantity_processor():
    def check_stock_quantity(product_id, quantity):
        products = get_data("products")
        for product in products:
            if product[0] == product_id:
                if product[4] >= quantity:  # Check if stock quantity is sufficient
                    return True
                else:
                    return False
        return False  # Product not found
    return dict(check_stock_quantity=check_stock_quantity)

# index route
@app.route("/")
def index():
    return render_template("landing.html")

# get products
@app.route("/products",methods=["GET"])
def products():    
    records = get_data("products")
    return render_template("products.html", products=records )

# add product
@app.route("/add-product",methods=["POST"])
def add_product():
    product_name = request.form["product_name"]
    buying_price = float(request.form["buying_price"])
    selling_price = float(request.form["selling_price"])
    stock_quantity = int(request.form["stock_quantity"])
    values = (product_name,buying_price,selling_price,stock_quantity)
    # Insert the product into the database
    insert_product(values)
    flash("Product succesfully added!")
    return redirect(url_for("products"))
    
# get sales
@app.route("/sales", methods=["GET"])
def sales():
    prods = get_data("products")
    records = get_data("sales")
    return render_template("sales.html", sales= records,products = prods)

# add sale
@app.route("/add-sale", methods=["POST"])
def add_sale():
    # Retrieve form data
    product_id = int(request.form["product_id"])
    quantity = float(request.form["quantity"])
    values = (product_id,quantity,"now()")

    
    # Insert the sale into the database
    insert_sale(values)
    flash("Sale added succefully!")
    return redirect(url_for("sales"))

# dashboard
@app.route("/dashboard")
def dashboard():
    # sales per day
    data = get_data("sales_per_day")
    dates = [date for date, profit in data]
    profits = [profit for date, profit in data]


    # top five sales
    top_sales = get_data("top_five_sales")
    p_names = [name[0] for name in top_sales]
    p_sales = [sale[1] for sale in top_sales]

    return render_template("dashboard.html", dates=dates,profits=profits,p_names=p_names,p_sales=p_sales)

    

@app.route("/remaining-stock")
def rem_stock():
    records = remaining_stock()
    return render_template("stock.html", stocks=records)




if __name__ == '__main__':
    app.run(debug=True)

