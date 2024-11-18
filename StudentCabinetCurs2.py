import sys
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox, QTextEdit, QFileDialog, QApplication, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QInputDialog, QSplitter, QComboBox, QDialogButtonBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt,QByteArray, QBuffer, QIODevice, pyqtSignal
from datetime import datetime

import mysql.connector

class DatabaseHandler:
    def __init__(self):
        # Ваши данные для подключения к базе данных
        self.connection = mysql.connector.connect(
            host="bedrocks.tplinkdns.com",
            database="StudentCabinetCurs",
            user="root",
            password="Amazon321123"
        )
        self.cursor = self.connection.cursor()

    def get_table_list(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            return tables
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def get_records(self, table_name):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def delete_record(self, table, record_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id = {record_id}")
            self.connection.commit()
            print(f"Record with ID {record_id} deleted successfully from table {table}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()
    def get_notifications(self, search_text=None):
        try:
            cursor = self.connection.cursor()
            if search_text:
                query = f"SELECT title FROM notifications WHERE title LIKE '%{search_text}%'"
            else:
                query = "SELECT title FROM notifications"
            cursor.execute(query)
            notifications = cursor.fetchall()
            return notifications
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def get_notification_details(self, notification_title):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT message FROM notifications WHERE title = %s", (notification_title,))
            notification_details = cursor.fetchone()
            if notification_details:
                return notification_details[0]
            else:
                return "Детали оповещения не найдены"
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def search_notifications_by_title(self, title):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM notifications WHERE title LIKE %s", (f'%{title}%',))
            notifications = cursor.fetchall()
            return notifications
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def add_notification(self, title, message):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO notifications (title, message, created_at) VALUES (%s, %s, NOW())", (title, message))
            self.connection.commit()
            print("Notification added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def create_survey(self, title, description):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO surveys (title, description) VALUES (%s, %s)", (title, description))
            self.connection.commit()
            print("Опрос успешно создан.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def create_question(self, answer, question_text):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO questions (question_text, answer) VALUES (%s, %s)", (question_text, answer))
            self.connection.commit()
            print("Вопрос успешно создан.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def add_question(self, survey_id, question_text):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO questions (survey_id, question_text) VALUES (%s, %s)", (survey_id, question_text))
            self.connection.commit()
            print("Вопрос успешно добавлен к опросу.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def add_student(self, name, group_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO students (name, group_id) VALUES (%s, %s)", (name, group_id))
            self.connection.commit()
            print("Студент успешно добавлен.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def submit_response(self, survey_id, student_id, question_id, answer):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO responses (survey_id, student_id, question_id, answer) VALUES (%s, %s, %s, %s)",
                           (survey_id, student_id, question_id, answer))
            self.connection.commit()
            print("Ответ успешно отправлен.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def get_surveys(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM surveys")
            surveys = cursor.fetchall()
            return surveys
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def get_questions_for_survey(self, survey_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM questions WHERE survey_id = %s", (survey_id,))
            questions = cursor.fetchall()
            return questions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def get_students_in_group(self, group_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE group_id = %s", (group_id,))
            students = cursor.fetchall()
            return students
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    def get_surveys(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM surveys"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def add_answers(self, question_id, answers_text):
        try:
            cursor = self.connection.cursor()
            answers = answers_text.split(',')
            for answer in answers:
                query = "INSERT INTO answers (question_id, answer_text) VALUES (%s, %s)"
                print(f"Executing query: {query}, question_id: {question_id}, answer_text: {answer.strip()}")
                cursor.execute(query, (question_id, answer.strip()))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error adding answers: {err}")
        finally:
            cursor.close()

    def get_groups(self):
        query = "SELECT * FROM student_groups"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_students_by_group(self, group_id):
        query = "SELECT * FROM students WHERE group_id = %s"
        self.cursor.execute(query, (group_id,))
        return self.cursor.fetchall()

    def get_surveys_by_group(self, group_id):
        query = "SELECT * FROM surveys WHERE group_id = %s"
        self.cursor.execute(query, (group_id,))
        return self.cursor.fetchall()

    def search_groups(self, search_text):
        query = "SELECT * FROM student_groups WHERE name LIKE %s"
        self.cursor.execute(query, ('%' + search_text + '%',))
        return self.cursor.fetchall()

# Используйте этот класс в вашем коде
# db_handler = DatabaseHandler()
# tables = db_handler.get_table_list()
# print(tables)
                
class WelcomWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Личный кабинет студента")
        self.setGeometry(100, 100, 400, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_username = QLabel("Добро пожаловать в личный кабинет:")
        layout.addWidget(self.label_username)

        self.label_password = QLabel("Иформация")
        layout.addWidget(self.label_password)

        self.button_welcome = QPushButton("Авторизация", self)
        self.button_welcome.clicked.connect(self.login)
        layout.addWidget(self.button_welcome)

        self.setLayout(layout)

    def login(self):
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Личный кабинет студента")
        self.setGeometry(100, 100, 400, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_username = QLabel("Логин:")
        self.text_username = QLineEdit(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.text_username)

        self.label_password = QLabel("Пароль:")
        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.text_password)

        self.button_login = QPushButton("Войти", self)
        self.button_login.clicked.connect(self.login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def login(self):
        username = self.text_username.text()
        password = self.text_password.text()

        connection = None  # Инициализация переменной перед блоком try

        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()
            query = "SELECT id, role FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                user_id, role = user
                self.open_main_window(role, user_id)
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def open_main_window(self, role, user_id):
        if role == 1:
            self.admin_window = AdminWindow(self, user_id)
            self.admin_window.show()
        elif role == 2:
            teacher_window = TeacherWindow()
            teacher_window.show()
        elif role == 3:
            student_window = StudentWindow()
            student_window.show()

        self.close()

class AdminWindow(QWidget):
    def __init__(self, login_window, user_id):
        super().__init__()

        self.login_window = login_window
        self.user_id = user_id
        self.profile_window = None
        self.infocreate_window = None
        self.datawindow = None
        self.notification_window = None
        self.survey_window = None

        self.db_handler = DatabaseHandler()

        self.setWindowTitle("Admin")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        # Название окна
        title_label = QLabel("Личный кабинет администратора", self)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Надписи об оповещении и информации
        notification_label = QLabel("Оповещение:", self)
        info_label = QLabel("Информация:", self)

        # Кнопки
        home_button = QPushButton("Главная страница", self)
        tasks_button = QPushButton("Задания", self)
        surveys_button = QPushButton("Опросы", self)
        notifications_button = QPushButton("Оповещения", self)
        logout_button = QPushButton("Выйти", self)
        data_button = QPushButton("Данные", self)
        create_info_button = QPushButton("Создать запись", self)
        profile_button = QPushButton("Профиль", self)

        # Логика кнопок
        logout_button.clicked.connect(self.logout)
        notifications_button.clicked.connect(self.show_notification_window)
        surveys_button.clicked.connect(self.show_survey_window)

        # Создаем QVBoxLayout как основной макет для AdminWindow
        main_layout = QVBoxLayout(self)

        # Создаем QListWidget для отображения записей
        self.info_list_widget = QListWidget()
        main_layout.addWidget(self.info_list_widget)

        self.load_info_from_database()

        # Добавляем заголовок и кнопки в основной макет
        main_layout.addWidget(title_label)
        main_layout.addWidget(notification_label)
        main_layout.addWidget(info_label)
        main_layout.addStretch(1)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(home_button)
        buttons_layout.addWidget(tasks_button)
        buttons_layout.addWidget(surveys_button)
        buttons_layout.addWidget(notifications_button)
        buttons_layout.addWidget(logout_button)
        buttons_layout.addWidget(data_button)
        buttons_layout.addWidget(create_info_button)
        buttons_layout.addWidget(profile_button)

        # Добавляем макет с кнопками в основной макет
        main_layout.addLayout(buttons_layout)

        # Подключаем события кнопок
        profile_button.clicked.connect(self.show_profile_window)
        create_info_button.clicked.connect(self.show_infocreate_window)
        data_button.clicked.connect(self.show_data_window)

    def add_info_to_list(self, info_text):
        # Добавляем новую запись в QListWidget
        item = QListWidgetItem(info_text)
        self.info_list_widget.addItem(item)

    def logout(self):
        # Логика для выхода из учетной записи
        self.close()
        self.login_window.show()

    def show_profile_window(self):
        if not self.profile_window:
            self.profile_window = ProfileWindow(self.user_id)
        self.profile_window.exec_()

    def show_infocreate_window(self):
        if not self.infocreate_window:
            self.infocreate_window = InformationTab(self.user_id)
            self.infocreate_window.info_created.connect(self.add_info_to_list)
        self.infocreate_window.show()

    def show_data_window(self):
        if not self.datawindow:
            self.datawindow = DataWindow()
        self.datawindow.show()

    def show_notification_window(self):
        if not self.notification_window:
            self.notification_window = NotificationsWindow()
        self.notification_window.show()

    def show_survey_window(self):
        if not self.survey_window:
            self.survey_window = SurveysWindow(self.db_handler)
        self.survey_window.show()

    def load_info_from_database(self):
        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Загружаем информацию из базы данных
            select_query = "SELECT info_text FROM information WHERE user_id = %s"
            cursor.execute(select_query, (self.user_id,))

            for (info_text,) in cursor:
                self.add_info_to_list(info_text)

            print("Информация успешно загружена.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class ProfileWindow(QDialog):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle("Профиль")
        self.setGeometry(300, 300, 600, 400)

        self.text_name = QLineEdit(self)
        self.text_surname = QLineEdit(self)
        self.text_email = QLineEdit(self)
        self.text_password = QLineEdit(self)

        self.photo_label = QLabel(self)
        self.load_default_photo()  # Установка изображения по умолчанию

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок "Профиль"
        title_label = QLabel("Профиль", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Ваше фото
        your_photo_label = QLabel("Ваше фото", self)

        # # Область для отображения фото
        self.load_profile_data()  # Загрузка данных профиля при инициализации окна
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(150, 150)

        # Поля для данных
        form_layout = QFormLayout()

        self.label_name = QLabel("Имя:")
        form_layout.addRow(self.label_name, self.text_name)

        self.label_surname = QLabel("Фамилия:")
        form_layout.addRow(self.label_surname, self.text_surname)

        self.label_email = QLabel("Почта:")
        form_layout.addRow(self.label_email, self.text_email)

        self.label_password = QLabel("Пароль:")
        self.text_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow(self.label_password, self.text_password)

        # Кнопка загрузки фото
        self.button_upload_photo = QPushButton("Загрузить фото", self)
        self.button_upload_photo.clicked.connect(self.upload_photo)

        # Кнопка "Сохранить"
        self.button_save = QPushButton("Сохранить", self)
        self.button_save.clicked.connect(self.save_profile)

        # Кнопка "Назад"
        self.button_back = QPushButton("Назад", self)
        self.button_back.clicked.connect(self.close)

        # Размещение элементов в основном макете
        layout.addWidget(title_label)
        layout.addWidget(your_photo_label)
        layout.addWidget(self.photo_label)
        layout.addLayout(form_layout)
        layout.addWidget(self.button_upload_photo)
        layout.addWidget(self.button_save)
        layout.addWidget(self.button_back)

        self.setLayout(layout)
    
    def load_default_photo(self):
        # Загрузка изображения по умолчанию (замените на свой путь)
        default_photo_path = "images/default_photo_profile.png"

        pixmap = QPixmap(default_photo_path)
        self.set_photo(pixmap)

    def set_photo(self, pixmap):
        # Установка изображения в QLabel с сохранением пропорций
        self.photo_label.setPixmap(pixmap.scaled(
            self.photo_label.size(), Qt.KeepAspectRatioByExpanding))
        
    def convert_pixmap_to_blob(self, pixmap):
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")  # Сохраняем в формате PNG, вы можете выбрать другой формат
        return byte_array.data()

    def convert_blob_to_pixmap(self, blob_data):
        # Метод для преобразования данных в формате blob в QPixmap
        byte_array = QByteArray(blob_data)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        return pixmap

    def update_user_photo(self, user_id, photo_data):
        # Метод для обновления фото пользователя в базе данных
        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Обновление данных изображения в базе данных
            update_query = "UPDATE users SET photo=%s WHERE id=%s"
            cursor.execute(update_query, (photo_data, user_id))
            connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def load_profile_data(self):
        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Получение данных профиля из базы данных
            query = "SELECT name, surname, email, password, photo FROM users WHERE id=%s"
            cursor.execute(query, (self.user_id,))
            user_data = cursor.fetchone()

            if user_data:
                name, surname, email, password, photo_data = user_data
                self.text_name.setText(name)
                self.text_surname.setText(surname)
                self.text_email.setText(email)
                self.text_password.setText(password)

                # Отображение фото, если есть данные изображения
                if photo_data:
                    pixmap = self.convert_blob_to_pixmap(photo_data)
                    self.set_photo(pixmap)
                else:
                    # Если данных изображения нет, загрузите фото по умолчанию
                    self.load_default_photo()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def upload_photo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Изображения (*.png *.jpg *.bmp);;Все файлы (*)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            byte_array = self.convert_pixmap_to_blob(pixmap)
            self.update_user_photo(self.user_id, byte_array)
            self.set_photo(pixmap)

    def save_profile(self):
        name = self.text_name.text()
        surname = self.text_surname.text()
        email = self.text_email.text()
        password = self.text_password.text()

        pixmap = self.photo_label.pixmap()
        photo_data = self.convert_pixmap_to_blob(pixmap)

        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Обновление данных профиля в таблице users
            update_query = "UPDATE users SET name=%s, surname=%s, email=%s, password=%s, photo=%s WHERE id=%s"
            cursor.execute(update_query, (name, surname, email, password, photo_data, self.user_id))
            connection.commit()

            QMessageBox.information(self, "Сохранено", "Данные профиля сохранены успешно.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при сохранении данных профиля.")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class InformationTab(QWidget):
    # Добавим сигнал info_created
    info_created = pyqtSignal(str)

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle("Создать запись")
        self.setGeometry(300, 300, 400, 300)

        self.text_info = QTextEdit(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Название окна
        title_label = QLabel("Создать запись", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Текстовое поле "Информация"
        info_label = QLabel("Информация:")
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addWidget(self.text_info)

        # Кнопка "Назад"
        button_back = QPushButton("Назад", self)
        button_back.clicked.connect(self.close)

        # Кнопка "Создать запись"
        button_create = QPushButton("Создать запись", self)
        button_create.clicked.connect(self.create_info_entry)

        layout.addWidget(button_back)
        layout.addWidget(button_create)

        self.setLayout(layout)

    def create_info_entry(self):
        info_text = self.text_info.toPlainText()

        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Вставка новой записи в базу данных
            insert_query = "INSERT INTO information (user_id, info_text) VALUES (%s, %s)"
            cursor.execute(insert_query, (self.user_id, info_text))
            connection.commit()

            # Испускаем сигнал info_created с текстом созданной информации
            self.info_created.emit(info_text)

            QMessageBox.information(self, "Успешно", "Запись успешно создана.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при создании записи.")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class DataWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Данные")
        self.setGeometry(300, 300, 400, 300)
        

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Название окна
        title_label = QLabel("Управление данными", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Кнопки управления данными
        button_view = QPushButton("Просмотр", self)
        button_add = QPushButton("Добавление", self)
        button_delete = QPushButton("Удаление", self)
        button_edit = QPushButton("Редактирование", self)
        button_back = QPushButton("Назад", self)
        button_back.clicked.connect(self.close)

        layout.addWidget(title_label)
        layout.addWidget(button_view)
        layout.addWidget(button_add)
        layout.addWidget(button_delete)
        layout.addWidget(button_edit)
        layout.addWidget(button_back)

        button_add.clicked.connect(self.show_add_record_window)
        button_edit.clicked.connect(self.show_edit_record_window)
        button_view.clicked.connect(self.show_view_record_window)
        button_delete.clicked.connect(self.show_delete_record_window)

        self.setLayout(layout)

    def show_add_record_window(self):
        # Получаем список таблиц из базы данных
        db_handler = DatabaseHandler()
        tables = db_handler.get_table_list()

        # Показываем диалоговое окно для выбора таблицы
        table, ok_pressed = QInputDialog.getItem(
            self,
            "Выбор таблицы",
            "Выберите таблицу для редактирования:",
            tables,
            0,
            False
        )

        # Если пользователь нажал "OK", открываем окно редактирования для выбранной таблицы
        if ok_pressed and table:
            add_record_window = AddRecordWindow(table)
            add_record_window.exec_() 
    
    def show_edit_record_window(self):
    # Получаем список таблиц из базы данных
        db_handler = DatabaseHandler()
        tables = db_handler.get_table_list()

        # Показываем диалоговое окно для выбора таблицы
        table, ok_pressed = QInputDialog.getItem(
            self,
            "Выбор таблицы",
            "Выберите таблицу для редактирования:",
            tables,
            0,
            False
        )

        # Если пользователь нажал "OK", открываем окно редактирования для выбранной таблицы
        if ok_pressed and table:
            edit_window = EditRecordWindow(table, self)
            edit_window.show()

    def show_view_record_window(self):
        db_handler = DatabaseHandler()
        tables = db_handler.get_table_list()
        table, ok_pressed = QInputDialog.getItem(
            self,
            "Выбор таблицы",
            "Выберите таблицу для просмотра данных:",
            tables,
            0,
            False
        )
        if ok_pressed and table:
            view_window = ViewRecordWindow(table, self)  # Открываем окно просмотра данных
            view_window.show()
    
    def show_delete_record_window(self):
        db_handler = DatabaseHandler()
        tables = db_handler.get_table_list()
        table, ok_pressed = QInputDialog.getItem(
            self,
            "Выбор таблицы",
            "Выберите таблицу для удаления данных:",
            tables,
            0,
            False
        )
        if ok_pressed and table:
            delete_window = DeleteRecordWindow(table, self)  # Открываем окно удаления данных
            delete_window.show()

class AddRecordWindow(QDialog):
    def __init__(self, table_name):
        super().__init__()

        self.table_name = table_name

        self.setWindowTitle("Добавить запись")
        self.setGeometry(300, 300, 400, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создаем виджеты для ввода данных
        self.input_widgets = []
        columns = self.get_table_columns()
        for column in columns:
            label = QLabel(f"{column}:")
            line_edit = QLineEdit()
            self.input_widgets.append(line_edit)
            layout.addWidget(label)
            layout.addWidget(line_edit)

        # Кнопка "Добавить запись"
        button_add = QPushButton("Добавить запись")
        button_add.clicked.connect(self.add_record)
        layout.addWidget(button_add)

        self.setLayout(layout)

    def get_table_columns(self):
        # Получаем список столбцов таблицы из базы данных
        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Получаем список столбцов
            cursor.execute(f"DESCRIBE {self.table_name}")
            columns = [column[0] for column in cursor.fetchall()]

            return columns

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_record(self):
        # Добавление новой записи в таблицу
        try:
            connection = mysql.connector.connect(
                host="bedrocks.tplinkdns.com",
                database="StudentCabinetCurs",
                user="root",
                password="Amazon321123"
            )

            cursor = connection.cursor()

            # Формируем строку для вставки
            columns = ", ".join(self.get_table_columns())
            values = ", ".join(f"'{widget.text()}'" for widget in self.input_widgets)
            insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            
            cursor.execute(insert_query)
            connection.commit()

            print("Запись успешно добавлена.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class EditRecordWindow(QDialog):
    def __init__(self, table, parent=None):
        super(EditRecordWindow, self).__init__(parent)
        self.table = table  # Сохраняем имя таблицы
        self.current_record_index = 0  # Индекс текущей записи
        self.setWindowTitle(f"Редактирование записей в таблице {table}")
        self.setGeometry(200, 200, 400, 300)
        self.init_ui()

    def init_ui(self):
        # Заголовок окна
        title_label = QLabel(f"Редактирование записей в таблице {self.table}", self)
        # Создаем QVBoxLayout для элементов интерфейса
        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        # Создаем QFormLayout для отображения атрибутов и их значений
        attribute_layout = QVBoxLayout()
        # Создаем QLineEdit для каждого атрибута и заполняем их значениями
        self.attribute_line_edits = {}
        self.records = self.get_records()
        if not self.records:
            QMessageBox.information(self, "Информация", f"В таблице {self.table} нет записей.")
            self.close()  # Закрываем окно, если нет записей
            return
        record_data = self.get_record_data()
        for attribute, value in record_data.items():
            label = QLabel(attribute.capitalize() + ":", self)
            line_edit = QLineEdit(self)
            line_edit.setText(str(value))  # Устанавливаем начальное значение из базы данных
            attribute_layout.addWidget(label)
            attribute_layout.addWidget(line_edit)
            self.attribute_line_edits[attribute] = line_edit
        # Добавляем QFormLayout в основной макет
        layout.addLayout(attribute_layout)
        # Создаем кнопку "Сохранить"
        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_changes)
        # Добавляем кнопку "Сохранить" в основной макет
        layout.addWidget(save_button)
        # Создаем кнопки "Назад" и "Вперед"
        prev_button = QPushButton("Назад", self)
        next_button = QPushButton("Вперед", self)
        prev_button.clicked.connect(self.show_prev_record)
        next_button.clicked.connect(self.show_next_record)
        # Создаем кнопку "Закрыть"
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)
        # Добавляем кнопки в основной макет
        layout.addWidget(prev_button)
        layout.addWidget(next_button)
        layout.addWidget(close_button)
        # Устанавливаем основной макет для окна
        self.setLayout(layout)

    def get_records(self):
        # Здесь реализуйте логику получения данных из базы данных для выбранной таблицы
        # Примечание: Замените параметры подключения к вашей базе данных и SQL-запросом
        db_handler = DatabaseHandler()
        records = db_handler.get_records(self.table)  # Исправлен вызов метода
        return records

    def get_record_data(self):
        # Получаем данные для текущей записи
        record_data = self.records[self.current_record_index]
        return record_data

    def show_prev_record(self):
        # Логика отображения предыдущей записи
        self.current_record_index -= 1
        if self.current_record_index < 0:
            self.current_record_index = 0  # Минимальный индекс
        self.update_record_data()

    def show_next_record(self):
        # Логика отображения следующей записи
        self.current_record_index += 1
        if self.current_record_index >= len(self.records):
            self.current_record_index = len(self.records) - 1  # Максимальный индекс
        self.update_record_data()

    def update_record_data(self):
        # Обновляем данные для текущей записи
        record_data = self.get_record_data()
        for attribute, value in record_data.items():
            self.attribute_line_edits[attribute].setText(str(value))

    def save_changes(self):
        # Логика сохранения изменений
        new_values = {}
        for attribute, line_edit in self.attribute_line_edits.items():
            new_values[attribute] = line_edit.text()
        # Здесь вы можете использовать new_values для обновления записей в базе данных
        # Примечание: Обязательно проверьте данные на корректность перед сохранением!
        print(f"Сохранение изменений в таблице {self.table}: {new_values}")
        self.accept()  # Закрываем окно после сохранения изменений

class ViewRecordWindow(QDialog):
    def __init__(self, table, parent=None):
        super(ViewRecordWindow, self).__init__(parent)
        self.table = table
        self.current_record_index = 0
        self.setWindowTitle(f"Просмотр данных из таблицы {table}")
        self.setGeometry(200, 200, 400, 300)
        self.attribute_line_edits = {}  # Initialize attribute_line_edits dictionary
        self.init_ui()

    def init_ui(self):
        title_label = QLabel(f"Просмотр данных из таблицы {self.table}", self)
        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        self.attribute_layout = QVBoxLayout()
        layout.addLayout(self.attribute_layout)
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.show_records()

    def show_records(self):
        self.records = self.get_records()
        if self.records:
            self.update_record_data()
            prev_button = QPushButton("Назад", self)
            next_button = QPushButton("Вперед", self)
            prev_button.clicked.connect(self.show_prev_record)
            next_button.clicked.connect(self.show_next_record)
            self.attribute_layout.addWidget(prev_button)
            self.attribute_layout.addWidget(next_button)
        else:
            self.attribute_layout.addWidget(QLabel("Нет данных для отображения"))

    def get_records(self):
        # Здесь реализуйте логику получения данных из базы данных для выбранной таблицы
        db_handler = DatabaseHandler()
        records = db_handler.get_records(self.table)  # Получаем записи из таблицы
        return records

    def show_prev_record(self):
        # Логика отображения предыдущей записи
        self.current_record_index -= 1
        if self.current_record_index < 0:
            self.current_record_index = 0  # Минимальный индекс
        self.update_record_data()

    def show_next_record(self):
        # Логика отображения следующей записи
        self.current_record_index += 1
        if self.current_record_index >= len(self.records):
            self.current_record_index = len(self.records) - 1  # Максимальный индекс
        self.update_record_data()

    def update_record_data(self):
        # Обновляем данные для текущей записи
        record_data = self.records[self.current_record_index]
        for attribute, value in record_data.items():
            line_edit = self.attribute_line_edits.get(attribute)
            if line_edit is None:
                line_edit = QLineEdit(self)
                self.attribute_line_edits[attribute] = line_edit
                self.attribute_layout.addWidget(line_edit)
            line_edit.setText(str(value))

class DeleteRecordWindow(QDialog):
    def __init__(self, table, parent=None):
        super().__init__(parent)  # Исправлен вызов super()
        self.table = table
        self.current_record_index = 0
        self.setWindowTitle(f"Удаление записи из таблицы {table}")  # Изменено название окна
        self.setGeometry(200, 200, 400, 300)
        self.init_ui()

    def init_ui(self):
        title_label = QLabel(f"Удаление записи из таблицы {self.table}", self)
        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        self.attribute_layout = QVBoxLayout()
        layout.addLayout(self.attribute_layout)
        
        # Добавляем кнопки "Назад", "Вперед" и "Удалить"
        prev_button = QPushButton("Назад", self)
        next_button = QPushButton("Вперед", self)
        delete_button = QPushButton("Удалить", self)
        
        prev_button.clicked.connect(self.show_prev_record)
        next_button.clicked.connect(self.show_next_record)
        delete_button.clicked.connect(self.delete_record)
        
        layout.addWidget(prev_button)
        layout.addWidget(next_button)
        layout.addWidget(delete_button)
        
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.show_records()

    def show_records(self):
        self.records = self.get_records()
        if self.records:
            self.update_record_data()
        else:
            self.attribute_layout.addWidget(QLabel("Нет данных для отображения"))

    def get_records(self):
        db_handler = DatabaseHandler()
        records = db_handler.get_records(self.table)
        return records

    def show_prev_record(self):
        self.current_record_index -= 1
        if self.current_record_index < 0:
            self.current_record_index = 0
        self.update_record_data()

    def show_next_record(self):
        self.current_record_index += 1
        if self.current_record_index >= len(self.records):
            self.current_record_index = len(self.records) - 1
        self.update_record_data()

    def update_record_data(self):
        for i in reversed(range(self.attribute_layout.count())):
            widget = self.attribute_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        record_data = self.records[self.current_record_index]
        for attribute, value in record_data.items():
            label = QLabel(f"{attribute.capitalize()}: {value}", self)
            self.attribute_layout.addWidget(label)

    def delete_record(self):
        confirm_dialog = QMessageBox.question(self, 'Подтверждение удаления',
                                               'Вы уверены, что хотите удалить выбранную запись?',
                                               QMessageBox.Yes | QMessageBox.No)
        if confirm_dialog == QMessageBox.Yes:
            record_id = self.records[self.current_record_index]['id']
            db_handler = DatabaseHandler()
            db_handler.delete_record(self.table, record_id)
            self.records = self.get_records()
            if self.current_record_index >= len(self.records):
                self.current_record_index = len(self.records) - 1
            self.update_record_data()

class NotificationsWindow(QWidget):
    def __init__(self, parent=None):
        super(NotificationsWindow, self).__init__(parent)
        self.setWindowTitle("Оповещения")
        self.setGeometry(200, 200, 600, 400)  # Увеличил размер окна для наглядности
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Верхний блок: поиск оповещений
        search_layout = QHBoxLayout()
        search_label = QLabel("Найти:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите заголовок оповещения")
        self.search_edit.textChanged.connect(self.search_notifications)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)

        # Создаем горизонтальный блок для разделения области
        splitter = QSplitter()

        # Левая часть: список оповещений
        left_layout = QVBoxLayout()
        self.notification_list = QListWidget()
        self.notification_list.itemClicked.connect(self.show_notification_details)
        left_layout.addWidget(self.notification_list)

        # Правая часть: сообщения оповещений
        right_layout = QVBoxLayout()
        self.notification_details = QTextEdit()
        right_layout.addWidget(self.notification_details)

        # Добавляем компоненты в splitter
        splitter.addWidget(self.notification_list)
        splitter.addWidget(self.notification_details)

        # Устанавливаем горизонтальный блок внутри вертикального
        layout.addWidget(splitter)

        # Кнопка "Создать оповещение"
        create_button = QPushButton("Создать оповещение")
        create_button.clicked.connect(self.create_notification)
        layout.addWidget(create_button)

        # Добавляем кнопку "Назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        # Устанавливаем layout для виджета
        self.setLayout(layout)

        # Заполнение списка оповещений
        self.populate_notification_list()

    def populate_notification_list(self):
        # Получаем список оповещений из базы данных и добавляем их в список
        db_handler = DatabaseHandler()
        notifications = db_handler.get_notifications()
        for notification in notifications:
            self.notification_list.addItem(notification[0])  # Добавляем только первый элемент кортежа (заголовок оповещения)

    def search_notifications(self):
        # Метод для поиска оповещений по введенному пользователем тексту
        search_text = self.search_edit.text()
        self.notification_list.clear()
        db_handler = DatabaseHandler()
        notifications = db_handler.get_notifications(search_text)
        for notification in notifications:
            self.notification_list.addItem(notification[0])

    def show_notification_details(self, item):
        notification_title = item.text()
        db_handler = DatabaseHandler()
        notification_details = db_handler.get_notification_details(notification_title)
        if notification_details:
            self.notification_details.setPlainText(notification_details)
        else:
            self.notification_details.setPlainText("Детали оповещения не найдены.")

    def create_notification(self):
        # Метод для открытия окна создания нового оповещения
        create_notification_window = CreateNotificationWindow()
        create_notification_window.exec_()


class CreateNotificationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создать оповещение")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Введите название оповещения")
        layout.addWidget(self.title_edit)

        self.message_edit = QTextEdit()
        layout.addWidget(self.message_edit)

        create_button = QPushButton("Создать")
        create_button.clicked.connect(self.create_notification)
        layout.addWidget(create_button)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def create_notification(self):
        title = self.title_edit.text()
        message = self.message_edit.toPlainText()
        if title and message:
            db_handler = DatabaseHandler()
            db_handler.add_notification(title, message)
            self.title_edit.clear()
            self.message_edit.clear()

class SurveysWindow(QWidget):
    def __init__(self, db_handler):
        super().__init__()
        self.db_handler = db_handler
        self.setWindowTitle("Управление опросами")
        self.init_ui()

    def init_ui(self):
        # Название окна
        title_label = QLabel("Управление опросами", self)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Выпадающий список групп
        group_label = QLabel("Выбрать группу:", self)
        self.group_combo = QComboBox(self)
        self.group_combo.currentIndexChanged.connect(self.load_students_and_surveys)

        # Поле поиска группы
        search_group_label = QLabel("Или найти группу:", self)
        self.search_group_edit = QLineEdit(self)
        self.search_group_edit.setPlaceholderText("Введите название группы")
        self.search_group_edit.textChanged.connect(self.search_group)

        # Список студентов
        self.students_list = QListWidget(self)

        # Список опросов для выбранной группы
        self.surveys_list = QListWidget(self)
        self.surveys_list.itemClicked.connect(self.show_survey_answers)

        # Кнопка создания опроса
        create_survey_button = QPushButton("Создать опрос", self)
        create_survey_button.clicked.connect(self.create_survey_dialog)

        # Кнопка назад
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.close)

        # Создаем макет
        layout = QVBoxLayout()
        layout.addWidget(title_label)

        group_layout = QHBoxLayout()
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_group_label)
        search_layout.addWidget(self.search_group_edit)

        layout.addLayout(group_layout)
        layout.addLayout(search_layout)
        layout.addWidget(self.students_list)
        layout.addWidget(self.surveys_list)
        layout.addWidget(create_survey_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

        # Загружаем список групп при открытии окна
        self.load_groups()

    def load_groups(self):
        self.group_combo.clear()
        groups = self.db_handler.get_groups()
        for group in groups:
            self.group_combo.addItem(group[1])

    def load_students_and_surveys(self):
        self.students_list.clear()
        self.surveys_list.clear()

        group_index = self.group_combo.currentIndex()
        if group_index >= 0:
            group_id = self.db_handler.get_groups()[group_index][0]
            students = self.db_handler.get_students_by_group(group_id)
            for student in students:
                self.students_list.addItem(student[1])

            surveys = self.db_handler.get_surveys_by_group(group_id)
            for survey in surveys:
                self.surveys_list.addItem(survey[1])

    def search_group(self, text):
        self.group_combo.clear()
        groups = self.db_handler.search_groups(text)
        for group in groups:
            self.group_combo.addItem(group[1])

    def create_survey_dialog(self):
        dialog = CreateSurveyDialog(self.db_handler, self.group_combo.currentIndex(), self)
        dialog.exec_()

    def show_survey_answers(self, item):
        survey_name = item.text()
        group_index = self.group_combo.currentIndex()
        if group_index >= 0:
            group_id = self.db_handler.get_groups()[group_index][0]
            survey_id = self.db_handler.get_survey_id_by_name_and_group(survey_name, group_id)
            answers = self.db_handler.get_survey_answers(survey_id)
            if answers:
                QMessageBox.information(self, "Ответы на опрос", "\n".join(answers))
            else:
                QMessageBox.information(self, "Ответы на опрос", "На данный опрос пока нет ответов.")

class CreateSurveyDialog(QDialog):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание опроса")
        self.db_handler = db_handler
        self.group_index = group_index  # Сохраняем индекс выбранной группы
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_edit = QLineEdit(self)
        self.description_edit = QTextEdit(self)

        layout.addWidget(QLabel("Название опроса:", self))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Описание опроса:", self))
        layout.addWidget(self.description_edit)

        self.question_widgets = []

        add_question_button = QPushButton("Добавить вопрос", self)
        add_question_button.clicked.connect(self.add_question)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.create_survey)
        button_box.rejected.connect(self.reject)

        layout.addWidget(add_question_button)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def add_question(self):
        question_layout = QFormLayout()
        question_edit = QLineEdit(self)
        answer_edit = QLineEdit(self)
        self.question_widgets.append((question_edit, answer_edit))
        question_layout.addRow("Вопрос:", question_edit)
        question_layout.addRow("Ответ:", answer_edit)
        layout = self.layout()
        layout.insertLayout(layout.count() - 1, question_layout)

    def create_survey(self):
        title = self.title_edit.text()
        description = self.description_edit.toPlainText()
        if not title or not description:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите название и описание опроса.")
            return

        questions = []
        for question_edit, answer_edit in self.question_widgets:
            question = question_edit.text()
            answer = answer_edit.text()
            if not question or not answer:
                QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все поля вопросов и ответов.")
                return
            questions.append((question, answer))

        group_id = self.db_handler.get_groups()[self.group_index][0]  # Получаем group_id из индекса группы
        survey_id = self.db_handler.create_survey(title, description)
        if survey_id:
            for question, answer in questions:
                self.db_handler.create_question(survey_id, question, answer)
            QMessageBox.information(self, "Успех", "Опрос успешно создан.")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать опрос. Попробуйте еще раз.")


class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Преподаватель")
        # Код препада

class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Студент")
        # Добавьте элементы интерфейса и логику для студента здесь


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomWindow()
    welcome_window.show()
    sys.exit(app.exec_())
