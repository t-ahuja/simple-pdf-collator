import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from pypdf import PdfMerger
import os


class PDFCollator:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 PDF Collator - Merge & Rearrange")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Modern color palette
        self.bg_dark = "#1a1a2e"
        self.bg_medium = "#16213e"
        self.bg_light = "#0f3460"
        self.accent_purple = "#e94560"
        self.accent_blue = "#00d4ff"
        self.accent_green = "#00ff88"
        self.text_light = "#ffffff"
        self.text_muted = "#b0b0b0"
        self.hover_purple = "#ff5370"
        
        # Configure root background
        self.root.configure(bg=self.bg_dark)
        
        self.pdf_files = []
        self.drag_index = None
        
        # Main container
        main_container = tk.Frame(root, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title section
        title_frame = tk.Frame(main_container, bg=self.bg_dark)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="📄 PDF COLLATOR",
            font=("Segoe UI", 24, "bold"),
            fg=self.accent_blue,
            bg=self.bg_dark
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Drag, drop & merge your PDFs effortlessly",
            font=("Segoe UI", 10),
            fg=self.text_muted,
            bg=self.bg_dark
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Action buttons frame
        button_frame = tk.Frame(main_container, bg=self.bg_dark)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Add PDF button
        self.add_button = self.create_modern_button(
            button_frame, "➕ Add PDFs", self.add_pdfs, self.accent_blue
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Clear button
        self.clear_button = self.create_modern_button(
            button_frame, "🗑️ Clear All", self.clear_all, "#ff6b6b"
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Merge button
        self.merge_button = self.create_modern_button(
            button_frame, "✨ Merge PDFs", self.merge_pdfs, self.accent_green
        )
        self.merge_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # PDF list container with modern styling
        list_container = tk.Frame(main_container, bg=self.bg_medium, relief=tk.FLAT, bd=0)
        list_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Listbox header
        header_frame = tk.Frame(list_container, bg=self.bg_light, height=40)
        header_frame.pack(fill=tk.X, padx=2, pady=(2, 0))
        
        header_label = tk.Label(
            header_frame,
            text="📋 Your PDFs (drag to reorder)",
            font=("Segoe UI", 11, "bold"),
            fg=self.text_light,
            bg=self.bg_light
        )
        header_label.pack(pady=10)
        
        # Listbox with custom styling
        list_frame = tk.Frame(list_container, bg=self.bg_medium)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        scrollbar = tk.Scrollbar(list_frame, bg=self.bg_light, troughcolor=self.bg_medium, 
                                 activebackground=self.accent_purple, width=12)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 11),
            bg=self.bg_light,
            fg=self.text_light,
            selectbackground=self.accent_purple,
            selectforeground=self.text_light,
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectborderwidth=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Bind drag and drop events
        self.listbox.bind('<Button-1>', self.on_click)
        self.listbox.bind('<B1-Motion>', self.on_drag)
        self.listbox.bind('<ButtonRelease-1>', self.on_release)
        
        # Control buttons frame
        control_frame = tk.Frame(main_container, bg=self.bg_dark)
        control_frame.pack(fill=tk.X)
        
        # Move buttons
        move_frame = tk.Frame(control_frame, bg=self.bg_dark)
        move_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        self.move_up_btn = self.create_icon_button(move_frame, "⬆️", self.move_up)
        self.move_up_btn.pack(side=tk.LEFT, padx=2)
        
        self.move_down_btn = self.create_icon_button(move_frame, "⬇️", self.move_down)
        self.move_down_btn.pack(side=tk.LEFT, padx=2)
        
        self.remove_btn = self.create_icon_button(control_frame, "❌ Remove", self.remove_selected)
        self.remove_btn.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="",
            font=("Segoe UI", 9),
            fg=self.accent_green,
            bg=self.bg_dark,
            anchor=tk.E
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Configure button hover effects
        self.setup_hover_effects()
    
    def create_modern_button(self, parent, text, command, color):
        """Create a modern styled button with rounded corners effect"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg=self.text_light,
            activebackground=self.hover_purple,
            activeforeground=self.text_light,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=12
        )
        return btn
    
    def create_icon_button(self, parent, text, command):
        """Create an icon button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            bg=self.bg_light,
            fg=self.text_light,
            activebackground=self.accent_purple,
            activeforeground=self.text_light,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=12,
            pady=8
        )
        return btn
    
    def setup_hover_effects(self):
        """Add hover effects to buttons"""
        buttons = [
            (self.add_button, self.accent_blue, "#00e5ff"),
            (self.clear_button, "#ff6b6b", "#ff8787"),
            (self.merge_button, self.accent_green, "#33ff99"),
            (self.move_up_btn, self.bg_light, self.accent_purple),
            (self.move_down_btn, self.bg_light, self.accent_purple),
            (self.remove_btn, self.bg_light, self.accent_purple)
        ]
        
        for btn, normal_color, hover_color in buttons:
            def make_hover(button=btn, normal=normal_color, hover=hover_color):
                def on_enter(e):
                    button.config(bg=hover)
                def on_leave(e):
                    button.config(bg=normal)
                return on_enter, on_leave
            
            on_enter, on_leave = make_hover()
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def update_status(self, message, color=None):
        """Update status label"""
        if color is None:
            color = self.accent_green
        self.status_label.config(text=message, fg=color)
        self.root.after(3000, lambda: self.status_label.config(text=""))
    
    def on_click(self, event):
        """Handle mouse click for drag and drop"""
        self.drag_index = self.listbox.nearest(event.y)
    
    def on_drag(self, event):
        """Handle drag motion"""
        if self.drag_index is not None:
            current_index = self.listbox.nearest(event.y)
            if current_index != self.drag_index and 0 <= current_index < len(self.pdf_files):
                # Visual feedback
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(current_index)
    
    def on_release(self, event):
        """Handle mouse release for drag and drop"""
        if self.drag_index is not None:
            new_index = self.listbox.nearest(event.y)
            if new_index != self.drag_index and 0 <= new_index < len(self.pdf_files):
                # Move item
                item = self.listbox.get(self.drag_index)
                file_path = self.pdf_files[self.drag_index]
                
                self.listbox.delete(self.drag_index)
                self.pdf_files.pop(self.drag_index)
                
                self.listbox.insert(new_index, item)
                self.pdf_files.insert(new_index, file_path)
                
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(new_index)
                self.update_status("✓ PDF reordered!", self.accent_green)
            self.drag_index = None
    
    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        added_count = 0
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                filename = os.path.basename(file)
                self.listbox.insert(tk.END, f"📄 {filename}")
                added_count += 1
        
        if added_count > 0:
            self.update_status(f"✓ Added {added_count} PDF(s)", self.accent_blue)
        else:
            self.update_status("No new PDFs added", "#ffaa00")
    
    def clear_all(self):
        if self.pdf_files:
            if messagebox.askyesno("Clear All", "Are you sure you want to remove all PDFs?"):
                self.pdf_files.clear()
                self.listbox.delete(0, tk.END)
                self.update_status("✓ All PDFs cleared", "#ff6b6b")
        else:
            self.update_status("Nothing to clear", "#ffaa00")
    
    def remove_selected(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            filename = os.path.basename(self.pdf_files[index])
            self.listbox.delete(index)
            self.pdf_files.pop(index)
            self.update_status(f"✓ Removed {filename}", "#ff6b6b")
        else:
            self.update_status("Please select a PDF to remove", "#ffaa00")
    
    def move_up(self):
        selected = self.listbox.curselection()
        if selected and selected[0] > 0:
            index = selected[0]
            item = self.listbox.get(index)
            file_path = self.pdf_files[index]
            
            self.listbox.delete(index)
            self.pdf_files.pop(index)
            
            self.listbox.insert(index - 1, item)
            self.pdf_files.insert(index - 1, file_path)
            
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index - 1)
            self.update_status("✓ Moved up", self.accent_blue)
    
    def move_down(self):
        selected = self.listbox.curselection()
        if selected and selected[0] < len(self.pdf_files) - 1:
            index = selected[0]
            item = self.listbox.get(index)
            file_path = self.pdf_files[index]
            
            self.listbox.delete(index)
            self.pdf_files.pop(index)
            
            self.listbox.insert(index + 1, item)
            self.pdf_files.insert(index + 1, file_path)
            
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index + 1)
            self.update_status("✓ Moved down", self.accent_blue)
    
    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("⚠️ No PDFs", "Please add at least one PDF file.")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        try:
            self.update_status("⏳ Merging PDFs...", self.accent_blue)
            self.root.update()
            
            merger = PdfMerger()
            
            for pdf_file in self.pdf_files:
                merger.append(pdf_file)
            
            merger.write(output_file)
            merger.close()
            
            filename = os.path.basename(output_file)
            self.update_status(f"✨ Successfully merged {len(self.pdf_files)} PDF(s)!", self.accent_green)
            messagebox.showinfo(
                "✨ Success!",
                f"PDFs merged successfully!\n\n📄 Saved as: {filename}\n📍 Location: {os.path.dirname(output_file)}"
            )
        except Exception as e:
            self.update_status("❌ Merge failed", "#ff6b6b")
            messagebox.showerror("❌ Error", f"An error occurred while merging PDFs:\n\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCollator(root)
    root.mainloop()
