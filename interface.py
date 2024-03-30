import tkinter as tk
from tkinter import messagebox
from investment_manager import InvestmentManager  # Your existing code encapsulated in a class

class InvestmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Management")

        self.manager = InvestmentManager()

        self.create_widgets()

    def create_widgets(self):
        self.download_button = tk.Button(self.root, text="Start Over", command=self.start_over)
        self.download_button.pack(pady=10)
    
        self.download_button = tk.Button(self.root, text="Download Files", command=self.download_files)
        self.download_button.pack(pady=10)

        self.update_button = tk.Button(self.root, text="Update Portfolio", command=self.update_portfolio)
        self.update_button.pack(pady=10)

        self.sell_button = tk.Button(self.root, text="Sell", command=self.sell)
        self.sell_button.pack(pady=10)

        self.buy_button = tk.Button(self.root, text="Buy", command=self.buy)
        self.buy_button.pack(pady=10)
    
    def createsellwindow(self):
        self.root.destroy()
        
        root = tk.Tk()
        root.title("Sell")

        sell_date_label = tk.Label(root, text="Sell Date:")
        sell_date_label.grid(row=0, column=0)

        self.sell_date_entry = tk.Entry(root)
        self.sell_date_entry.grid(row=0, column=1)

        sell_yatırımAracı_label = tk.Label(root, text="Sell Yatırım Aracı:")
        sell_yatırımAracı_label.grid(row=1, column=0)

        self.sell_yatırımAracı_entry = tk.Entry(root)
        self.sell_yatırımAracı_entry.grid(row=1, column=1)

        sell_maaliyet_label = tk.Label(root, text="Sell Maaliyet:")
        sell_maaliyet_label.grid(row=2, column=0)

        self.sell_maaliyet_entry = tk.Entry(root)
        self.sell_maaliyet_entry.grid(row=2, column=1)

        sell_satis_label = tk.Label(root, text="Sell Satis:")
        sell_satis_label.grid(row=3, column=0)

        self.sell_satis_entry = tk.Entry(root)
        self.sell_satis_entry.grid(row=3, column=1)



        sell_day = tk.Label(root, text="Süre:")
        sell_day.grid(row=4, column=0)

        self.sell_day_entry = tk.Entry(root)
        self.sell_day_entry.grid(row=4, column=1)

        root.mainloop()

    def start_over(self):
        try:
            self.manager.start_over()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def download_files(self):
        try:
            self.manager.download_Fund_Info()
            messagebox.showinfo("Success", "Files downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_portfolio(self):
        #try:
        self.manager.start_update()
        messagebox.showinfo("Success", "Portfolio updated successfully.")
        # except Exception as e:
        #     messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def sell(self):
        try:
            # Implement sell logic here
            self.createsellwindow()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def buy(self):
        try:
            # Implement buy logic here
            pass
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = InvestmentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
