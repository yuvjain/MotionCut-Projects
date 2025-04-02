import random
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CoinTossSimulator:
    def __init__(self):
        # Initialize session history
        self.session_history = []
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Virtual Coin Toss Simulator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Create frames
        self.input_frame = ttk.Frame(self.root, padding="10")
        self.input_frame.pack(fill=tk.X)
        
        self.result_frame = ttk.Frame(self.root, padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_frame = ttk.Frame(self.root, padding="10")
        self.history_frame.pack(fill=tk.X)
        
        # Input section
        ttk.Label(self.input_frame, text="Number of flips:").grid(row=0, column=0, padx=5, pady=5)
        self.flips_var = tk.StringVar()
        self.flips_entry = ttk.Entry(self.input_frame, textvariable=self.flips_var)
        self.flips_entry.grid(row=0, column=1, padx=5, pady=5)
        self.flips_entry.insert(0, "10")
        
        self.toss_button = ttk.Button(self.input_frame, text="Toss Coins", command=self.perform_tosses)
        self.toss_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.clear_button = ttk.Button(self.input_frame, text="Clear History", command=self.clear_history)
        self.clear_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Results section
        self.result_text = tk.Text(self.result_frame, height=10, width=40)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(self.result_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # History section
        ttk.Label(self.history_frame, text="Session History:").pack(anchor=tk.W)
        self.history_text = tk.Text(self.history_frame, height=5, width=40)
        self.history_text.pack(fill=tk.X)
        
        # Prepare for plotting
        self.fig = plt.Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.result_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_packed = False
        
        # Start the main loop
        self.root.mainloop()
    
    def coin_toss(self):
        """Simulates a single coin toss and returns 'Heads' or 'Tails'"""
        return random.choice(['Heads', 'Tails'])
    
    def perform_tosses(self):
        """Performs coin tosses based on user input and displays results"""
        try:
            num_flips = int(self.flips_var.get())
            if num_flips <= 0:
                messagebox.showerror("Error", "Please enter a positive number.")
                return
                
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Perform the coin tosses
            heads_count = 0
            tails_count = 0
            results = []
            
            self.result_text.insert(tk.END, "Flipping the coin...\n\n")
            
            for i in range(num_flips):
                result = self.coin_toss()
                results.append(result)
                if result == 'Heads':
                    heads_count += 1
                else:
                    tails_count += 1
                self.result_text.insert(tk.END, f"Flip {i+1}: {result}\n")
            
            # Display the summary
            heads_percent = (heads_count/num_flips)*100
            tails_percent = (tails_count/num_flips)*100
            
            summary = f"\nResults Summary:\n"
            summary += f"Total Flips: {num_flips}\n"
            summary += f"Heads: {heads_count} ({heads_percent:.2f}%)\n"
            summary += f"Tails: {tails_count} ({tails_percent:.2f}%)\n"
            
            self.result_text.insert(tk.END, summary)
            
            # Add to session history
            self.session_history.append({
                'flips': num_flips,
                'heads': heads_count,
                'tails': tails_count
            })
            self.update_history()
            
            # Update the visualization
            self.update_visualization(heads_count, tails_count)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
    
    def update_history(self):
        """Updates the history display with session information"""
        self.history_text.delete(1.0, tk.END)
        
        for i, session in enumerate(self.session_history):
            self.history_text.insert(tk.END, f"Session {i+1}: {session['flips']} flips - "
                                            f"Heads: {session['heads']} ({session['heads']/session['flips']*100:.2f}%), "
                                            f"Tails: {session['tails']} ({session['tails']/session['flips']*100:.2f}%)\n")
    
    def clear_history(self):
        """Clears the session history"""
        self.session_history = []
        self.history_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        if self.canvas_packed:
            self.canvas_widget.pack_forget()
            self.canvas_packed = False
    
    def update_visualization(self, heads, tails):
        """Updates the graphical representation of results"""
        # Clear previous plot
        self.fig.clear()
        
        # Create two subplots
        ax1 = self.fig.add_subplot(121)  # Pie chart
        ax2 = self.fig.add_subplot(122)  # Bar chart
        
        # Data
        labels = ['Heads', 'Tails']
        sizes = [heads, tails]
        colors = ['#ff9999', '#66b3ff']
        
        # Pie chart
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title('Coin Toss Results')
        
        # Bar chart
        ax2.bar(labels, sizes, color=colors)
        ax2.set_ylabel('Count')
        ax2.set_title('Heads vs Tails')
        
        # Add to display if not already there
        if not self.canvas_packed:
            self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.canvas_packed = True
            
        self.canvas.draw()


def main():
    """Main function to run the program"""
    try:
        import tkinter
        import matplotlib
        print("Starting graphical interface...")
        CoinTossSimulator()
    except ImportError:
        print("Required libraries not available, running console version...")
        session_history = []
        continue_simulation = True
        while continue_simulation:
            continue_simulation = run_simulation(session_history)


if __name__ == "__main__":
    main()