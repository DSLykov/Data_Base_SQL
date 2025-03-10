import psycopg2
from psycopg2 import sql


# Подключение к базе данных
def create_connection(
    db_name, db_user, db_password, db_host="localhost", db_port="5432"
):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None


# Функция для создания структуры БД
def create_tables(conn):
    with conn.cursor() as cur:
        # Создание таблицы clients
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """
        )
        # Создание таблицы phones
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS phones (
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
                phone VARCHAR(20) UNIQUE
            );
        """
        )
        conn.commit()
        print("Таблицы созданы успешно.")


# Функция для добавления нового клиента
def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING client_id;
        """,
            (first_name, last_name, email),
        )
        client_id = cur.fetchone()[0]
        conn.commit()
        print(f"Клиент {first_name} {last_name} добавлен с ID {client_id}.")
        return client_id


# Функция для добавления телефона для существующего клиента
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO phones (client_id, phone)
            VALUES (%s, %s);
        """,
            (client_id, phone),
        )
        conn.commit()
        print(f"Телефон {phone} добавлен для клиента с ID {client_id}.")


# Функция для изменения данных о клиенте
def update_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute(
                """
                UPDATE clients
                SET first_name = %s
                WHERE client_id = %s;
            """,
                (first_name, client_id),
            )
        if last_name:
            cur.execute(
                """
                UPDATE clients
                SET last_name = %s
                WHERE client_id = %s;
            """,
                (last_name, client_id),
            )
        if email:
            cur.execute(
                """
                UPDATE clients
                SET email = %s
                WHERE client_id = %s;
            """,
                (email, client_id),
            )
        conn.commit()
        print(f"Данные клиента с ID {client_id} обновлены.")


# Функция для удаления телефона для существующего клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM phones
            WHERE client_id = %s AND phone = %s;
        """,
            (client_id, phone),
        )
        conn.commit()
        print(f"Телефон {phone} удален для клиента с ID {client_id}.")


# Функция для удаления существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM clients
            WHERE client_id = %s;
        """,
            (client_id,),
        )
        conn.commit()
        print(f"Клиент с ID {client_id} удален.")


# Функция для поиска клиента по данным
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        query = """
            SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone
            FROM clients c
            LEFT JOIN phones p ON c.client_id = p.client_id
            WHERE 1=1
        """
        params = []
        if first_name:
            query += " AND c.first_name = %s"
            params.append(first_name)
        if last_name:
            query += " AND c.last_name = %s"
            params.append(last_name)
        if email:
            query += " AND c.email = %s"
            params.append(email)
        if phone:
            query += " AND p.phone = %s"
            params.append(phone)
        cur.execute(query, params)
        results = cur.fetchall()
        if results:
            print("Найденные клиенты:")
            for row in results:
                print(
                    f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Email: {row[3]}, Телефон: {row[4]}"
                )
        else:
            print("Клиенты не найдены.")


# Демонстрация работы функций
if __name__ == "__main__":
    # Подключение к базе данных
    conn = create_connection("clients_db", "postgres", "password")
    if conn:
        # Создание таблиц
        create_tables(conn)

        # Добавление клиентов
        client1_id = add_client(conn, "Иван", "Иванов", "ivan@mail.ru")
        client2_id = add_client(conn, "Петр", "Петров", "petr@yandex.ru")

        # Добавление телефонов
        add_phone(conn, client1_id, "79855009987")
        add_phone(conn, client2_id, "79855009989")

        # Поиск клиента
        find_client(conn, first_name="Иван")
        find_client(conn, phone="79855009989")
        find_client(conn, last_name="Петров")
        find_client(conn, email="petr@yandex.ru")

        # Обновление данных клиента
        update_client(conn, client1_id, first_name="Иван", last_name="Сидоров")

        # Удаление телефона
        delete_phone(conn, client1_id, "79855009987")

        # Удаление клиента
        delete_client(conn, client2_id)

        # Закрытие соединения
        conn.close()
