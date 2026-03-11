import sys
import customtkinter as ctk
from core.logic import start_process
import os
import logging


class MainWindow:

    def __init__(self):

        log_dir = os.path.join(os.getcwd(), "logs")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, "app.log")

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

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

        # 子弹类型列表
        bullet_types = [
            "PRS","T","PS","BT","BS","RRLP","FMJ","M855",
            "M855A1","M995","BPZ","M80","M62","M61",
            "PSO","Pst","AP6.3","RIP"
        ]

        # 子弹ID（下拉框）
        label_id = ctk.CTkLabel(frame, text="子弹ID")
        label_id.grid(row=0, column=0, padx=10, pady=10)

        self.bullet_select = ctk.CTkOptionMenu(
            frame,
            values=bullet_types,
            width=180
        )
        self.bullet_select.grid(row=0, column=1, padx=10)

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
        logging.info("注入进程失败！error[10001]")
        sys.exit()

    def run(self):
        logging.info("程序启动")
        self.app.mainloop()