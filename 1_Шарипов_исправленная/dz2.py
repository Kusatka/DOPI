import re
import tkinter as tk

# Число: необязательный знак, цифры 0-9, необязательная дробная часть через точку.
NUMBER = re.compile(r"[+-]?[0-9]+(\.[0-9]+)?")


class ChessNumbersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шахматный порядок чисел")

        self.root.geometry("500x300")
        self.center_window(self.root, 500, 300)
        self.root.resizable(True, True)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=2)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

        label1 = tk.Label(root, text="Первая строка:", font=("Arial", 11))
        label1.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry1 = tk.Entry(root, font=("Arial", 11))
        self.entry1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        label2 = tk.Label(root, text="Вторая строка:", font=("Arial", 11))
        label2.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry2 = tk.Entry(root, font=("Arial", 11))
        self.entry2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.process_btn = tk.Button(
            root,
            text="Вывести в шахматном порядке",
            font=("Arial", 11, "bold"),
            bg="#8890E5",
            fg="white",
            activebackground="#b1abe7",
            cursor="hand2",
            command=self.process_numbers,
        )
        self.process_btn.grid(
            row=2, column=0, columnspan=2, pady=15, padx=50, sticky="ew"
        )

        result_label = tk.Label(root, text="Результат:", font=("Arial", 11, "bold"))
        result_label.grid(
            row=3, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w"
        )

        self.result_text = tk.Text(
            root, font=("Arial", 10), height=5, state="disabled", wrap="word"
        )
        self.result_text.grid(
            row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew"
        )

        self.entry1.bind("<Return>", lambda e: self.process_numbers())
        self.entry2.bind("<Return>", lambda e: self.process_numbers())

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Ошибка")

        error_window.geometry("400x150")
        self.center_window(error_window, 400, 150)
        error_window.resizable(False, False)
        error_window.transient(self.root)
        error_window.grab_set()

        frame = tk.Frame(error_window)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        error_label = tk.Label(
            frame, text=message, font=("Arial", 10), wraplength=360, justify="center"
        )
        error_label.pack(pady=(0, 15))

        ok_btn = tk.Button(
            frame,
            text="ОК",
            font=("Arial", 10),
            width=10,
            command=error_window.destroy,
            bg="#f44336",
            fg="white",
            cursor="hand2",
        )
        ok_btn.pack()

    def set_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, text)
        self.result_text.config(state="disabled")

    def parse_line(self, text):
        """Строка -> (числа в том виде, как их ввели, None) или (None, текст ошибки).
        Слова проверяются слева направо до первой ошибки."""
        text = text.strip()
        if not text:
            return None, "Ошибка: Оба поля должны быть заполнены!"

        numbers = text.split()
        for num in numbers:
            if not NUMBER.fullmatch(num):
                return None, f"Ошибка: '{num}' не является корректным числом!"
        return numbers, None

    def process_numbers(self):
        # Старый результат не должен оставаться на экране рядом с сообщением об ошибке.
        self.set_result("")
        try:
            numbers1, error = self.parse_line(self.entry1.get())
            if error:
                self.show_error(error)
                return

            numbers2, error = self.parse_line(self.entry2.get())
            if error:
                self.show_error(error)
                return

            result = []
            max_len = max(len(numbers1), len(numbers2))

            for i in range(max_len):
                if i < len(numbers1):
                    result.append(numbers1[i])
                if i < len(numbers2):
                    result.append(numbers2[i])

            self.set_result(" ".join(result))

        except Exception as e:
            self.show_error(f"Непредвиденная ошибка: {str(e)}")


def main():
    root = tk.Tk()
    app = ChessNumbersApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
