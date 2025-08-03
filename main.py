# streamlit run main.py
import psycopg2
import psycopg2.extras
import streamlit as st

def connect_to_postgresql():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='215069121',
            host='localhost',
            port='5432',
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        print("Connected successfully.")
        return conn
    except psycopg2.Error as e:
        print("Connection error:", e)
        return None

def create_table():
    conn = connect_to_postgresql()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS products(
                product_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price NUMERIC(6, 2) NOT NULL,
                in_stock BOOLEAN DEFAULT TRUE
            );
            """)
            conn.commit()
            print("Table created.")
        except psycopg2.Error as e:
            print("Error creating table:", e)
        finally:
            cur.close()
            conn.close()




def insert_data():
    conn = connect_to_postgresql()
    if conn:
        try:
            cur = conn.cursor()
            cur.executemany(
                "INSERT INTO products (name, price, in_stock) VALUES (%s, %s, %s)",
                [
                            ('Laptop', 3200.50, True),
                            ('Mouse', 99.99, True),
                            ('Keyboard', 250.00, False),
                            ('Monitor', 1190.95, False)
                        ]
                        )
            conn.commit()
            print("Data inserted")
        except psycopg2.Error as e:
            print("Insert error:", e)
        finally:
            cur.close()
            conn.close()





def select_data(query):
    rows = []
    conn = connect_to_postgresql()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()

        except psycopg2.Error as e:
            print(f"Select error: {e}")
        finally:
            cur.close()
            conn.close()
    return rows


st.title("👤 Noa Rozen")
number_1 = st.number_input("Enter first number:")
number_2 = st.number_input("Enter second number:")
if st.button("Add"):
    result = number_1 + number_2
    st.success(f"The result is: {result}")
st.subheader("📦 Available Products")
if st.button("Show Products"):
    products = select_data("SELECT * FROM products WHERE in_stock = True")
    if products:
        for product in products:
            st.write(product)
    else:
        st.info("No products in stock.")

