import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import keyboard
import re
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, Listbox, EXTENDED

# ================== 配置 ==================
CONFIG_FILE = "config.json"
BULLET_FILE = "bullets.txt"

# 加载坐标配置
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
else:
    CONFIG = {
        "tesseract_cmd": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        "price_region": [1520, 420, 300, 80],
        "name_region": [1100, 380, 400, 60],
        "item_positions": [[960, 480], [960, 580], [960, 680], [960, 780]],
        "buy_button_pos": [1650, 650],
        "refresh_pos": [1800, 300],
        "refresh_interval": 8,
        "auto_refresh": True
    }

pytesseract.pytesseract.tesseract_cmd = CONFIG.get("tesseract_cmd", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

selected_bullets = []
buy_amount = 10
running = False
bullet_dict = {}
last_refresh_time = 0

def load_bullets():
    global bullet_dict
    bullet_dict.clear()
    if not os.path.exists(BULLET_FILE):
        messagebox.showerror("错误", f"未找到 {BULLET_FILE}！请创建并按 名称:价格 格式填写。")
        return False
    try:
        with open(BULLET_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and ":" in line:
                    name, price_str = line.split(":", 1)
                    name = name.strip()
                    try:
                        bullet_dict[name] = int(price_str.strip())
                    except:
                        pass
        return True
    except Exception as e:
        messagebox.showerror("错误", str(e))
        return False

def capture_text(region):
    screenshot = pyautogui.screenshot(region=region)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(gray, lang='chi_sim+eng').strip()
    return text

def auto_buy():
    global running, last_refresh_time
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 多子弹监控启动 | 选中 {len(selected_bullets)} 种 | 自动刷新: {CONFIG.get('auto_refresh', True)}")
    start_time = time.time()
    scan_count = 0
    
    while running:
        if keyboard.is_pressed('f9'):
            break
        
        # 自动刷新
        if CONFIG.get("auto_refresh", True) and time.time() - last_refresh_time > CONFIG.get("refresh_interval", 8):
            try:
                pyautogui.click(CONFIG["refresh_pos"][0], CONFIG["refresh_pos"][1])
                last_refresh_time = time.time()
                print("已自动刷新交易行")
                time.sleep(0.6)
            except:
                pass
        
        for pos in CONFIG["item_positions"]:
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.35)
            
            name_text = capture_text(tuple(CONFIG["name_region"]))
            price_text = capture_text(tuple(CONFIG["price_region"]))
            
            price_match = re.findall(r'\d+', price_text.replace(',', ''))
            price = int(price_match[0]) if price_match else None
            
            for bullet_name in selected_bullets:
                if bullet_name.lower() in name_text.lower():
                    cfg_price = bullet_dict.get(bullet_name, 999999)
                    if price and price <= cfg_price:
                        print(f"🎯 发现低价！{bullet_name} 价格 {price} ≤ {cfg_price}，立即抢购...")
                        pyautogui.click(CONFIG["buy_button_pos"][0], CONFIG["buy_button_pos"][1])
                        time.sleep(0.3)
                        for _ in range(buy_amount):
                            pyautogui.press('backspace')
                        pyautogui.typewrite(str(buy_amount))
                        time.sleep(0.2)
                        pyautogui.press('enter')
                        print(f"🚀 已下单 {buy_amount} 发 {bullet_name}！")
                        time.sleep(2.5)
                        break  # 抢到后跳出本次循环
            else:
                continue
            break  # 如果抢到就跳出物品循环
        
        scan_count += 1
        time.sleep(0.7)

# ================== GUI ==================
def refresh_all():
    if load_bullets():
        listbox.delete(0, tk.END)
        for name in bullet_dict.keys():
            listbox.insert(tk.END, name)
        status_label.config(text=f"已加载 {len(bullet_dict)} 种子弹")

def start_monitoring():
    global selected_bullets, buy_amount, running
    sel_indices = listbox.curselection()
    if not sel_indices:
        messagebox.showwarning("警告", "请至少选择一种子弹！")
        return
    try:
        buy_amount = int(amount_entry.get())
    except:
        messagebox.showerror("错误", "购买数量必须是数字！")
        return
    
    selected_bullets = [listbox.get(i) for i in sel_indices]
    running = True
    status_label.config(text=f"运行中... 选中 {len(selected_bullets)} 种子弹")
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    
    import threading
    threading.Thread(target=auto_buy, daemon=True).start()

def stop_monitoring():
    global running
    running = False
    status_label.config(text="已停止")
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

root = tk.Tk()
root.title("三角洲行动 多子弹抢购助手（自动刷新 + 多选）")
root.geometry("580x520")
root.resizable(False, False)

tk.Label(root, text="bullets.txt 配置（名称:价格）", font=("微软雅黑", 11)).pack(pady=5)

refresh_btn = tk.Button(root, text="刷新配置文件", command=refresh_all, bg="#2196F3", fg="white")
refresh_btn.pack(pady=5)

tk.Label(root, text="按住 Ctrl 多选要抢的子弹：", font=("微软雅黑", 12)).pack(pady=8)

listbox = Listbox(root, selectmode=EXTENDED, height=12, font=("微软雅黑", 10), width=60)
listbox.pack(pady=5)

tk.Label(root, text="单次购买数量：", font=("微软雅黑", 10)).pack(pady=(10,5))
amount_entry = tk.Entry(root, width=15, font=("微软雅黑", 11))
amount_entry.insert(0, "10")
amount_entry.pack()

start_btn = tk.Button(root, text="开始监控 (F8)", font=("微软雅黑", 12), bg="#4CAF50", fg="white", command=start_monitoring)
start_btn.pack(pady=12)

stop_btn = tk.Button(root, text="停止监控 (F9)", font=("微软雅黑", 12), bg="#f44336", fg="white", command=stop_monitoring, state="disabled")
stop_btn.pack()

status_label = tk.Label(root, text="就绪 - 请编辑 bullets.txt 并点击刷新", font=("微软雅黑", 10), fg="blue")
status_label.pack(pady=10)

tk.Label(root, text="提示：\n1. 游戏窗口模式 1920x1080\n2. 把子弹加入收藏夹前几位\n3. 可编辑 config.json 调整坐标与刷新间隔", 
         font=("微软雅黑", 9), fg="gray", justify="left").pack(pady=10)

# 初始加载
load_bullets()
for name in bullet_dict.keys():
    listbox.insert(tk.END, name)

keyboard.add_hotkey('f8', lambda: start_monitoring() if not running else None)
keyboard.add_hotkey('f9', stop_monitoring)

root.mainloop()