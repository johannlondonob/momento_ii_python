from os import name
from flask import Flask, render_template, request, url_for, redirect
from controllers.CustomerController import CustomerController as CustomerController
from controllers.InvoiceController import InvoiceController as InvoiceController

app = Flask(__name__)

if __name__ == "__main__":

    # @app.errorhandler(400)
    # def bad_request():
    #     return render_template("layouts/error400.html"), 400

    # @app.errorhandler(404)
    # def not_found():
    #     return render_template("layouts/error404.html"), 404

    # @app.errorhandler(500)
    # def not_server():
    #     return render_template("layouts/error500.html"), 500

    @app.route("/")
    def index():
        __page = {"title": "Inicio"}
        return render_template("index.html", page=__page)

    @app.route("/customer")
    def index_customer():
        __page = {"title": "Clientes"}
        customer = CustomerController()
        __page["customers"] = customer.all_customers()
        return render_template("customer/index.html", page=__page)

    @app.route("/customer/new", methods=["GET", "POST"])
    def store_customer():
        __page = {"title": "Registrar cliente"}
        if request.method == "GET":
            return render_template("customer/register.html", page=__page)
        elif request.method == "POST":
            customer_controller = CustomerController()
            name = request.form.get("name")
            email = request.form.get("email")
            mobile = request.form.get("mobile")
            is_ok = customer_controller.register(
                name=name, email=email, mobile=mobile, active=1
            )
            if is_ok:
                return redirect(url_for("index_customer"))
            else:
                return redirect(url_for("index"))

    @app.route("/update-customer/<int:id>", methods=["GET", "POST"])
    def update_customer(id):
        if request.method == "GET":
            customer_controller = CustomerController()
            __page = {
                "title": "Actualización datos Cliente",
                "customer": customer_controller.get_customer_by_id(id),
            }
            return render_template("customer/update.html", page=__page)
        elif request.method == "POST":
            customer_controller = CustomerController()
            name = request.form.get("name")
            email = request.form.get("email")
            mobile = request.form.get("mobile")
            active = request.form.get("active")
            is_ok = customer_controller.update(
                id=id, name=name, email=email, mobile=mobile, active=active
            )
            if is_ok:
                return redirect(url_for("index_customer"))
            else:
                return redirect(url_for("index"))

    @app.route("/delete-customer/<int:id>", methods=["POST"])
    def delete_customer(id):
        customer = CustomerController()
        is_ok = customer.delete(id)
        if is_ok:
            return redirect(url_for("index_customer"))
        else:
            return redirect(url_for("index"))

    @app.route("/customer/<int:id>/profile")
    def customer_profile(id):
        customer_controller = CustomerController()
        customer_invoices = customer_controller.get_customer_invoices_by_id(id)
        customer = customer_controller.get_customer_by_id(id)
        __page = {
            "title": "Facturas cliente",
            "customer": customer,
            "customer_invoices": customer_invoices,
        }
        return render_template("customer/customer_profile.html", page=__page)

    @app.route("/customer/<int:id>/invoice/new", methods=["GET", "POST"])
    def store_customer_invoice(id):
        customer_controller = CustomerController()
        invoice_controller = InvoiceController()
        customer = customer_controller.get_customer_by_id(id)
        if request.method == "POST":
            if customer is not False and customer.get("active"):
                date = request.form.get("date")
                price = request.form.get("price")
                balance = request.form.get("balance")
                is_ok = invoice_controller.store_invoice(
                    date=date, customer_id=id, price=price, balance=balance
                )
                if is_ok:
                    return redirect(url_for("customer_profile", id=id))
                else:
                    return redirect(url_for("index_customer"))
            else:
                return redirect(url_for("index_customer"))
        elif request.method == "GET":
            __page = {
                "title": "Nueva factura",
                "customer": customer_controller.get_customer_by_id(id),
            }
            return render_template("customer/new-invoice.html", page=__page)

    @app.route("/invoice")
    def index_invoice():
        invoice_controller = InvoiceController()
        __page = {"title": "Facturas", "invoices": invoice_controller.all_invoices()}
        return render_template("invoices/index.html", page=__page)

    @app.route("/invoice/new", methods=["GET", "POST"])
    def store_invoice():
        if request.method == "GET":
            customer_controller = CustomerController()
            __page = {
                "title": "Facturar a un cliente",
                "customers": customer_controller.all_customers(),
            }
            return render_template("invoices/new-invoice.html", page=__page)
        elif request.method == "POST":
            date = request.form.get("date")
            customer_id = request.form.get("customer_id")
            price = request.form.get("price")
            balance = request.form.get("balance")
            invoice_controller = InvoiceController()
            is_ok = invoice_controller.store_invoice(
                date=date, customer_id=customer_id, price=price, balance=balance
            )

            if is_ok:
                return redirect(url_for("index_invoice"))
            else:
                return redirect(url_for("index_customer"))

    @app.route("/invoice/update/<int:id>", methods=["GET", "POST"])
    def update_invoice(id):
        if request.method == "GET":
            invoice_controller = InvoiceController()
            __page = {
                "title": "Facturar a un cliente",
                "invoice": invoice_controller.get_invoice_by_id(id),
            }
            return render_template("invoices/update.html", page=__page)
        elif request.method == "POST":
            date = request.form.get("date")
            # customer_id = request.form.get("customer_id")
            price = request.form.get("price")
            balance = request.form.get("balance")
            invoice_controller = InvoiceController()
            is_ok = invoice_controller.update(
                id=id, date=date, price=price, balance=balance
            )

            if is_ok:
                return redirect(url_for("index_invoice"))
            else:
                return redirect(url_for("index_customer"))

    @app.route("/invoice/delete/<int:id>", methods=["POST"])
    def delete_invoice(id):
        invoice_controller = InvoiceController()
        is_ok = invoice_controller.delete(id)
        if is_ok:
            return redirect(url_for("index_invoice"))
        else:
            return redirect(url_for("index"))

    app.run(port=5400, debug=True)
