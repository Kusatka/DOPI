import tkinter as tk
from tkinter import ttk

HUNDREDS = {
    "сто": 100,
    "двести": 200,
    "триста": 300,
    "четыреста": 400,
    "пятьсот": 500,
    "шестьсот": 600,
    "семьсот": 700,
    "восемьсот": 800,
    "девятьсот": 900,
}

TENS = {
    "десять": 10,
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
}

TEENS = {
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
}

UNITS = {
    "ноль": 0,
    "один": 1,
    "два": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
}

ELEMENT_INFO = {
    "hundreds": {
        "weight": 4,
        "label_full": "Число формата сотен",
        "label_lower": "числом формата сотен",
    },
    "tens": {
        "weight": 3,
        "label_full": "Число десятичного формата",
        "label_lower": "числом десятичного формата",
    },
    "teens": {
        "weight": 2,
        "label_full": "Число формата 11-19",
        "label_lower": "числом формата 11-19",
    },
    "units": {
        "weight": 1,
        "label_full": "Число единичного формата",
        "label_lower": "числом единичного формата",
    },
}


class ASTNode:
    def __init__(self):
        self.hundreds = None
        self.tens = None
        self.teens = None
        self.units = None

    def value(self):
        total = 0
        if self.hundreds:
            total += self.hundreds[1]
        if self.tens:
            total += self.tens[1]
        if self.teens:
            total += self.teens[1]
        if self.units:
            total += self.units[1]
        return total


def classify_token(tok):
    tok_l = tok.lower()
    if tok_l in HUNDREDS:
        return "hundreds", HUNDREDS[tok_l], tok_l
    if tok_l in TEENS:
        return "teens", TEENS[tok_l], tok_l
    if tok_l in TENS:
        return "tens", TENS[tok_l], tok_l
    if tok_l in UNITS:
        return "units", UNITS[tok_l], tok_l
    return None, None, tok_l


def check_pair(prev, cur):
    """Может ли слово cur стоять сразу после слова prev.
    prev, cur: (тип, слово, значение). Возвращает текст ошибки или None."""
    prev_type, prev_word, prev_val = prev
    cur_type, cur_word, cur_val = cur

    if prev_word == "ноль" or cur_word == "ноль":
        return 'Число "ноль" не может сочетаться с другими числами'

    if prev_type == cur_type:
        label_full = ELEMENT_INFO[cur_type]["label_full"]
        label_lower = ELEMENT_INFO[prev_type]["label_lower"]
        return f"{label_full} не может стоять за {label_lower}"

    if ELEMENT_INFO[prev_type]["weight"] < ELEMENT_INFO[cur_type]["weight"]:
        first_label = ELEMENT_INFO[prev_type]["label_full"]
        second_label_lower = ELEMENT_INFO[cur_type]["label_lower"]
        return f"{first_label} не может стоять перед {second_label_lower}"

    if prev_type == "teens" and cur_type == "units":
        return (
            f"{ELEMENT_INFO['teens']['label_full']} не может сочетаться с "
            f"{ELEMENT_INFO['units']['label_lower']}"
        )

    if prev_type == "tens" and cur_type == "teens":
        return (
            f"{ELEMENT_INFO['tens']['label_full']} не может сочетаться с "
            f"{ELEMENT_INFO['teens']['label_lower']}"
        )

    if prev_type == "tens" and prev_val == 10 and cur_type == "units":
        return (
            f"Число десятичного формата '{prev_word}' не может сочетаться с "
            f"{ELEMENT_INFO['units']['label_lower']}"
        )

    return None


def parse_sentence(sentence):
    """Разбор слева направо до первой ошибки.
    Каждое слово проверяется по словарю в тот момент, когда до него дошёл разбор,
    поэтому сообщение всегда относится к первой ошибке в тексте.
    Возвращает (ast, None) или (None, текст ошибки)."""
    tokens = (sentence or "").split()
    if not tokens:
        return None, "Введите число от 0 до 999 словами"

    ast = ASTNode()
    prev = None
    for tok in tokens:
        if tok.isdigit():
            return None, f'Ошибка в слове "{tok}": число нужно ввести словами'

        typ, val, orig = classify_token(tok)
        if typ is None:
            return None, f'Ошибка в слове "{orig}"'

        cur = (typ, orig, val)
        if prev is not None:
            error = check_pair(prev, cur)
            if error:
                return None, error

        setattr(ast, typ, (orig, val))
        prev = cur

    return ast, None


class NumberWordsApp:
    def __init__(self, root):
        self.root = root
        root.title("Преобразование букв в числа")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        frame = ttk.Frame(root, padding=12)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        self.entry = ttk.Entry(frame, font=("Segoe UI", 12))
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.entry.bind("<Return>", self.on_convert)

        self.btn = ttk.Button(frame, text="Конвертировать", command=self.on_convert)
        self.btn.grid(row=0, column=1)

        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(
            frame, textvariable=self.result_var, font=("Segoe UI", 12), state="readonly"
        )
        self.result_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        hint = ttk.Label(
            frame,
            text='Введите число от 0 до 999 словами (пример: "девятьсот один").',
        )
        hint.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        self.center_window(root, 560, 160)

    def on_convert(self, event=None):
        # Старый ответ не должен оставаться на экране рядом с сообщением об ошибке.
        self.result_var.set("")

        parsed, error = parse_sentence(self.entry.get())
        if error:
            self.show_error(error)
            return

        self.result_var.set(str(parsed.value()))

    def show_error(self, msg):
        win = tk.Toplevel(self.root)
        win.title("Ошибка ввода")
        win.transient(self.root)
        win.grab_set()

        frm = ttk.Frame(win, padding=12)
        frm.grid(sticky="nsew")
        frm.columnconfigure(0, weight=1)

        lbl = ttk.Label(frm, text=msg, font=("Segoe UI", 11))
        lbl.grid(row=0, column=0, sticky="w")

        btn = ttk.Button(frm, text="ОК", command=win.destroy)
        btn.grid(row=1, column=0, pady=(10, 0), sticky="e")

        self.center_toplevel(win)

    def center_window(self, win, width, height):
        win.update_idletasks()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (width // 2)
        y = (hs // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def center_toplevel(self, win):
        win.update_idletasks()
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f"+{x}+{y}")


def main():
    root = tk.Tk()
    app = NumberWordsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
