from tkinter import messagebox
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame
import db
from track_main import ExpenseTrackerClass

class LoginRegisterClass(CTk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Management")
        self.geometry("600x450")
        self.current_user_id = None
        
        self.configure(bg_color="#2E4053") 

        self.create_widgets()

    def create_widgets(self):
        # Welcome label
        self.label = CTkLabel(self, text="Welcome to Personal Finance Management",
                              font=("Courier New", 22, "bold"), text_color="#F7DC6F")  # Gold text color
        self.label.pack(pady=20)

        # Frame for input fields
        self.frame_input = CTkFrame(self, fg_color="#34495E", corner_radius=10)  # Slightly lighter blue-gray frame
        self.frame_input.pack(pady=20, padx=20)

        # Username label and entry
        self.username_label = CTkLabel(self.frame_input, text="Username:", font=("Courier New", 14), text_color="#ECF0F1")  # Light gray text
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = CTkEntry(self.frame_input, font=("Courier New", 14), width=150, fg_color="#D5D8DC", text_color="#000000")  # Light gray entry background
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password label and entry
        self.password_label = CTkLabel(self.frame_input, text="Password:", font=("Courier New", 14), text_color="#ECF0F1")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = CTkEntry(self.frame_input, font=("Courier New", 14), width=150, show="*", fg_color="#D5D8DC", text_color="#000000")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Login button
        self.login_button = CTkButton(self, text="Login", command=self.login_user, font=("Courier New", 14),
                                      height=32, width=100, corner_radius=10, fg_color="#27AE60", text_color="#FFFFFF")  # Green button
        self.login_button.pack(pady=(10, 5))

        # "or" label
        self.or_label = CTkLabel(self, text="or", font=("Courier New", 14), text_color="#FFFFFF")  # White text
        self.or_label.pack()

        # Register button
        self.register_button = CTkButton(self, text="Register", command=self.register_user, font=("Courier New", 14),
                                         height=32, width=100, corner_radius=10, fg_color="#2980B9", text_color="#FFFFFF")  # Blue button
        self.register_button.pack(pady=(5, 20))


    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            conn, cursor = db.connect_to_database()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showwarning("Warning", "Username already exists. Please choose a different username.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Warning", "Please enter both username and password.")

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            conn, cursor = db.connect_to_database()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            if user:
                self.current_user_id = user[0]
                self.load_expenses()  # Load expenses for the current user
                self.create_expense_tracker()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showwarning("Warning", "Please enter both username and password.")

    def load_expenses(self):
        conn, cursor = db.connect_to_database()
        cursor.execute("SELECT amount, description, category, date FROM expenses WHERE user_id=?", (self.current_user_id,))
        self.expenses = cursor.fetchall()
        conn.close()

    def create_expense_tracker(self):
        self.withdraw()  # Hide login window
        expense_tracker = ExpenseTrackerClass(current_user_id=self.current_user_id)
        expense_tracker.mainloop()

if __name__ == "__main__":
    app = LoginRegisterClass()
    app.mainloop()
