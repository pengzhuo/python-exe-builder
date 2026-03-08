import sys
import customtkinter as ctk
from core.logic import start_process


class MainWindow:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("三角洲辅助")
        self.app.geometry("420x260")
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

        # 子弹ID
        label_id = ctk.CTkLabel(frame, text="子弹ID")
        label_id.grid(row=0, column=0, padx=10, pady=10)

        self.id_input = ctk.CTkEntry(
            frame,
            width=180,
            placeholder_text="输入子弹ID"
        )
        self.id_input.grid(row=0, column=1, padx=10)

        # 子弹价格
        label_price = ctk.CTkLabel(frame, text="子弹价格")
        label_price.grid(row=1, column=0, padx=10, pady=10)

        self.price_input = ctk.CTkEntry(
            frame,
            width=180,
            placeholder_text="输入子弹价格"
        )
        self.price_input.grid(row=1, column=1, padx=10)

        # 开始按钮
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
        sys.exit()
        # bullet_id = self.id_input.get()
        # price = self.price_input.get()

        # text = start_process(price)

        # self.result.configure(
        #     text=f"ID:{bullet_id}  价格:{price}"
        # )

    def run(self):
        self.app.mainloop()