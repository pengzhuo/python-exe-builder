import customtkinter as ctk
from core.logic import start_process

class MainWindow:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("三角洲辅助")
        self.app.geometry("420x220")
        self.app.resizable(False, False)

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self.app,
            text="三角洲辅助",
            font=("Microsoft YaHei", 22, "bold")
        )
        title.pack(pady=15)

        frame = ctk.CTkFrame(self.app)
        frame.pack(pady=10)

        label = ctk.CTkLabel(frame, text="子弹价格")
        label.grid(row=0, column=0, padx=10, pady=10)

        self.price_input = ctk.CTkEntry(
            frame,
            width=180,
            placeholder_text="输入子弹价格"
        )
        self.price_input.grid(row=0, column=1, padx=10)

        start_btn = ctk.CTkButton(
            self.app,
            text="开始",
            width=220,
            height=40,
            command=self.start_click
        )
        start_btn.pack(pady=15)

        self.result = ctk.CTkLabel(self.app, text="")
        self.result.pack()

    def start_click(self):
        price = self.price_input.get()
        text = start_process(price)
        self.result.configure(text=text)

    def run(self):
        self.app.mainloop()
