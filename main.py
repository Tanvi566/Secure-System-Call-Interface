import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import os
import time
import shutil
import stat

# ---------------- THEME SETUP ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- PATH RESTRICTION (THE SANDBOX) ----------------
BASE_DIR = os.path.abspath("project_files")
os.makedirs(BASE_DIR, exist_ok=True) 

def get_safe_path(name, current_dir):
    path = os.path.abspath(os.path.join(current_dir, name))
    if not path.startswith(BASE_DIR):
        raise Exception("Security Alert: Sandbox escape attempt blocked!")
    return path

# ---------------- LOGIN ATTEMPTS ----------------
attempts_left = 5

# ---------------- REGISTER ----------------
def register_user():
    dialog_u = ctk.CTkInputDialog(text="Enter new Username:\n(Use 'admin' for superuser rights)", title="Register")
    username = dialog_u.get_input()
    if not username: return
    
    dialog_p = ctk.CTkInputDialog(text="Enter new Password:", title="Register")
    password = dialog_p.get_input()
    if not password: return

    try:
        with open("users.txt", "r") as f:
            for line in f:
                u, _ = line.strip().split(",")
                if u == username:
                    result_label.configure(text="User already exists!", text_color="#ef4444")
                    return
    except:
        pass

    with open("users.txt", "a") as f:
        f.write(f"\n{username},{password}")

    result_label.configure(text="Account created successfully!", text_color="#4ade80")

# ---------------- LOGGING ----------------
def log_action(user, action):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} - {user}: {action}\n")

# ---------------- LOGIN LOGIC ----------------
def check_login():
    global attempts_left

    u = username_entry.get()
    p = password_entry.get()

    try:
        with open("users.txt", "r") as f:
            for line in f:
                if not line.strip(): continue
                user, pw = line.strip().split(",")
                if u == user and p == pw:
                    result_label.configure(text="Login Successful", text_color="#4ade80")
                    root.withdraw() 
                    open_dashboard(u)
                    return

        attempts_left -= 1
        result_label.configure(text=f"Wrong credentials! Attempts left: {attempts_left}", text_color="#f87171")

        if attempts_left <= 0:
            result_label.configure(text="SYSTEM LOCKED.", text_color="#ef4444")
            root.after(1000, root.destroy)

    except FileNotFoundError:
        result_label.configure(text="System error: No users registered yet.", text_color="#f87171")

