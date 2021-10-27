from datetime import date
from config.database import database


class InvoiceController:
    _database = database()

    def __init__(self):
        self._database = database()

    @classmethod
    def store_invoice(self, date: date, customer_id: int, price: float, balance: float):
        try:
            with self._database.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO invoices(date, customer_id, price, balance) VALUES (%s, %s, %s, %s)",
                    (date, customer_id, price, balance),
                )

            self._database.commit()
            return True
        except:
            return False

    @classmethod
    def update(self, id, date, price, balance):
        try:
            with self._database.cursor() as cursor:
                cursor.execute(
                    "UPDATE invoices SET date = %s, price = %s, balance = %s WHERE id = %s",
                    (date, price, balance, id),
                )
            self._database.commit()
            return True
        except:
            return False

    @classmethod
    def delete(self, id):
        try:
            with self._database.cursor() as cursor:
                cursor.execute("DELETE FROM invoices WHERE id = %s", (id))
                self._database.commit()
                print(cursor.rowcount, "record(s) deleted")
                return True
        except:
            print("Error al eliminar la factura.")
            return False

    @classmethod
    def all_invoices(self):
        with self._database.cursor() as cursor:
            cursor.execute(
                "SELECT invoices.id, invoices.date, customers.id, customers.name, invoices.price, invoices.balance, customers.active FROM invoices LEFT JOIN customers ON invoices.customer_id = customers.id"
            )
            invoices_aux = cursor.fetchall()
        invoices = []

        for invoice in invoices_aux:
            invoices.append(
                {
                    "id": invoice[0],
                    "date": invoice[1],
                    "customer_id": invoice[2],
                    "customer_name": invoice[3],
                    "price": invoice[4],
                    "balance": invoice[5],
                    "customer_active": invoice[6],
                }
            )

        return invoices

    @classmethod
    def get_invoice_by_id(self, id):
        with self._database.cursor() as cursor:
            cursor.execute(
                "SELECT invoices.id, invoices.date, invoices.price, invoices.balance, customers.name, customers.email, customers.mobile, customers.active FROM invoices LEFT JOIN customers ON invoices.customer_id = customers.id WHERE invoices.id = %s",
                (id),
            )
            invoice = cursor.fetchone()

        return {
            "id": invoice[0],
            "date": invoice[1],
            "price": invoice[2],
            "balance": invoice[3],
            "customer_name": invoice[4],
            "customer_email": invoice[5],
            "customer_mobile": invoice[6],
            "customer_active": invoice[7],
        }
