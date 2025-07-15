import tkinter as tk
import threading

def create_gui_start_stop_buttons(start_callback, stop_callback):
    """
    Create a window with both start and stop buttons for controlling the surveillance.
    """
    def update_status_label(status):
        # Safely update the status label using after() method
        root.after(0, status_label.config, {'text': status})

    def start_surveillance():
        update_status_label("Camera starting in a few seconds...")
        start_button.config(state=tk.DISABLED)
        root.after(2000, start_surveillance_logic)  # Add a delay before starting

    def start_surveillance_logic():
        update_status_label("Surveillance started.")
        start_callback()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

    def stop_surveillance_func():
        update_status_label("Surveillance stopped.")
        stop_callback()
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("Surveillance System")
    root.geometry("400x300")

    # Status label
    status_label = tk.Label(root, text="Surveillance is not running", font=('Helvetica', 12))
    status_label.pack(pady=10)

    # Start button (Green)
    start_button = tk.Button(root, text="Start Surveillance", command=lambda: threading.Thread(target=start_surveillance, daemon=True).start(),
                             bg="green", fg="white", font=('Helvetica', 12), width=20, height=2)
    start_button.pack(pady=10)

    # Stop button (Red)
    stop_button = tk.Button(root, text="Stop Surveillance", command=stop_surveillance_func, state=tk.DISABLED,
                            bg="red", fg="white", font=('Helvetica', 12), width=20, height=2)
    stop_button.pack(pady=10)

    # Run the GUI
    root.mainloop()