# ---------------- DASHBOARD ----------------
def open_dashboard(user):
    password_entry.delete(0, "end")
    result_label.configure(text="") 

    dash = ctk.CTkToplevel(root)
    dash.title("SecureSys - Terminal")
    dash.geometry("1100x750") # Slightly taller to fit the new button
    dash.configure(fg_color="#09090b") 

    def on_closing():
        root.destroy()
    dash.protocol("WM_DELETE_WINDOW", on_closing)

    # ---- SYSTEM STATE ----
    current_dir = BASE_DIR
    role = "SUPERUSER" if user == "admin" else "USER"

    # ---- IDLE TIMER LOGIC ----
    last_activity = time.time()
    IDLE_TIMEOUT = 120 

    def reset_idle_timer(event=None):
        nonlocal last_activity
        last_activity = time.time()

    dash.bind("<Motion>", reset_idle_timer)
    dash.bind("<Key>", reset_idle_timer)

    def check_idle():
        if time.time() - last_activity >= IDLE_TIMEOUT:
            log_action(user, "Auto-logged out due to inactivity")
            messagebox.showwarning("Session Expired", "You have been logged out due to 2 minutes of inactivity.")
            logout()
        else:
            dash.after(1000, check_idle)

    check_idle() 

    # ---- TOP NAVBAR ----
    navbar = ctk.CTkFrame(dash, height=60, fg_color="#18181b", border_color="#27272a", border_width=1, corner_radius=0)
    navbar.pack(side="top", fill="x")
    navbar.pack_propagate(False)

    ctk.CTkLabel(navbar, text="🛡️ SecureSys", font=("Roboto", 20, "bold"), text_color="white").pack(side="left", padx=20)
    
    start_time = time.time()
    timer_label = ctk.CTkLabel(navbar, text="Session: 0s", font=("Consolas", 14, "bold"), text_color="#38bdf8")
    timer_label.pack(side="left", padx=40)

    def update_timer():
        if not dash.winfo_exists(): return 
        t = int(time.time() - start_time)
        mins, secs = divmod(t, 60)
        timer_label.configure(text=f"Session Time: {mins:02d}:{secs:02d}")
        dash.after(1000, update_timer)

    update_timer()

    user_frame = ctk.CTkFrame(navbar, fg_color="transparent")
    user_frame.pack(side="right", padx=20, pady=10)
    ctk.CTkLabel(user_frame, text=f"User: {user} | Role: {role}", font=("Consolas", 12), text_color="#a1a1aa").pack(side="left", padx=15)
    
    def logout():
        log_action(user, "User logged out")
        dash.destroy()       
        root.deiconify()     
        
    ctk.CTkButton(user_frame, text="[→ Logout", width=80, height=30, fg_color="transparent", border_width=1, border_color="#ef4444", text_color="#ef4444", hover_color="#7f1d1d", command=logout).pack(side="left")

    # ---- LEFT SIDEBAR ----
    sidebar = ctk.CTkFrame(dash, width=230, fg_color="#18181b", border_color="#27272a", border_width=1, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(sidebar, text="QUICK COMMANDS", font=("Roboto", 10, "bold"), text_color="#71717a").pack(anchor="w", padx=20, pady=(20, 10))

    # ---- MAIN TERMINAL AREA ----
    main_area = ctk.CTkFrame(dash, fg_color="#09090b", corner_radius=0)
    main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    terminal_box = ctk.CTkFrame(main_area, fg_color="#050505", border_color="#27272a", border_width=1, corner_radius=10)
    terminal_box.pack(fill="both", expand=True)

    win_controls = ctk.CTkFrame(terminal_box, fg_color="transparent", height=30)
    win_controls.pack(fill="x", padx=15, pady=10)
    ctk.CTkLabel(win_controls, text="🔴 🟡 🟢", font=("Arial", 14)).pack(side="left")
    ctk.CTkLabel(win_controls, text="Terminal — System Shell", font=("Consolas", 12), text_color="#52525b").pack(side="left", padx=15)

    term_output = ctk.CTkTextbox(terminal_box, font=("Consolas", 13), fg_color="transparent", text_color="#d4d4d8", wrap="word", border_width=0)
    term_output.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    term_output.tag_config("system", foreground="#f59e0b")
    term_output.tag_config("cmd", foreground="#38bdf8")
    term_output.tag_config("success", foreground="#4ade80")
    term_output.tag_config("error", foreground="#ef4444")

    term_output.insert("end", f"Login successful at {datetime.now().strftime('%H:%M:%S')}\nType a command or use the sidebar shortcuts to interact with the file system.\n\n", "system")
    term_output.configure(state="disabled")

    def print_to_term(cmd, msg, tag="success"):
        term_output.configure(state="normal")
        rel_path = os.path.relpath(current_dir, BASE_DIR)
        display_path = "~" if rel_path == "." else f"~/{rel_path.replace(os.sep, '/')}"
        
        term_output.insert("end", f"[{user}@securesys {display_path}]$ {cmd}\n", "cmd")
        term_output.insert("end", f"{msg}\n\n", tag)
        term_output.see("end")
        term_output.configure(state="disabled")

    def term_error(cmd, msg):
        print_to_term(cmd, f"Permission/System Error: {msg}", "error")

    # -----------------------------------------------
    def ask_large_content(title_text):
        dialog = ctk.CTkToplevel(dash)
        dialog.title(title_text)
        dialog.geometry("500x400")
        dialog.configure(fg_color="#09090b")
        dialog.transient(dash) 
        dialog.grab_set() 

        ctk.CTkLabel(dialog, text="Enter file data:", font=("Consolas", 14, "bold"), text_color="white").pack(pady=(15, 5))
        
        textbox = ctk.CTkTextbox(dialog, width=450, height=250, corner_radius=5, fg_color="#050505", border_color="#27272a", border_width=1, font=("Consolas", 12))
        textbox.pack(padx=10, pady=10)

        result = [None]
        def save():
            result[0] = textbox.get("0.0", "end-1c")
            dialog.destroy()

        ctk.CTkButton(dialog, text="Save (Ctrl+S)", command=save, fg_color="#3b82f6", hover_color="#2563eb", font=("Consolas", 12)).pack(pady=10)
        dialog.wait_window()
        return result[0]

    # -------- DIRECTORY NAVIGATION --------
    def print_working_dir():
        log_action(user, "Executed 'pwd'")
        print_to_term("pwd", current_dir, "success")

    def change_dir():
        nonlocal current_dir
        name = ctk.CTkInputDialog(text="Enter folder name to enter:", title="cd").get_input()
        if name:
            try:
                target = get_safe_path(name, current_dir)
                if os.path.isdir(target):
                    current_dir = target
                    log_action(user, f"Moved into directory {name}")
                    print_to_term(f"cd {name}", f"Changed directory.", "success")
                else:
                    term_error(f"cd {name}", "Not a valid directory.")
            except Exception as e:
                term_error(f"cd {name}", str(e))

    def go_up_dir():
        nonlocal current_dir
        if current_dir == BASE_DIR:
            term_error("cd ..", "Sandbox restriction: Cannot navigate above the root project directory.")
            return

        try:
            target = get_safe_path("..", current_dir)
            current_dir = target
            print_to_term("cd ..", "Moved up one directory level.", "success")
        except Exception as e:
            term_error("cd ..", str(e))

    # -------- FILE FUNCTIONS --------
    def list_files():
        try:
            files = os.listdir(current_dir)
            output = ""
            if files:
                for file in files:
                    if os.path.isdir(os.path.join(current_dir, file)):
                        output += f"d-rwxr-xr-x  1 {user}  admin  4096  {file}/\n"
                    else:
                        output += f"-rwxr-xr-x  1 {user}  admin     0  {file}\n"
            else:
                output = "Directory is empty."
            
            log_action(user, "Executed 'ls'")
            print_to_term("ls -l", output.strip(), "success")
        except Exception as e:
            term_error("ls -l", str(e))

    # ---- NEW TREE FUNCTION ----
    def show_tree():
        try:
            log_action(user, "Executed 'tree'")
            
            # Start the output with the name of the current folder
            folder_name = os.path.basename(current_dir)
            if not folder_name: folder_name = "project_files"
            tree_output = f"{folder_name}/\n"
            
            # Recursive function to build the tree drawing
            def build_tree(path, prefix=""):
                output = ""
                try:
                    items = sorted(os.listdir(path))
                except Exception:
                    return ""
                
                for i, item in enumerate(items):
                    item_path = os.path.join(path, item)
                    is_last = (i == len(items) - 1)
                    
                    if is_last:
                        output += f"{prefix}└── {item}\n"
                        new_prefix = prefix + "    "
                    else:
                        output += f"{prefix}├── {item}\n"
                        new_prefix = prefix + "│   "
                        
                    # If it's a folder, dive inside it!
                    if os.path.isdir(item_path):
                        output += build_tree(item_path, new_prefix)
                return output
                
            tree_output += build_tree(current_dir)
            
            if tree_output.strip() == f"{folder_name}/":
                tree_output += "    (Empty Directory)"
                
            print_to_term("tree", tree_output.rstrip(), "success")
        except Exception as e:
            term_error("tree", str(e))
    # ---------------------------

    def create_file():
        name = ctk.CTkInputDialog(text="Enter filename:", title="touch").get_input()
        if name:
            try:
                open(get_safe_path(name, current_dir), "x").close()
                log_action(user, f"Created file {name}")
                print_to_term(f"touch {name}", "File created successfully.", "success")
            except Exception as e:
                term_error(f"touch {name}", str(e))

    def read_file():
        name = ctk.CTkInputDialog(text="Enter filename:", title="cat").get_input()
        if name:
            try:
                content = open(get_safe_path(name, current_dir)).read()
                win = ctk.CTkToplevel(dash)
                win.title(f"cat {name}")
                win.geometry("550x400")
                win.configure(fg_color="#09090b")
                win.transient(dash)
                win.grab_set()
                
                textbox = ctk.CTkTextbox(master=win, width=530, height=380, corner_radius=5, fg_color="#050505", text_color="white", font=("Consolas", 12))
                textbox.pack(padx=10, pady=10)
                textbox.insert("0.0", content)
                textbox.configure(state="disabled")

                log_action(user, f"Read file {name}")
                print_to_term(f"cat {name}", "File opened in viewer.", "success")
            except Exception as e:
                term_error(f"cat {name}", str(e))

    def write_file():
        name = ctk.CTkInputDialog(text="Enter filename:", title="echo").get_input()
        if name:
            content = ask_large_content(f"echo > {name}") 
            if content is not None:
                try:
                    open(get_safe_path(name, current_dir), "w").write(content)
                    log_action(user, f"Wrote file {name}")
                    print_to_term(f"echo '...' > {name}", "Data written to file.", "success")
                except Exception as e:
                    term_error(f"echo > {name}", str(e))

    def rename_file():
        old_name = ctk.CTkInputDialog(text="Enter current filename:", title="mv (Rename)").get_input()
        if old_name:
            new_name = ctk.CTkInputDialog(text="Enter NEW filename:", title="mv (Rename)").get_input()
            if new_name:
                try:
                    old_path = get_safe_path(old_name, current_dir)
                    new_path = get_safe_path(new_name, current_dir)
                    os.rename(old_path, new_path)
                    log_action(user, f"Renamed {old_name} to {new_name}")
                    print_to_term(f"mv {old_name} {new_name}", "File renamed successfully.", "success")
                except Exception as e:
                    term_error(f"mv {old_name} {new_name}", str(e))

    def create_folder():
        nonlocal current_dir
        name = ctk.CTkInputDialog(text="Enter folder name:", title="mkdir").get_input()
        if name:
            try:
                new_path = get_safe_path(name, current_dir)
                os.makedirs(new_path)
                log_action(user, f"Created folder {name}")
                current_dir = new_path
                print_to_term(f"mkdir {name}", f"Directory created.\nAutomatically moved into ~/{name}.", "success")
            except Exception as e:
                term_error(f"mkdir {name}", str(e))

    # ---- ADMIN ONLY DELETE FUNCTIONS ----
    def delete_file():
        if user != "admin":
            term_error("rm", "Access Denied. Only 'admin' has delete privileges.")
            return

        name = ctk.CTkInputDialog(text="Enter filename to delete:", title="rm").get_input()
        if name:
            try:
                target_path = get_safe_path(name, current_dir)
                if not os.access(target_path, os.W_OK):
                    os.chmod(target_path, stat.S_IWRITE)
                
                os.remove(target_path)
                log_action(user, f"Deleted file {name}")
                print_to_term(f"rm {name}", "File removed permanently.", "system")
            except Exception as e:
                term_error(f"rm {name}", str(e))

    def delete_folder():
        if user != "admin":
            term_error("rmdir", "Access Denied. Only 'admin' has delete privileges.")
            return

        name = ctk.CTkInputDialog(text="Enter folder to delete:", title="rmdir").get_input()
        if name:
            try:
                target_path = get_safe_path(name, current_dir)
                if os.path.isdir(target_path):
                    def force_remove(func, path, excinfo):
                        os.chmod(path, stat.S_IWRITE)
                        func(path)

                    shutil.rmtree(target_path, onerror=force_remove)  
                    log_action(user, f"Deleted folder {name}")
                    print_to_term(f"rmdir {name}", "Directory and all contents removed permanently.", "system")
                else:
                    term_error(f"rmdir {name}", f"'{name}' is not a directory.")
            except Exception as e:
                term_error(f"rmdir {name}", str(e))

    def view_logs():
        win = ctk.CTkToplevel(dash)
        win.title("tail -f logs.txt")
        win.geometry("600x450")
        win.configure(fg_color="#09090b")
        win.transient(dash)
        win.grab_set()

        textbox = ctk.CTkTextbox(master=win, width=580, height=350, corner_radius=5, fg_color="#050505", text_color="#a855f7", font=("Consolas", 12))
        textbox.pack(padx=10, pady=10)

        try:
            textbox.insert("0.0", open("logs.txt").read())
        except:
            textbox.insert("0.0", "No logs found.")
        textbox.configure(state="disabled")

        def clear():
            if user != "admin":
                messagebox.showerror("Denied", "Only admin can clear server logs.")
                return
            open("logs.txt", "w").close()
            textbox.configure(state="normal")
            textbox.delete("0.0", "end")
            textbox.configure(state="disabled")
            print_to_term("rm logs.txt", "Logs cleared from system.", "system")

        ctk.CTkButton(master=win, text="Clear Logs (Admin)", fg_color="transparent", border_color="#ef4444", border_width=1, hover_color="#7f1d1d", command=clear).pack(pady=10)

    def system_info():
        import platform
        info = f"OS: {platform.system()}\nPython: {platform.python_version()}"
        print_to_term("uname -a", info, "system")

    def change_password():
        new = ctk.CTkInputDialog(text="Enter new password:", title="passwd").get_input()
        if new:
            lines = []
            try:
                for line in open("users.txt"):
                    user_id, pw = line.strip().split(",")
                    if user_id == user:
                        lines.append(f"{user_id},{new}\n")
                    else:
                        lines.append(line)
                open("users.txt", "w").writelines(lines)
                log_action(user, "Password changed")
                print_to_term("passwd", "Password updated successfully.", "success")
            except Exception as e:
                term_error("passwd", str(e))

    # -------- SIDEBAR BUTTONS --------
    buttons = [
        ("📄 ls (List Files)", list_files),
        ("🌳 tree (Show Tree)", show_tree),        # <--- NEW TREE BUTTON
        ("📍 pwd (Print Dir)", print_working_dir), 
        ("📁 cd (Enter Dir)", change_dir),
        ("🔙 cd .. (Go Up)", go_up_dir),
        ("📝 touch (Create File)", create_file),
        ("🐱 cat (Read File)", read_file),
        ("📉 echo (Write File)", write_file),
        ("📥 mv (Rename File)", rename_file), 
        ("📁 mkdir (New Dir)", create_folder),
        ("✂️ rm (Del File)", delete_file),     
        ("✂️ rmdir (Del Dir)", delete_folder),  
        ("📜 tail (Logs)", view_logs),
        ("💻 uname (Sys Info)", system_info),
        ("🔑 passwd (Change Pass)", change_password),
    ]

    for text, cmd in buttons:
        btn = ctk.CTkButton(master=sidebar, text=text, command=cmd, 
                            fg_color="transparent", hover_color="#27272a", anchor="w",
                            text_color="#d4d4d8", width=190, height=26, corner_radius=6, font=("Consolas", 12))
        btn.pack(pady=2, padx=20)


# ---------------- LOGIN UI ----------------
root = ctk.CTk()
root.title("Secure Dashboard - Login")
root.geometry("800x700") 
root.configure(fg_color="#09090b") 

frame = ctk.CTkFrame(master=root, width=500, height=560, corner_radius=20, fg_color="#18181b", border_color="#27272a", border_width=1)
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.pack_propagate(False) 

header_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
header_frame.pack(fill="x", pady=(35, 20))

ctk.CTkLabel(master=header_frame, text="🛡️", font=("Roboto", 45), text_color="#3b82f6").pack(anchor="center")
ctk.CTkLabel(master=header_frame, text="Secure Dashboard", font=("Roboto", 24, "bold"), text_color="white").pack(anchor="center", pady=(5, 5))
ctk.CTkLabel(master=header_frame, text="Sign in to access your system terminal", font=("Roboto", 13), text_color="#a1a1aa").pack(anchor="center")

form_wrapper = ctk.CTkFrame(master=frame, fg_color="transparent")
form_wrapper.pack(fill="x", padx=65) 

ctk.CTkLabel(master=form_wrapper, text="USERNAME", font=("Roboto", 10, "bold"), text_color="#71717a").pack(anchor="w", pady=(0, 2))
username_entry = ctk.CTkEntry(master=form_wrapper, placeholder_text="Enter username", height=45, corner_radius=8, border_width=1, border_color="#3f3f46", fg_color="#09090b", text_color="white")
username_entry.pack(fill="x", pady=(0, 20))

ctk.CTkLabel(master=form_wrapper, text="PASSWORD", font=("Roboto", 10, "bold"), text_color="#71717a").pack(anchor="w", pady=(0, 2))
password_entry = ctk.CTkEntry(master=form_wrapper, placeholder_text="Enter password", show="•", height=45, corner_radius=8, border_width=1, border_color="#3f3f46", fg_color="#09090b", text_color="white")
password_entry.pack(fill="x", pady=(0, 30))

login_btn = ctk.CTkButton(master=form_wrapper, text="Sign In →", command=check_login, fg_color="#8b5cf6", hover_color="#7c3aed", height=45, corner_radius=8, font=("Roboto", 14, "bold"))
login_btn.pack(fill="x", pady=(0, 15))

register_btn = ctk.CTkButton(master=form_wrapper, text="Sign Up", command=register_user, fg_color="transparent", hover_color="#27272a", text_color="#a1a1aa", height=35, corner_radius=8, font=("Roboto", 12))
register_btn.pack(fill="x")

result_label = ctk.CTkLabel(master=frame, text="", text_color="white", font=("Roboto", 12))
result_label.pack(pady=(15, 0))

root.mainloop()