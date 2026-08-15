# -*- coding: utf-8 -*-
"""
ساختارشکن - ابزار گرافیکی برای ایجاد پوشه‌ها و فایل‌ها
تهیه‌کننده: MA.AD.GH
گیت‌هاب: https://github.com/mahanneman
"""

import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

class StructureBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("ساختارشکن - سازنده‌ی پوشه و فایل")
        self.root.geometry("800x600")
        self.base_path = tk.StringVar(value=os.getcwd())
        self.tree_nodes = {}  # نگهداری آی‌دی گره‌ها برای دسترسی سریع

        self.create_widgets()
        self.populate_tree_from_text("""
        پروژه/
            Agent/
                V1/
                    main_agent.py
                    router.py
                    executor.py
                    system_scan.py
                    browser_tool.py
                    file_tool.py
                    code_agent.py
            Models/
                qwen2.5-1.5b.gguf
            Whisper/
        """)  # یک نمونه اولیه از ساختار درخواستی شما

    def create_widgets(self):
        # ========== نوار ابزار ==========
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="➕ افزودن پوشه", command=self.add_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📄 افزودن فایل", command=self.add_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑 حذف", command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 ساخت", command=self.build_structure).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🧹 پاک‌سازی", command=self.clear_tree).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📝 وارد کردن از متن", command=self.open_text_import).pack(side=tk.LEFT, padx=2)

        # ========== درخت ==========
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("type",), show="tree headings")
        self.tree.heading("#0", text="نام")
        self.tree.heading("type", text="نوع")
        self.tree.column("type", width=80, anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # منوی راست‌کلیک
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="افزودن پوشه", command=self.add_folder)
        self.context_menu.add_command(label="افزودن فایل", command=self.add_file)
        self.context_menu.add_command(label="حذف", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)

        # ========== پایین صفحه: مسیر و اطلاعات ==========
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        ttk.Label(bottom_frame, text="مسیر پایه:").pack(side=tk.LEFT)
        path_entry = ttk.Entry(bottom_frame, textvariable=self.base_path, width=50)
        path_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(bottom_frame, text="انتخاب مسیر", command=self.select_path).pack(side=tk.LEFT, padx=2)

        # برچسب تهیه‌کننده
        info_label = ttk.Label(
            bottom_frame,
            text="تهیه‌کننده: MA.AD.GH | GitHub: https://github.com/mahanneman",
            font=("Arial", 9, "italic")
        )
        info_label.pack(side=tk.RIGHT)

    # ========== توابع درخت ==========
    def get_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("هشدار", "لطفاً یک آیتم را انتخاب کنید.")
            return None
        return selected[0]

    def add_folder(self):
        parent = self.get_selected_item()
        if parent is None:
            return
        name = tk.simpledialog.askstring("افزودن پوشه", "نام پوشه:")
        if name:
            # بررسی تکراری نبودن
            children = self.tree.get_children(parent)
            for child in children:
                if self.tree.item(child, "text") == name:
                    messagebox.showerror("خطا", "آیتمی با این نام در این سطح وجود دارد.")
                    return
            new_id = self.tree.insert(parent, "end", text=name, values=("پوشه",))
            self.tree.selection_set(new_id)
            self.tree.focus(new_id)

    def add_file(self):
        parent = self.get_selected_item()
        if parent is None:
            return
        name = tk.simpledialog.askstring("افزودن فایل", "نام فایل (با پسوند):")
        if name:
            children = self.tree.get_children(parent)
            for child in children:
                if self.tree.item(child, "text") == name:
                    messagebox.showerror("خطا", "آیتمی با این نام در این سطح وجود دارد.")
                    return
            new_id = self.tree.insert(parent, "end", text=name, values=("فایل",))
            self.tree.selection_set(new_id)
            self.tree.focus(new_id)

    def delete_selected(self):
        selected = self.get_selected_item()
        if selected is None:
            return
        if messagebox.askyesno("تأیید حذف", "آیا از حذف این آیتم مطمئن هستید؟"):
            self.tree.delete(selected)

    def clear_tree(self):
        if messagebox.askyesno("تأیید پاک‌سازی", "همه‌ی آیتم‌های درخت حذف خواهند شد. ادامه می‌دهید؟"):
            for item in self.tree.get_children():
                self.tree.delete(item)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    # ========== ساختار از متن ==========
    def open_text_import(self):
        win = tk.Toplevel(self.root)
        win.title("وارد کردن ساختار از متن")
        win.geometry("600x500")

        ttk.Label(win, text="متن ساختار را با تورفتگی (چهار Space یا Tab) وارد کنید:").pack(pady=5)

        text_area = scrolledtext.ScrolledText(win, wrap=tk.NONE, width=70, height=20)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        text_area.insert(tk.END, """
پروژه/
    Agent/
        V1/
            main_agent.py
            router.py
            executor.py
            system_scan.py
            browser_tool.py
            file_tool.py
            code_agent.py
    Models/
        qwen2.5-1.5b.gguf
    Whisper/
        """)

        def parse_and_load():
            content = text_area.get("1.0", tk.END)
            self.populate_tree_from_text(content)
            win.destroy()

        ttk.Button(win, text="بارگذاری", command=parse_and_load).pack(pady=5)

    def populate_tree_from_text(self, text):
        """پارس کردن متن تورفتگی‌دار و پر کردن درخت"""
        # پاک کردن درخت فعلی
        for item in self.tree.get_children():
            self.tree.delete(item)

        lines = text.splitlines()
        # حذف خطوط خالی
        lines = [line for line in lines if line.strip()]
        if not lines:
            return

        # تشخیص کاراکتر تورفتگی (چهار فاصله یا تب)
        # فرض می‌کنیم اولین خط تورفتگی ندارد
        # اما ممکن است همه خطوط تورفتگی داشته باشند؟ پس ریشه را به عنوان یک پوشه فرض می‌کنیم.
        # بهتر است یک ریشه مجازی بسازیم.
        root_id = self.tree.insert("", "end", text="ریشه", values=("پوشه",), open=True)
        stack = [(root_id, 0)]  # (آی‌دی گره, سطح تورفتگی)

        for line in lines:
            stripped = line.rstrip()
            if not stripped:
                continue
            # شمارش تورفتگی (تعداد فاصله‌های ابتدایی)
            indent = len(line) - len(line.lstrip())
            # اگر تب بود، هر تب را معادل ۴ فاصله در نظر می‌گیریم (اختیاری)
            # برای سادگی، فرض می‌کنیم تورفتگی با فاصله است.
            # اما اگر تب داشت، می‌توانیم جایگزین کنیم.
            line_for_count = line.replace("\t", "    ")
            indent = len(line_for_count) - len(line_for_count.lstrip())

            # تعیین نوع: اگر به "/" ختم شود، پوشه است
            is_folder = stripped.endswith("/")
            name = stripped.rstrip("/").strip()
            if not name:
                continue

            # پیدا کردن والد مناسب با توجه به تورفتگی
            while stack and stack[-1][1] >= indent:
                stack.pop()
            if not stack:
                # اگر هیچ پدری وجود نداشت، به ریشه متصل می‌کنیم
                parent_id = root_id
            else:
                parent_id = stack[-1][0]

            # اضافه کردن گره
            item_type = "پوشه" if is_folder else "فایل"
            new_id = self.tree.insert(parent_id, "end", text=name, values=(item_type,))
            # اگر پوشه است، به استک اضافه می‌کنیم تا فرزندان بعدی زیر آن قرار گیرند
            if is_folder:
                stack.append((new_id, indent))
            # اگر فایل است، استک را تغییر نمی‌دهیم (همان پدر حفظ می‌شود)

        # باز کردن گره ریشه
        self.tree.item(root_id, open=True)

    # ========== ساخت در دیسک ==========
    def build_structure(self):
        base = self.base_path.get().strip()
        if not base:
            messagebox.showerror("خطا", "لطفاً مسیر پایه را وارد کنید.")
            return
        if not os.path.exists(base):
            try:
                os.makedirs(base)
            except Exception as e:
                messagebox.showerror("خطا", f"نمی‌توان مسیر پایه را ایجاد کرد:\n{e}")
                return

        # تابع بازگشتی برای ایجاد
        def create_items(parent_id, current_path):
            for child_id in self.tree.get_children(parent_id):
                name = self.tree.item(child_id, "text")
                item_type = self.tree.item(child_id, "values")[0]
                full_path = os.path.join(current_path, name)
                if item_type == "پوشه":
                    try:
                        os.makedirs(full_path, exist_ok=True)
                    except Exception as e:
                        messagebox.showerror("خطا", f"خطا در ایجاد پوشه {full_path}:\n{e}")
                        return
                    create_items(child_id, full_path)
                else:  # فایل
                    try:
                        # ایجاد فایل خالی
                        with open(full_path, 'w') as f:
                            pass
                    except Exception as e:
                        messagebox.showerror("خطا", f"خطا در ایجاد فایل {full_path}:\n{e}")
                        return

        # ریشه‌ی درخت (آیتم اول)
        roots = self.tree.get_children()
        if not roots:
            messagebox.showwarning("هشدار", "هیچ آیتمی برای ساخت وجود ندارد.")
            return
        # معمولاً یک ریشه مجازی داریم، اما ممکن است کاربر آن را حذف کرده باشد.
        # برای سادگی، همه‌ی گره‌های سطح اول را به‌عنوان پوشه‌های اصلی در مسیر پایه می‌سازیم.
        for root_id in roots:
            # اگر خود ریشه یک پوشه است (معمولاً)، آن را در base ایجاد می‌کنیم
            root_name = self.tree.item(root_id, "text")
            root_type = self.tree.item(root_id, "values")[0]
            if root_type == "پوشه":
                root_path = os.path.join(base, root_name)
                try:
                    os.makedirs(root_path, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("خطا", f"خطا در ایجاد پوشه اصلی {root_path}:\n{e}")
                    return
                create_items(root_id, root_path)
            else:
                # اگر ریشه فایل باشد، آن را مستقیماً در base ایجاد می‌کنیم (معمولاً نادرست)
                file_path = os.path.join(base, root_name)
                try:
                    with open(file_path, 'w') as f:
                        pass
                except Exception as e:
                    messagebox.showerror("خطا", f"خطا در ایجاد فایل {file_path}:\n{e}")
                    return

        messagebox.showinfo("موفقیت", "ساختار با موفقیت در مسیر مشخص ایجاد شد.")

    def select_path(self):
        path = filedialog.askdirectory(title="انتخاب مسیر پایه")
        if path:
            self.base_path.set(path)


if __name__ == "__main__":
    root = tk.Tk()
    app = StructureBuilder(root)
    root.mainloop()