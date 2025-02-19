import tkinter as tk
from tkinter import messagebox
import json


class Employee:
    """Класс, представляющий сотрудника."""

    def __init__(self, employee_id, name, position, salary):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"ID: {self.employee_id}, Имя: {self.name}, Должность: {self.position}, Зарплата: {self.salary}"

    def to_dict(self):
        """Возвращает словарь, представляющий сотрудника."""
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "position": self.position,
            "salary": self.salary,
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект Employee из словаря."""
        return cls(data["employee_id"], data["name"], data["position"], data["salary"])


class EmployeeManager:
    """Класс, управляющий списком сотрудников."""

    def __init__(self, master):
        self.master = master
        master.title("Менеджер сотрудников")

        self.employees = []  # Список объектов Employee
        self.filename = "employees.json"  # Файл для сохранения данных

        self.load_data()  # Загружаем данные при запуске

        # Labels и Entry для ввода данных сотрудника
        tk.Label(master, text="ID сотрудника:").grid(row=0, column=0, sticky="w")
        self.id_entry = tk.Entry(master)
        self.id_entry.grid(row=0, column=1, sticky="w")

        tk.Label(master, text="Имя:").grid(row=1, column=0, sticky="w")
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=1, column=1, sticky="w")

        tk.Label(master, text="Должность:").grid(row=2, column=0, sticky="w")
        self.position_entry = tk.Entry(master)
        self.position_entry.grid(row=2, column=1, sticky="w")

        tk.Label(master, text="Зарплата:").grid(row=3, column=0, sticky="w")
        self.salary_entry = tk.Entry(master)
        self.salary_entry.grid(row=3, column=1, sticky="w")

        # Кнопки
        tk.Button(master, text="Добавить сотрудника", command=self.add_employee).grid(row=4, column=0, columnspan=2,
                                                                                       pady=10)
        tk.Button(master, text="Просмотреть сотрудников", command=self.view_employees).grid(row=5, column=0,
                                                                                            columnspan=2, pady=10)
        tk.Button(master, text="Найти сотрудника", command=self.search_employee).grid(row=6, column=0, columnspan=2,
                                                                                     pady=10)
        tk.Button(master, text="Обновить сотрудника", command=self.update_employee).grid(row=7, column=0,
                                                                                         columnspan=2, pady=10)
        tk.Button(master, text="Удалить сотрудника", command=self.delete_employee).grid(row=8, column=0,
                                                                                       columnspan=2, pady=10)

        # Текстовое поле для отображения информации
        self.text_area = tk.Text(master, height=15, width=50)
        self.text_area.grid(row=9, column=0, columnspan=2, pady=10)

    def add_employee(self):
        """Добавляет нового сотрудника."""
        try:
            employee_id = int(self.id_entry.get())
            name = self.name_entry.get()
            position = self.position_entry.get()
            salary = float(self.salary_entry.get())

            employee = Employee(employee_id, name, position, salary)
            self.employees.append(employee)
            self.clear_entries()
            self.save_data()
            messagebox.showinfo("Успех", "Сотрудник успешно добавлен.")

        except ValueError:
            messagebox.showerror("Ошибка",
                                 "Некорректный ввод. Пожалуйста, введите числовые значения для ID и зарплаты.")

    def view_employees(self):
        """Просматривает список сотрудников."""
        self.text_area.delete("1.0", tk.END)  # Очищаем текстовое поле
        if not self.employees:
            self.text_area.insert(tk.END, "Список сотрудников пуст.")
            return

        for employee in self.employees:
            self.text_area.insert(tk.END, str(employee) + "\n")  # Добавляем каждого сотрудника в поле

    def search_employee(self):
        """Ищет сотрудника по ID."""
        try:
            employee_id = int(self.id_entry.get())
            self.text_area.delete("1.0", tk.END) # Очистка перед новым поиском
            for employee in self.employees:
                if employee.employee_id == employee_id:
                    self.text_area.insert(tk.END, str(employee))
                    return
            self.text_area.insert(tk.END, "Сотрудник с таким ID не найден.")

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод. Пожалуйста, введите числовой ID.")

    def update_employee(self):
        """Обновляет информацию о сотруднике."""
        try:
            employee_id = int(self.id_entry.get())
            for employee in self.employees:
                if employee.employee_id == employee_id:
                    # Открываем новое окно для обновления информации
                    update_window = tk.Toplevel(self.master)
                    update_window.title("Обновление сотрудника")

                    tk.Label(update_window, text="Имя:").grid(row=0, column=0, sticky="w")
                    name_entry = tk.Entry(update_window)
                    name_entry.insert(0, employee.name) # Заполняем текущим значением
                    name_entry.grid(row=0, column=1, sticky="w")

                    tk.Label(update_window, text="Должность:").grid(row=1, column=0, sticky="w")
                    position_entry = tk.Entry(update_window)
                    position_entry.insert(0, employee.position) # Заполняем текущим значением
                    position_entry.grid(row=1, column=1, sticky="w")

                    tk.Label(update_window, text="Зарплата:").grid(row=2, column=0, sticky="w")
                    salary_entry = tk.Entry(update_window)
                    salary_entry.insert(0, str(employee.salary)) # Заполняем текущим значением
                    salary_entry.grid(row=2, column=1, sticky="w")

                    def save_update():
                        """Сохраняет обновленную информацию."""
                        try:
                            new_name = name_entry.get()
                            new_position = position_entry.get()
                            new_salary = float(salary_entry.get())

                            employee.name = new_name
                            employee.position = new_position
                            employee.salary = new_salary

                            self.save_data() # Сохраняем изменения в файл
                            self.view_employees() # Обновляем отображение списка
                            messagebox.showinfo("Успех", "Информация о сотруднике успешно обновлена.")
                            update_window.destroy()

                        except ValueError:
                            messagebox.showerror("Ошибка", "Некорректный ввод для зарплаты.")

                    tk.Button(update_window, text="Сохранить", command=save_update).grid(row=3, column=0,
                                                                                           columnspan=2, pady=10)
                    return

            messagebox.showinfo("Информация", "Сотрудник с таким ID не найден.")

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод. Пожалуйста, введите числовой ID.")

    def delete_employee(self):
        """Удаляет сотрудника по ID."""
        try:
            employee_id = int(self.id_entry.get())
            for employee in self.employees:
                if employee.employee_id == employee_id:
                    self.employees.remove(employee)
                    self.save_data() # Сохраняем изменения в файл
                    self.view_employees() # Обновляем список
                    messagebox.showinfo("Успех", "Сотрудник успешно удален.")
                    return

            messagebox.showinfo("Информация", "Сотрудник с таким ID не найден.")

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод. Пожалуйста, введите числовой ID.")

    def clear_entries(self):
        """Очищает поля ввода."""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)

    def save_data(self):
        """Сохраняет данные о сотрудниках в файл."""
        data = [employee.to_dict() for employee in self.employees]
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)  # Используем JSON для сохранения
            print("Данные успешно сохранены в файл.")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def load_data(self):
        """Загружает данные о сотрудниках из файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)  # Читаем JSON из файла
                self.employees = [Employee.from_dict(emp) for emp in data] #Преобразуем словари в объекты Employee
            print("Данные успешно загружены из файла.")
            self.view_employees() # Отображаем загруженные данные
        except FileNotFoundError:
            print("Файл не найден. Создан новый список сотрудников.") #Если файла нет, ничего страшного
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")



def main():
    """Основная функция программы."""
    root = tk.Tk()
    manager = EmployeeManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()