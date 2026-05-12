#!/usr/bin/env python3
"""
HAR Inspector - Desktop Application
A powerful tool to inspect, filter, and convert HTTP Archive (HAR) files
"""

import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path
import customtkinter as ctk

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class HARInspector(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("HAR Inspector - Network Archive Tool")
        self.geometry("1400x900")
        self.minsize(1000, 600)

        # Data storage
        self.har_data = None
        self.entries = []
        self.filtered_entries = []
        self.selected_entry = None

        # Create UI
        self.create_header()
        self.create_uploader_view()

    def create_header(self):
        """Create the header bar"""
        header = ctk.CTkFrame(self, height=60, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        # Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=10)

        title = ctk.CTkLabel(
            title_frame,
            text="HAR Inspector",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            title_frame,
            text="  •  NETWORK ARCHIVE TOOL",
            font=ctk.CTkFont(size=9),
            text_color="gray50"
        )
        subtitle.pack(side="left")

        # Info label
        info = ctk.CTkLabel(
            header,
            text="🛡️ Desktop Application - Files processed locally",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        info.pack(side="right", padx=20)

    def create_uploader_view(self):
        """Create the file uploader view"""
        # Clear existing content
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="Analyze and Modify Network Logs",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="A powerful, privacy-focused tool to inspect, filter, and convert HTTP Archive (HAR) files",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        subtitle.pack(pady=(0, 40))

        # Upload button
        upload_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, height=300)
        upload_frame.pack(pady=20, padx=100, fill="x")
        upload_frame.pack_propagate(False)

        upload_icon = ctk.CTkLabel(
            upload_frame,
            text="📁",
            font=ctk.CTkFont(size=60)
        )
        upload_icon.pack(pady=(60, 20))

        upload_text = ctk.CTkLabel(
            upload_frame,
            text="Click to select your HAR file",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        upload_text.pack(pady=5)

        upload_subtext = ctk.CTkLabel(
            upload_frame,
            text="Supports .har and .json files",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        upload_subtext.pack(pady=5)

        # Make frame clickable
        upload_frame.bind("<Button-1>", lambda e: self.open_file())
        for widget in upload_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: self.open_file())

        # Info boxes
        info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        info_frame.pack(pady=30, fill="x", padx=100)

        info1 = ctk.CTkFrame(info_frame, corner_radius=10)
        info1.pack(side="left", fill="both", expand=True, padx=(0, 10))

        info1_title = ctk.CTkLabel(
            info1,
            text="✓ Privacy First",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        info1_title.pack(pady=(15, 5), padx=15, anchor="w")

        info1_text = ctk.CTkLabel(
            info1,
            text="Files are processed entirely on your computer.\nNo data is uploaded to any server.",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            justify="left"
        )
        info1_text.pack(pady=(0, 15), padx=15, anchor="w")

        info2 = ctk.CTkFrame(info_frame, corner_radius=10)
        info2.pack(side="right", fill="both", expand=True, padx=(10, 0))

        info2_title = ctk.CTkLabel(
            info2,
            text="⚠️ Security Note",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        info2_title.pack(pady=(15, 5), padx=15, anchor="w")

        info2_text = ctk.CTkLabel(
            info2,
            text="HAR files can contain sensitive data like cookies\nand auth tokens. Be careful when sharing.",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            justify="left"
        )
        info2_text.pack(pady=(0, 15), padx=15, anchor="w")

    def open_file(self):
        """Open file dialog and load HAR file"""
        file_path = filedialog.askopenfilename(
            title="Select HAR file",
            filetypes=[("HAR files", "*.har"), ("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Validate HAR structure
                if 'log' not in data or 'entries' not in data['log']:
                    messagebox.showerror("Invalid File", "Invalid HAR file format. Missing 'log.entries' structure.")
                    return

                self.har_data = data
                self.entries = data['log']['entries']
                self.filtered_entries = self.entries.copy()

                # Add internal IDs
                for i, entry in enumerate(self.entries):
                    if '_id' not in entry:
                        entry['_id'] = f"entry-{i}"

                messagebox.showinfo("Success", f"Loaded {len(self.entries)} network entries")
                self.create_viewer_view()

            except json.JSONDecodeError:
                messagebox.showerror("Parse Error", "Failed to parse HAR file. Invalid JSON format.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def create_viewer_view(self):
        """Create the viewer with entry list and details"""
        # Clear existing content
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Toolbar
        self.create_toolbar()

        # Main content area with list and details
        main_area = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_area.pack(fill="both", expand=True)

        # Entry list (left side)
        self.create_entry_list(main_area)

        # Details panel (right side)
        self.create_details_panel(main_area)

    def create_toolbar(self):
        """Create the toolbar with filters and export buttons"""
        toolbar = ctk.CTkFrame(self.content_frame, corner_radius=0)
        toolbar.pack(fill="x", padx=0, pady=0)

        # Search box
        self.search_var = ctk.StringVar()
        self.search_var.trace('w', lambda *args: self.apply_filters())

        search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔍 Filter by URL...",
            textvariable=self.search_var,
            width=300
        )
        search_entry.pack(side="left", padx=10, pady=10)

        # Method filter
        self.method_var = ctk.StringVar(value="ALL")
        method_menu = ctk.CTkOptionMenu(
            toolbar,
            variable=self.method_var,
            values=["ALL", "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            command=lambda x: self.apply_filters(),
            width=120
        )
        method_menu.pack(side="left", padx=5, pady=10)

        # Spacer
        spacer = ctk.CTkFrame(toolbar, fg_color="transparent")
        spacer.pack(side="left", fill="x", expand=True)

        # Export CSV button
        export_csv_btn = ctk.CTkButton(
            toolbar,
            text="📊 Export CSV",
            command=self.export_csv,
            width=120,
            fg_color="gray30",
            hover_color="gray40"
        )
        export_csv_btn.pack(side="left", padx=5, pady=10)

        # Export HAR button
        export_har_btn = ctk.CTkButton(
            toolbar,
            text="💾 Save HAR",
            command=self.export_har,
            width=120
        )
        export_har_btn.pack(side="left", padx=5, pady=10)

        # Reset button
        reset_btn = ctk.CTkButton(
            toolbar,
            text="🗑️",
            command=self.reset_view,
            width=40,
            fg_color="transparent",
            hover_color="darkred"
        )
        reset_btn.pack(side="left", padx=10, pady=10)

    def create_entry_list(self, parent):
        """Create the scrollable list of entries"""
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Header
        header = ctk.CTkFrame(list_frame, height=35, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        headers = [
            ("Status", 60),
            ("Method", 70),
            ("URL", 400),
            ("Size", 80),
            ("Time", 80)
        ]

        for text, width in headers:
            label = ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="gray60",
                width=width
            )
            label.pack(side="left", padx=5)

        # Scrollable frame for entries
        self.entry_list_frame = ctk.CTkScrollableFrame(list_frame)
        self.entry_list_frame.pack(fill="both", expand=True, padx=0, pady=(5, 0))

        self.populate_entry_list()

    def populate_entry_list(self):
        """Populate the entry list with filtered entries"""
        # Clear existing entries
        for widget in self.entry_list_frame.winfo_children():
            widget.destroy()

        for entry in self.filtered_entries:
            self.create_entry_row(entry)

    def create_entry_row(self, entry):
        """Create a single row for an entry"""
        row = ctk.CTkFrame(
            self.entry_list_frame,
            corner_radius=5,
            fg_color=("gray85", "gray20"),
            cursor="hand2"
        )
        row.pack(fill="x", padx=2, pady=1)

        # Status
        status_color = self.get_status_color(entry['response']['status'])
        status_label = ctk.CTkLabel(
            row,
            text=str(entry['response']['status']),
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color=status_color,
            width=60
        )
        status_label.pack(side="left", padx=5, pady=5)

        # Method
        method_color = self.get_method_color(entry['request']['method'])
        method_label = ctk.CTkLabel(
            row,
            text=entry['request']['method'],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=method_color,
            width=70
        )
        method_label.pack(side="left", padx=5, pady=5)

        # URL (truncated)
        url = entry['request']['url']
        if len(url) > 60:
            url = url[:57] + "..."
        url_label = ctk.CTkLabel(
            row,
            text=url,
            font=ctk.CTkFont(size=11),
            anchor="w",
            width=400
        )
        url_label.pack(side="left", padx=5, pady=5)

        # Size
        size_text = self.format_bytes(entry['response']['content']['size'])
        size_label = ctk.CTkLabel(
            row,
            text=size_text,
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="gray60",
            width=80
        )
        size_label.pack(side="left", padx=5, pady=5)

        # Time
        time_text = f"{int(entry['time'])}ms"
        time_label = ctk.CTkLabel(
            row,
            text=time_text,
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="gray60",
            width=80
        )
        time_label.pack(side="left", padx=5, pady=5)

        # Make row clickable
        row.bind("<Button-1>", lambda e, ent=entry: self.show_entry_details(ent))
        for widget in row.winfo_children():
            widget.bind("<Button-1>", lambda e, ent=entry: self.show_entry_details(ent))

    def create_details_panel(self, parent):
        """Create the details panel (right side)"""
        self.details_frame = ctk.CTkFrame(parent)
        self.details_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # Default message
        self.details_content = ctk.CTkLabel(
            self.details_frame,
            text="Select an entry to view details",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        self.details_content.pack(expand=True)

    def show_entry_details(self, entry):
        """Show detailed information for selected entry"""
        self.selected_entry = entry

        # Clear details panel
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Create scrollable details
        details_scroll = ctk.CTkScrollableFrame(self.details_frame)
        details_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Header
        header = ctk.CTkFrame(details_scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(
            header,
            text=f"{entry['request']['method']} - {entry['response']['status']}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(anchor="w")

        url_label = ctk.CTkLabel(
            header,
            text=entry['request']['url'],
            font=ctk.CTkFont(family="Courier", size=10),
            text_color="gray60"
        )
        url_label.pack(anchor="w")

        # Action buttons
        btn_frame = ctk.CTkFrame(details_scroll, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))

        edit_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Edit Entry",
            command=lambda: self.edit_entry(entry),
            width=120
        )
        edit_btn.pack(side="left", padx=(0, 5))

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Remove",
            command=lambda: self.remove_entry(entry),
            width=120,
            fg_color="darkred",
            hover_color="red"
        )
        delete_btn.pack(side="left")

        # Summary info
        self.create_section(details_scroll, "Summary", [
            ("Started", datetime.fromisoformat(entry['startedDateTime'].replace('Z', '+00:00')).strftime('%H:%M:%S.%f')[:-3]),
            ("IP Address", entry.get('serverIPAddress', 'Unknown')),
            ("Protocol", entry['request']['httpVersion']),
            ("Content Type", entry['response']['content']['mimeType']),
            ("Total Time", f"{int(entry['time'])}ms"),
            ("Size", self.format_bytes(entry['response']['content']['size']))
        ])

        # Request headers
        headers_text = "\n".join([f"{h['name']}: {h['value']}" for h in entry['request']['headers'][:10]])
        if len(entry['request']['headers']) > 10:
            headers_text += f"\n... and {len(entry['request']['headers']) - 10} more"
        self.create_section(details_scroll, "Request Headers", [], headers_text)

        # Response headers
        headers_text = "\n".join([f"{h['name']}: {h['value']}" for h in entry['response']['headers'][:10]])
        if len(entry['response']['headers']) > 10:
            headers_text += f"\n... and {len(entry['response']['headers']) - 10} more"
        self.create_section(details_scroll, "Response Headers", [], headers_text)

        # Request body
        if 'postData' in entry['request'] and entry['request']['postData'].get('text'):
            body_text = entry['request']['postData']['text']
            if len(body_text) > 500:
                body_text = body_text[:500] + "\n... (truncated)"
            self.create_section(details_scroll, "Request Body", [], body_text)

        # Response content
        if entry['response']['content'].get('text'):
            content_text = entry['response']['content']['text']
            if len(content_text) > 500:
                content_text = content_text[:500] + "\n... (truncated)"
            self.create_section(details_scroll, "Response Content", [], content_text)

        # Timings
        timings = entry['timings']
        timing_info = [
            (f"DNS: {int(timings.get('dns', -1))}ms" if timings.get('dns', -1) >= 0 else "DNS: -"),
            (f"Connect: {int(timings.get('connect', -1))}ms" if timings.get('connect', -1) >= 0 else "Connect: -"),
            (f"Wait: {int(timings.get('wait', -1))}ms" if timings.get('wait', -1) >= 0 else "Wait: -"),
            (f"Receive: {int(timings.get('receive', -1))}ms" if timings.get('receive', -1) >= 0 else "Receive: -")
        ]
        self.create_section(details_scroll, "Timing Breakdown", [], "  |  ".join(timing_info))

    def create_section(self, parent, title, items=None, text=None):
        """Create a section in the details panel"""
        section = ctk.CTkFrame(parent, corner_radius=8)
        section.pack(fill="x", pady=(0, 10))

        # Title
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray70"
        )
        title_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Content
        if items:
            for key, value in items:
                item_frame = ctk.CTkFrame(section, fg_color="transparent")
                item_frame.pack(fill="x", padx=10, pady=2)

                key_label = ctk.CTkLabel(
                    item_frame,
                    text=f"{key}:",
                    font=ctk.CTkFont(size=11),
                    text_color="gray60",
                    width=120,
                    anchor="w"
                )
                key_label.pack(side="left")

                value_label = ctk.CTkLabel(
                    item_frame,
                    text=str(value),
                    font=ctk.CTkFont(family="Courier", size=11),
                    anchor="w"
                )
                value_label.pack(side="left", fill="x", expand=True)

        if text:
            text_box = ctk.CTkTextbox(
                section,
                height=100,
                font=ctk.CTkFont(family="Courier", size=10),
                wrap="none"
            )
            text_box.pack(fill="both", padx=10, pady=(5, 10))
            text_box.insert("1.0", text)
            text_box.configure(state="disabled")

        # Spacer
        ctk.CTkFrame(section, height=5, fg_color="transparent").pack()

    def edit_entry(self, entry):
        """Open edit dialog for an entry"""
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit Entry")
        edit_window.geometry("800x700")

        # Make it modal
        edit_window.transient(self)
        edit_window.grab_set()

        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(edit_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            scroll_frame,
            text="Edit Entry",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(0, 20))

        # URL
        url_label = ctk.CTkLabel(scroll_frame, text="URL:", anchor="w")
        url_label.pack(fill="x", pady=(10, 5))
        url_entry = ctk.CTkEntry(scroll_frame)
        url_entry.insert(0, entry['request']['url'])
        url_entry.pack(fill="x", pady=(0, 10))

        # Method
        method_label = ctk.CTkLabel(scroll_frame, text="Method:", anchor="w")
        method_label.pack(fill="x", pady=(10, 5))
        method_var = ctk.StringVar(value=entry['request']['method'])
        method_menu = ctk.CTkOptionMenu(
            scroll_frame,
            variable=method_var,
            values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        )
        method_menu.pack(fill="x", pady=(0, 10))

        # Status
        status_label = ctk.CTkLabel(scroll_frame, text="Status Code:", anchor="w")
        status_label.pack(fill="x", pady=(10, 5))
        status_entry = ctk.CTkEntry(scroll_frame)
        status_entry.insert(0, str(entry['response']['status']))
        status_entry.pack(fill="x", pady=(0, 10))

        # Request body
        if 'postData' in entry['request']:
            body_label = ctk.CTkLabel(scroll_frame, text="Request Body:", anchor="w")
            body_label.pack(fill="x", pady=(10, 5))
            body_text = ctk.CTkTextbox(scroll_frame, height=100)
            body_text.insert("1.0", entry['request']['postData'].get('text', ''))
            body_text.pack(fill="x", pady=(0, 10))

        # Response content
        content_label = ctk.CTkLabel(scroll_frame, text="Response Content:", anchor="w")
        content_label.pack(fill="x", pady=(10, 5))
        content_text = ctk.CTkTextbox(scroll_frame, height=150)
        content_text.insert("1.0", entry['response']['content'].get('text', ''))
        content_text.pack(fill="x", pady=(0, 10))

        # Save button
        def save_changes():
            entry['request']['url'] = url_entry.get()
            entry['request']['method'] = method_var.get()
            entry['response']['status'] = int(status_entry.get())

            if 'postData' in entry['request']:
                entry['request']['postData']['text'] = body_text.get("1.0", "end-1c")

            entry['response']['content']['text'] = content_text.get("1.0", "end-1c")

            messagebox.showinfo("Success", "Entry updated successfully")
            edit_window.destroy()

            # Refresh view
            self.show_entry_details(entry)
            self.populate_entry_list()

        save_btn = ctk.CTkButton(
            scroll_frame,
            text="💾 Save Changes",
            command=save_changes,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(pady=20, fill="x")

    def remove_entry(self, entry):
        """Remove an entry from the list"""
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this entry?"):
            # Remove from all lists
            if entry in self.entries:
                self.entries.remove(entry)
            if entry in self.filtered_entries:
                self.filtered_entries.remove(entry)

            # Update HAR data
            if self.har_data and 'log' in self.har_data:
                self.har_data['log']['entries'] = self.entries

            # Clear details
            for widget in self.details_frame.winfo_children():
                widget.destroy()

            self.details_content = ctk.CTkLabel(
                self.details_frame,
                text="Entry removed. Select another entry to view details.",
                font=ctk.CTkFont(size=14),
                text_color="gray60"
            )
            self.details_content.pack(expand=True)

            # Refresh list
            self.populate_entry_list()
            messagebox.showinfo("Success", "Entry removed successfully")

    def apply_filters(self):
        """Apply search and method filters"""
        search_text = self.search_var.get().lower()
        method_filter = self.method_var.get()

        self.filtered_entries = [
            entry for entry in self.entries
            if (search_text in entry['request']['url'].lower()) and
               (method_filter == "ALL" or entry['request']['method'] == method_filter)
        ]

        self.populate_entry_list()

    def export_csv(self):
        """Export filtered entries to CSV"""
        if not self.filtered_entries:
            messagebox.showwarning("No Data", "No entries to export")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export as CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Method', 'URL', 'Status', 'Size', 'Time (ms)'])

                    for entry in self.filtered_entries:
                        writer.writerow([
                            entry['request']['method'],
                            entry['request']['url'],
                            entry['response']['status'],
                            entry['response']['content']['size'],
                            int(entry['time'])
                        ])

                messagebox.showinfo("Success", f"Exported {len(self.filtered_entries)} entries to CSV")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")

    def export_har(self):
        """Export modified HAR file"""
        if not self.har_data:
            messagebox.showwarning("No Data", "No HAR data to export")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save HAR file",
            defaultextension=".har",
            filetypes=[("HAR files", "*.har"), ("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                # Clean up internal _id fields before saving
                clean_data = json.loads(json.dumps(self.har_data))
                for entry in clean_data['log']['entries']:
                    if '_id' in entry:
                        del entry['_id']

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(clean_data, f, indent=2)

                messagebox.showinfo("Success", "HAR file saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save HAR file: {str(e)}")

    def reset_view(self):
        """Reset to uploader view"""
        if messagebox.askyesno("Confirm", "Close current file and load a new one?"):
            self.har_data = None
            self.entries = []
            self.filtered_entries = []
            self.selected_entry = None
            self.create_uploader_view()

    @staticmethod
    def get_status_color(status):
        """Get color for HTTP status code"""
        if 200 <= status < 300:
            return "#10b981"  # green
        elif 300 <= status < 400:
            return "#0ea5e9"  # blue
        elif 400 <= status < 500:
            return "#f59e0b"  # amber
        elif status >= 500:
            return "#ef4444"  # red
        return "gray60"

    @staticmethod
    def get_method_color(method):
        """Get color for HTTP method"""
        colors = {
            'GET': '#10b981',     # green
            'POST': '#0ea5e9',    # blue
            'PUT': '#f59e0b',     # amber
            'DELETE': '#ef4444',  # red
            'PATCH': '#8b5cf6',   # violet
        }
        return colors.get(method.upper(), 'gray60')

    @staticmethod
    def format_bytes(bytes_size):
        """Format bytes to human readable format"""
        if bytes_size == 0:
            return "0 B"

        units = ['B', 'KB', 'MB', 'GB']
        size = float(bytes_size)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.1f} {units[unit_index]}"


def main():
    """Main entry point"""
    app = HARInspector()
    app.mainloop()


if __name__ == "__main__":
    main()
