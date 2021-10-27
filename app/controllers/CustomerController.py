from config.database import database


class CustomerController:
    _database = database()

    def __init__(self):
        self._database = database()

    @classmethod
    def register(self, name: str, email: str, mobile: str, active: int):
        try:
            if self._database is not False:
                with self._database.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO customers(name, email, mobile, active) VALUES (%s, %s, %s, %s)",
                        (name, email, mobile, active),
                    )

                self._database.commit()
                cursor.close()
                return True
            else:
                return False
        except:
            return False

    @classmethod
    def update(self, id: int, name: str, email: str, mobile: str, active: int):
        try:
            with self._database.cursor() as cursor:
                cursor.execute(
                    "UPDATE customers SET name = %s, email = %s, mobile = %s, active = %s WHERE id = %s",
                    (name, email, mobile, active, id),
                )
            self._database.commit()
            return True
        except:
            return False

    @classmethod
    def delete(self, id: int):
        try:
            customer = self.get_customer_by_id(id)
            if customer is not False:
                if not self.__has_invoices(id):
                    with self._database.cursor() as cursor:
                        cursor.execute("DELETE FROM customers WHERE id = %s", (id))
                        self._database.commit()
                        print(cursor.rowcount, "record(s) deleted")
                        cursor.close()
                    return True
                else:
                    print("Tiene facturas. No se puede eliminar.")
                    return False
            else:
                print("No existe el cliente especificado.")
                return False
        except Exception as error:
            print("Error al eliminar el usuario.")
            print(error)

    @classmethod
    def all_customers(self):
        try:
            with self._database.cursor() as cursor:
                cursor.execute("SELECT id, name, email, mobile, active FROM customers")
                customers_aux = cursor.fetchall()
                cursor.close()
            customers = []

            for customer in customers_aux:
                customers.append(
                    {
                        "id": customer[0],
                        "name": customer[1],
                        "email": customer[2],
                        "mobile": customer[3],
                        "active": customer[4],
                        "has_invoices": self.__has_invoices(customer[0]),
                    }
                )

            return customers
        except:
            return False

    @classmethod
    def get_customer_by_id(self, id: int):
        with self._database.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email, mobile, active FROM customers WHERE id = %s",
                (id),
            )
            customer = cursor.fetchone()
            cursor.close()

        return (
            False
            if customer[0] <= 0
            else {
                "id": customer[0],
                "name": customer[1],
                "email": customer[2],
                "mobile": customer[3],
                "active": customer[4],
            }
        )

    @classmethod
    def get_customer_invoices_by_id(self, id: int):
        with self._database.cursor() as cursor:
            cursor.execute(
                "SELECT invoices.id, invoices.date, invoices.price, invoices.balance FROM customers RIGHT JOIN invoices ON customers.id = invoices.customer_id WHERE customers.id = %s",
                (id),
            )
            customer_invoices_aux = cursor.fetchall()
            cursor.close()
            customer_invoices = []

        for customer_invoice in customer_invoices_aux:
            customer_invoices.append(
                {
                    "invoice_id": customer_invoice[0],
                    "date": customer_invoice[1],
                    "price": customer_invoice[2],
                    "balance": customer_invoice[3],
                }
            )

        return customer_invoices

    @classmethod
    def __has_invoices(self, id: int):
        with self._database.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(invoices.id) AS customer_invoices FROM customers RIGHT JOIN invoices ON customers.id = invoices.customer_id WHERE customers.id = %s",
                (id),
            )
            has_invoices = cursor.fetchone()
            cursor.close()

        return True if has_invoices[0] > 0 else False
