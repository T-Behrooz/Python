import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import win32api  # For getting drive letters on Windows

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Search and Move Tool")
        self.root.geometry("800x600")
        
        # Initialize variables first
        self.selected_extensions = []
        self.selected_drives = []
        self.destination_folder = ""
        self.move_files = tk.BooleanVar(value=True)
        self.searching = False
        self.found_files = []
        self.drives = self.get_available_drives()  # Initialize drives before creating widgets
        
        # Then create UI
        self.create_widgets()
        
    def get_available_drives(self):
        """Get list of available drives on Windows"""
        drives = []
        try:
            drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        except:
            # Fallback for non-Windows or if win32api not available
            drives = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]
        return drives
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # File extensions frame
        ext_frame = ttk.LabelFrame(self.root, text="Select File Types", padding=10)
        ext_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.ext_listbox = tk.Listbox(ext_frame, selectmode=tk.MULTIPLE, height=6)
        self.ext_listbox.pack(fill=tk.X)
        
        common_exts = ['.pdf', '.docx', '.xlsx', '.jpg', '.png', '.mp3', '.mp4', '.txt']
        for ext in common_exts:
            self.ext_listbox.insert(tk.END, ext)
        
        # Add custom extension
        ext_control_frame = ttk.Frame(ext_frame)
        ext_control_frame.pack(fill=tk.X, pady=5)
        
        self.custom_ext = ttk.Entry(ext_control_frame, width=10)
        self.custom_ext.pack(side=tk.LEFT, padx=5)
        ttk.Button(ext_control_frame, text="Add", command=self.add_custom_extension).pack(side=tk.LEFT)
        
        # Drives frame
        drives_frame = ttk.LabelFrame(self.root, text="Select Drives to Search", padding=10)
        drives_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.drive_vars = []
        for i in range(0, len(self.drives), 3):
            row_frame = ttk.Frame(drives_frame)
            row_frame.pack(fill=tk.X)
            for drive in self.drives[i:i+3]:
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(row_frame, text=drive, variable=var)
                cb.pack(side=tk.LEFT, padx=10)
                self.drive_vars.append((drive, var))
        
        # Rest of the code remains the same...
        # Destination frame
        dest_frame = ttk.LabelFrame(self.root, text="Destination Folder", padding=10)
        dest_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(dest_frame, text="Select Destination", command=self.select_destination).pack(anchor=tk.W)
        self.dest_label = ttk.Label(dest_frame, text="No folder selected")
        self.dest_label.pack(anchor=tk.W)
        
        # Options frame
        options_frame = ttk.Frame(self.root)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Radiobutton(options_frame, text="Move Files", variable=self.move_files, value=True).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(options_frame, text="Copy Files", variable=self.move_files, value=False).pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Start Search", command=self.start_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop", command=self.stop_search).pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(anchor=tk.W)
        
        # Results treeview
        self.tree = ttk.Treeview(progress_frame, columns=('original', 'new'), show='headings')
        self.tree.heading('original', text='Original Path')
        self.tree.heading('new', text='New Path')
        self.tree.column('original', width=400)
        self.tree.column('new', width=400)
        
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    # Rest of the methods remain the same...
    def add_custom_extension(self):
        """Add user-specified file extension to the list"""
        ext = self.custom_ext.get().strip()
        if ext:
            if not ext.startswith('.'):
                ext = '.' + ext
            if ext not in self.ext_listbox.get(0, tk.END):
                self.ext_listbox.insert(tk.END, ext)
                self.custom_ext.delete(0, tk.END)
    
    def select_destination(self):
        """Let user select destination folder"""
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder = folder
            self.dest_label.config(text=folder)
    
    def start_search(self):
        """Start searching files in a separate thread"""
        if self.searching:
            return
            
        # Get selected extensions
        self.selected_extensions = [self.ext_listbox.get(i) for i in self.ext_listbox.curselection()]
        if not self.selected_extensions:
            messagebox.showwarning("Warning", "Please select at least one file type")
            return
            
        # Get selected drives
        self.selected_drives = [drive for drive, var in self.drive_vars if var.get()]
        if not self.selected_drives:
            messagebox.showwarning("Warning", "Please select at least one drive")
            return
            
        if not self.destination_folder:
            messagebox.showwarning("Warning", "Please select a destination folder")
            return
            
        # Clear previous results
        self.found_files = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Start search thread
        self.searching = True
        self.status_label.config(text="Searching...")
        Thread(target=self.search_files, daemon=True).start()
    
    def stop_search(self):
        """Stop the current search operation"""
        self.searching = False
        self.status_label.config(text="Search stopped by user")
    
    def search_files(self):
        """Search for files in selected drives with selected extensions"""
        try:
            # Prepare extensions for case-insensitive search
            extensions = [ext.lower() for ext in self.selected_extensions]
            
            # Walk through selected drives
            total_files = 0
            for drive in self.selected_drives:
                if not self.searching:
                    break
                    
                self.status_label.config(text=f"Searching {drive}...")
                self.root.update()
                
                for root, _, files in os.walk(drive):
                    if not self.searching:
                        break
                        
                    for file in files:
                        if not self.searching:
                            break
                            
                        # Check file extension
                        _, ext = os.path.splitext(file)
                        if ext.lower() in extensions:
                            src_path = os.path.join(root, file)
                            dest_path = os.path.join(self.destination_folder, file)
                            
                            # Handle duplicates
                            counter = 1
                            while os.path.exists(dest_path):
                                name, ext = os.path.splitext(file)
                                dest_path = os.path.join(self.destination_folder, f"{name}_{counter}{ext}")
                                counter += 1
                            
                            self.found_files.append((src_path, dest_path))
                            self.tree.insert('', tk.END, values=(src_path, dest_path))
                            total_files += 1
                            
                            # Update UI every 10 files
                            if total_files % 10 == 0:
                                self.status_label.config(text=f"Found {total_files} files...")
                                self.root.update()
            
            # Process found files
            if self.found_files and self.searching:
                self.status_label.config(text=f"Found {len(self.found_files)} files. Processing...")
                self.progress.config(maximum=len(self.found_files))
                
                for i, (src, dest) in enumerate(self.found_files):
                    if not self.searching:
                        break
                        
                    try:
                        if self.move_files.get():
                            shutil.move(src, dest)
                        else:
                            shutil.copy2(src, dest)
                    except Exception as e:
                        self.tree.item(self.tree.get_children()[i], tags=('error',))
                        self.tree.tag_configure('error', foreground='red')
                    
                    self.progress['value'] = i + 1
                    self.root.update()
                
                if self.searching:
                    self.status_label.config(text=f"Completed! Processed {len(self.found_files)} files")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.searching = False
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    app.run()