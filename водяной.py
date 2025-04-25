#водяной
import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread
import time

class WaterTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Водяной")
        self.root.geometry("400x550")
        self.root.configure(bg="#f0f8ff")

        # Переменные
        self.daily_goal = 2000  # мл (стандартная норма)
        self.current_water = 0
        self.reminder_enabled = True
        self.reminder_interval = 60  # минуты
        self.last_reminder_time = 0
        
        # Запуск потока для напоминаний
        self.reminder_thread = Thread(target=self.reminder_loop, daemon=True)
        self.reminder_thread.start()

        # Виджеты
        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Водяной",
            font=("Arial", 24, "bold"),
            bg="#f0f8ff",
            fg="#4682b4"
        )
        title_label.pack(pady=20)

        # Прогресс-бар
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        # Текущий прогресс (в %)
        self.progress_label = tk.Label(
            self.root,
            text="0%",
            font=("Arial", 14),
            bg="#f0f8ff"
        )
        self.progress_label.pack()

        # Количество выпитой воды
        self.water_label = tk.Label(
            self.root,
            text=f"Выпито: 0 мл / {self.daily_goal} мл",
            font=("Arial", 12),
            bg="#f0f8ff"
        )
        self.water_label.pack(pady=10)

        # Кнопки для добавления воды
        buttons_frame = tk.Frame(self.root, bg="#f0f8ff")
        buttons_frame.pack(pady=20)

        button_100 = tk.Button(
            buttons_frame,
            text="+100 мл",
            command=lambda: self.add_water(100),
            bg="#add8e6",
            padx=10,
            pady=5
        )
        button_100.grid(row=0, column=0, padx=5)

        button_250 = tk.Button(
            buttons_frame,
            text="+250 мл",
            command=lambda: self.add_water(250),
            bg="#87ceeb",
            padx=10,
            pady=5
        )
        button_250.grid(row=0, column=1, padx=5)

        button_500 = tk.Button(
            buttons_frame,
            text="+500 мл",
            command=lambda: self.add_water(500),
            bg="#4682b4",
            fg="white",
            padx=10,
            pady=5
        )
        button_500.grid(row=0, column=2, padx=5)

        # Ручной ввод
        input_frame = tk.Frame(self.root, bg="#f0f8ff")
        input_frame.pack(pady=10)

        self.entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
        self.entry.grid(row=0, column=0, padx=5)

        add_button = tk.Button(
            input_frame,
            text="Добавить (мл)",
            command=self.add_custom_water,
            bg="#e6e6fa",
            padx=5,
            pady=2
        )
        add_button.grid(row=0, column=1, padx=5)

        # Кнопка сброса
        reset_button = tk.Button(
            self.root,
            text="Сбросить",
            command=self.reset_water,
            bg="#ffb6c1",
            padx=10,
            pady=5
        )
        reset_button.pack(pady=10)

        # Кнопка настроек
        settings_button = tk.Button(
            self.root,
            text="Настройки напоминаний",
            command=self.open_settings,
            bg="#d8bfd8",
            padx=10,
            pady=5
        )
        settings_button.pack(pady=5)

    def add_water(self, amount):
        """Добавляет воду и обновляет интерфейс."""
        self.current_water += amount
        self.update_display()
        self.check_goal()

    def add_custom_water(self):
        """Добавляет воду из поля ввода."""
        try:
            amount = int(self.entry.get())
            self.add_water(amount)
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число!")

    def reset_water(self):
        """Сбрасывает счетчик воды."""
        self.current_water = 0
        self.update_display()

    def update_display(self):
        """Обновляет прогресс-бар и текстовые метки."""
        progress_percent = (self.current_water / self.daily_goal) * 100
        self.progress["value"] = progress_percent
        self.progress_label.config(text=f"{int(progress_percent)}%")
        self.water_label.config(text=f"Выпито: {self.current_water} мл / {self.daily_goal} мл")

    def check_goal(self):
        """Проверяет, достигнута ли дневная норма."""
        if self.current_water >= self.daily_goal:
            messagebox.showinfo("Поздравляем!", "Вы достигли дневной нормы воды!")

    def reminder_loop(self):
        """Цикл для напоминаний."""
        while True:
            if self.reminder_enabled:
                current_time = time.time()
                if current_time - self.last_reminder_time > self.reminder_interval * 60:
                    self.last_reminder_time = current_time
                    self.root.after(0, self.show_reminder)
            time.sleep(60)  # Проверяем каждую минуту

    def show_reminder(self):
        """Показывает напоминание."""
        if self.current_water < self.daily_goal:
            messagebox.showinfo("Напоминание", "Пора выпить воды! 💧")
            self.last_reminder_time = time.time()

    def open_settings(self):
        """Открывает окно настроек напоминаний."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки напоминаний")
        settings_window.geometry("300x200")
        settings_window.configure(bg="#f0f8ff")
        settings_window.resizable(False, False)

        # Переключатель напоминаний
        reminder_var = tk.BooleanVar(value=self.reminder_enabled)
        reminder_check = tk.Checkbutton(
            settings_window,
            text="Включить напоминания",
            variable=reminder_var,
            font=("Arial", 12),
            bg="#f0f8ff",
            command=lambda: self.toggle_reminders(reminder_var.get())
        )
        reminder_check.pack(pady=10)

        # Интервал напоминаний
        interval_frame = tk.Frame(settings_window, bg="#f0f8ff")
        interval_frame.pack(pady=10)

        tk.Label(
            interval_frame,
            text="Интервал (мин):",
            font=("Arial", 12),
            bg="#f0f8ff"
        ).grid(row=0, column=0, padx=5)

        interval_var = tk.IntVar(value=self.reminder_interval)
        interval_entry = tk.Entry(
            interval_frame,
            textvariable=interval_var,
            width=5,
            font=("Arial", 12)
        )
        interval_entry.grid(row=0, column=1, padx=5)

        save_button = tk.Button(
            settings_window,
            text="Сохранить",
            command=lambda: self.save_settings(interval_var.get()),
            bg="#4682b4",
            fg="white",
            padx=10,
            pady=5
        )
        save_button.pack(pady=20)

    def toggle_reminders(self, enabled):
        """Включает/выключает напоминания."""
        self.reminder_enabled = enabled
        if enabled:
            self.last_reminder_time = time.time()

    def save_settings(self, interval):
        """Сохраняет настройки напоминаний."""
        if interval > 0:
            self.reminder_interval = interval
            self.last_reminder_time = time.time()
            messagebox.showinfo("Сохранено", "Настройки напоминаний сохранены!")
        else:
            messagebox.showerror("Ошибка", "Интервал должен быть положительным числом!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterTrackerApp(root)
    root.mainloop()