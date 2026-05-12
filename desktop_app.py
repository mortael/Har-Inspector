from __future__ import annotations

import csv
import json
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk


class HarInspectorDesktop(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("HAR Inspector")
        self.geometry("1260x760")
        self.minsize(960, 620)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.har_data: dict | None = None
        self.filtered_indices: list[int] = []
        self.current_index: int | None = None

        self.search_var = ctk.StringVar(value="")
        self.method_var = ctk.StringVar(value="ALL")
        self.url_var = ctk.StringVar(value="")
        self.entry_method_var = ctk.StringVar(value="GET")
        self.status_var = ctk.StringVar(value="200")

        self._build_ui()
        self._bind_events()
        self._set_buttons_enabled(False)

    def _build_ui(self) -> None:
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=12, pady=(12, 8))

        self.open_btn = ctk.CTkButton(top, text="Open HAR", command=self.open_har_file)
        self.open_btn.pack(side="left", padx=(8, 8), pady=8)

        self.save_btn = ctk.CTkButton(top, text="Save HAR", command=self.save_har_file)
        self.save_btn.pack(side="left", padx=8, pady=8)

        self.csv_btn = ctk.CTkButton(top, text="Export CSV", command=self.export_csv)
        self.csv_btn.pack(side="left", padx=8, pady=8)

        self.remove_btn = ctk.CTkButton(top, text="Remove Selected", command=self.remove_selected_entry)
        self.remove_btn.pack(side="left", padx=8, pady=8)

        filters = ctk.CTkFrame(self)
        filters.pack(fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(filters, text="Search URL").pack(side="left", padx=(8, 6), pady=8)
        self.search_entry = ctk.CTkEntry(filters, textvariable=self.search_var, width=330)
        self.search_entry.pack(side="left", padx=(0, 12), pady=8)

        ctk.CTkLabel(filters, text="Method").pack(side="left", padx=(0, 6), pady=8)
        self.method_filter = ctk.CTkComboBox(
            filters, values=["ALL", "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"], variable=self.method_var, width=140
        )
        self.method_filter.pack(side="left", padx=(0, 8), pady=8)

        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(main)
        left.grid(row=0, column=0, padx=(10, 6), pady=10, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=1)

        columns = ("status", "method", "url", "time", "size")
        self.tree = ttk.Treeview(left, columns=columns, show="headings", height=20)
        self.tree.heading("status", text="Status")
        self.tree.heading("method", text="Method")
        self.tree.heading("url", text="URL")
        self.tree.heading("time", text="Time (ms)")
        self.tree.heading("size", text="Size")

        self.tree.column("status", width=70, anchor="center")
        self.tree.column("method", width=80, anchor="center")
        self.tree.column("url", width=440, anchor="w")
        self.tree.column("time", width=90, anchor="e")
        self.tree.column("size", width=90, anchor="e")

        y_scroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        y_scroll.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=8)

        right = ctk.CTkFrame(main)
        right.grid(row=0, column=1, padx=(6, 10), pady=10, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(7, weight=1)

        ctk.CTkLabel(right, text="Selected Request URL").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 4))
        self.url_entry = ctk.CTkEntry(right, textvariable=self.url_var)
        self.url_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))

        row = ctk.CTkFrame(right, fg_color="transparent")
        row.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 8))
        row.grid_columnconfigure(0, weight=0)
        row.grid_columnconfigure(1, weight=0)
        row.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(row, text="Method").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.entry_method = ctk.CTkComboBox(
            row, values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"], variable=self.entry_method_var, width=120
        )
        self.entry_method.grid(row=0, column=1, sticky="w", padx=(0, 12))

        ctk.CTkLabel(row, text="Status").grid(row=0, column=2, sticky="w")
        self.status_entry = ctk.CTkEntry(row, textvariable=self.status_var, width=90)
        self.status_entry.grid(row=0, column=2, sticky="e")

        actions = ctk.CTkFrame(right, fg_color="transparent")
        actions.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 8))
        self.apply_btn = ctk.CTkButton(actions, text="Apply Changes", command=self.apply_selected_changes)
        self.apply_btn.pack(side="left", padx=(0, 8))
        self.reload_btn = ctk.CTkButton(actions, text="Reload Selection", command=self.load_selection_into_form)
        self.reload_btn.pack(side="left")

        ctk.CTkLabel(right, text="Entry Details").grid(row=4, column=0, sticky="w", padx=10, pady=(8, 4))
        self.details = ctk.CTkTextbox(right, wrap="none")
        self.details.grid(row=7, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.details.configure(state="disabled")

        self.status_label = ctk.CTkLabel(self, text="Open a HAR file to begin.")
        self.status_label.pack(fill="x", padx=14, pady=(0, 8), anchor="w")

    def _bind_events(self) -> None:
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.search_var.trace_add("write", lambda *_: self.apply_filters())
        self.method_var.trace_add("write", lambda *_: self.apply_filters())

    def _set_buttons_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for widget in [self.save_btn, self.csv_btn, self.remove_btn, self.apply_btn, self.reload_btn, self.url_entry, self.entry_method, self.status_entry]:
            widget.configure(state=state)

    def open_har_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("HAR files", "*.har *.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._validate_har(data)
            self.har_data = data
            self.current_index = None
            self.apply_filters()
            self._set_buttons_enabled(True)
            self.status_label.configure(text=f"Loaded {len(self.har_data['log']['entries'])} entries from {Path(path).name}")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to open HAR file:\n{exc}")

    def _validate_har(self, data: dict) -> None:
        if not isinstance(data, dict) or "log" not in data:
            raise ValueError("Invalid HAR: missing 'log' object")
        entries = data.get("log", {}).get("entries")
        if not isinstance(entries, list):
            raise ValueError("Invalid HAR: 'log.entries' must be an array")

    def apply_filters(self) -> None:
        if not self.har_data:
            return

        search = self.search_var.get().strip().lower()
        method = self.method_var.get().strip().upper()
        all_entries = self.har_data["log"]["entries"]

        self.tree.delete(*self.tree.get_children())
        self.filtered_indices.clear()
        self.current_index = None
        self.clear_form()
        self._set_details("")

        for idx, entry in enumerate(all_entries):
            req = entry.get("request", {})
            res = entry.get("response", {})
            method_value = str(req.get("method", ""))
            url = str(req.get("url", ""))
            if search and search not in url.lower():
                continue
            if method != "ALL" and method_value.upper() != method:
                continue

            size = _safe_int(res.get("content", {}).get("size"))
            time_ms = _safe_int(entry.get("time"))
            status = _safe_int(res.get("status"))
            self.filtered_indices.append(idx)
            self.tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(status, method_value, _shorten(url, 140), time_ms, _format_bytes(size)),
            )

        self.status_label.configure(text=f"Showing {len(self.filtered_indices)} of {len(all_entries)} entries")

    def on_tree_select(self, _event=None) -> None:
        selected = self.tree.selection()
        if not selected or not self.har_data:
            return
        self.current_index = int(selected[0])
        self.load_selection_into_form()

    def load_selection_into_form(self) -> None:
        if self.current_index is None or not self.har_data:
            return
        entry = self.har_data["log"]["entries"][self.current_index]
        req = entry.get("request", {})
        res = entry.get("response", {})
        self.url_var.set(str(req.get("url", "")))
        self.entry_method_var.set(str(req.get("method", "GET")).upper())
        self.status_var.set(str(_safe_int(res.get("status"))))
        self._set_details(json.dumps(entry, indent=2, ensure_ascii=False))

    def apply_selected_changes(self) -> None:
        if self.current_index is None or not self.har_data:
            return
        status_text = self.status_var.get().strip()
        if not status_text.isdigit():
            messagebox.showerror("Validation error", "Status must contain digits only.")
            return

        entry = self.har_data["log"]["entries"][self.current_index]
        entry.setdefault("request", {})
        entry.setdefault("response", {})
        entry["request"]["url"] = self.url_var.get().strip()
        entry["request"]["method"] = self.entry_method_var.get().strip().upper()
        entry["response"]["status"] = int(status_text)
        self._set_details(json.dumps(entry, indent=2, ensure_ascii=False))
        self.apply_filters()
        self.tree.selection_set(str(self.current_index))
        self.status_label.configure(text="Selected entry updated.")

    def remove_selected_entry(self) -> None:
        if self.current_index is None or not self.har_data:
            messagebox.showinfo("Selection required", "Select an entry to remove.")
            return
        should_delete = messagebox.askyesno("Confirm removal", "Remove selected entry from HAR data?")
        if not should_delete:
            return
        entries = self.har_data["log"]["entries"]
        del entries[self.current_index]
        self.current_index = None
        self.apply_filters()
        self.status_label.configure(text="Entry removed.")

    def save_har_file(self) -> None:
        if not self.har_data:
            return
        output = filedialog.asksaveasfilename(
            defaultextension=".har",
            filetypes=[("HAR files", "*.har"), ("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="modified_capture.har",
        )
        if not output:
            return
        try:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(self.har_data, f, ensure_ascii=False, indent=2)
            self.status_label.configure(text=f"Saved HAR file to {Path(output).name}")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

    def export_csv(self) -> None:
        if not self.har_data:
            return
        output = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="network_log.csv",
        )
        if not output:
            return
        try:
            with open(output, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Method", "URL", "Status", "Size", "Time (ms)"])
                for idx in self.filtered_indices:
                    entry = self.har_data["log"]["entries"][idx]
                    req = entry.get("request", {})
                    res = entry.get("response", {})
                    writer.writerow(
                        [
                            req.get("method", ""),
                            req.get("url", ""),
                            _safe_int(res.get("status")),
                            _safe_int(res.get("content", {}).get("size")),
                            _safe_int(entry.get("time")),
                        ]
                    )
            self.status_label.configure(text=f"Exported CSV to {Path(output).name}")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))

    def clear_form(self) -> None:
        self.url_var.set("")
        self.entry_method_var.set("GET")
        self.status_var.set("200")

    def _set_details(self, text: str) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text)
        self.details.configure(state="disabled")


def _safe_int(value: object) -> int:
    # bool is intentionally excluded so True/False are not treated as 1/0 in HAR fields.
    # Negative numeric values are clamped to 0 for consistent UI aggregation/display.
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return 0
    try:
        return max(0, int(value))
    except ValueError:
        return 0


def _shorten(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[: max_len - 3] + "..."


def _format_bytes(size: int) -> str:
    if size <= 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    amount = float(size)
    unit_idx = 0
    while amount >= 1024 and unit_idx < len(units) - 1:
        amount /= 1024
        unit_idx += 1
    return f"{amount:.1f} {units[unit_idx]}"


if __name__ == "__main__":
    app = HarInspectorDesktop()
    app.mainloop()
