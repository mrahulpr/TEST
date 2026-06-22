import tkinter as tk

def on_click(button_text):
    current = entry.get()
    if button_text == "=":
        try:
            result = eval(current.replace('×', '*').replace('÷', '/'))
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif button_text == "C":
        entry.delete(0, tk.END)
    elif button_text == "⌫":
        entry.delete(len(current)-1, tk.END)
    else:
        entry.insert(tk.END, button_text)

root = tk.Tk()
root.title("Calculator")

entry = tk.Entry(root, width=20, font=('Arial', 24), borderwidth=5, justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    '%', 'CE', 'C', '⌫',
    '1/x', 'x²', '√x', '÷',
    '7', '8', '9', '×',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '+/-', '0', '.', '='
]

row_val = 1
col_val = 0
for button in buttons:
    tk.Button(root, text=button, width=5, height=2, font=('Arial', 14),
              command=lambda b=button: on_click(b)).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

root.mainloop()
