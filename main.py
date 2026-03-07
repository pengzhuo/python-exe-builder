import customtkinter as ctk

# 设置主题
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def start_action():
    os.exit()

# 创建窗口
app = ctk.CTk()
app.title("三角洲辅助")
app.geometry("400x200")

# 标题
title_label = ctk.CTkLabel(app, text="三角洲辅助", font=("微软雅黑", 22, "bold"))
title_label.pack(pady=15)

# 输入区域
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

label_price = ctk.CTkLabel(frame, text="子弹价格", font=("微软雅黑", 14))
label_price.grid(row=0, column=0, padx=10, pady=10)

entry_price = ctk.CTkEntry(frame, width=160, placeholder_text="请输入价格")
entry_price.grid(row=0, column=1, padx=10, pady=10)

# 开始按钮
start_btn = ctk.CTkButton(app, text="开始", width=200, height=40, command=start_action)
start_btn.pack(pady=15)

app.mainloop()
