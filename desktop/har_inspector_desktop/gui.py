from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

import customtkinter as ctk

from .har import EntryRow, HarFormatError, export_csv, iter_entry_rows, load_har, save_har


def _headers_to_text(headers: Any) -> str:
    if not isinstance(headers, list):
        return ""
    lines: list[str] = []
    for h in headers:
        if not isinstance(h, dict):
            continue
        name = str(h.get("name", "")).strip()
        value = str(h.get("value", "")).strip()
        if name or value:
            lines.append(f"{name}: {value}".rstrip())
    return "\n".join(lines)


def _text_to_headers(text: str) -> list[dict[str, str]]:
    headers: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" in line:
            name, value = line.split(":", 1)
            headers.append({"name": name.strip(), "value": value.strip()})
        else:
            headers.append({"name": line, "value": ""})
    return headers


def _safe_get(entry: dict[str, Any], *keys: str, default: Any = "") -> Any:
    cur: Any = entry
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def _safe_set(entry: dict[str, Any], *keys: str, value: Any) -> None:
    cur: Any = entry
    for k in keys[:-1]:
        nxt = cur.get(k)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[k] = nxt
        cur = nxt
    cur[keys[-1]] = value


@dataclass
class FilterState:
    search: str = ""
    method: str = "ALL"


class HarInspectorWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("HAR Inspector (Desktop)")
        self.geometry("1200x720")
        self.minsize(1000, 640)

        self.har: dict[str, Any] | None = None
        self.har_path: Path | None = None
        self.selected_entry_id: str | None = None
        self.filters = FilterState()

        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        toolbar = ctk.CTkFrame(self, corner_radius=0)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_columnconfigure(4, weight=1)

        ctk.CTkButton(toolbar, text="Open HAR…", command=self.open_har).grid(row=0, column=0, padx=10, pady=10)
        self.save_button = ctk.CTkButton(toolbar, text="Save", command=self.save_har_in_place, state="disabled")
        self.save_button.grid(row=0, column=1, padx=6, pady=10)
        self.save_as_button = ctk.CTkButton(toolbar, text="Save HAR As…", command=self.save_har_as, state="disabled")
        self.save_as_button.grid(row=0, column=2, padx=6, pady=10)
        self.export_button = ctk.CTkButton(toolbar, text="Export CSV…", command=self.export_csv_as, state="disabled")
        self.export_button.grid(row=0, column=3, padx=6, pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._on_search_changed())
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, placeholder_text="Filter by URL…")
        search_entry.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        self.method_var = tk.StringVar(value="ALL")
        self.method_var.trace_add("write", lambda *_: self._on_method_changed())
        method_menu = ctk.CTkOptionMenu(
            toolbar,
            variable=self.method_var,
            values=["ALL", "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        )
        method_menu.grid(row=0, column=5, padx=10, pady=10)

        content = ctk.CTkFrame(self, corner_radius=0)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=2)

        self._build_left(content)
        self._build_right(content)

        self._set_empty_state()

    def _build_left(self, parent: ctk.CTkFrame) -> None:
        left = ctk.CTkFrame(parent)
        left.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(left, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))
        header.grid_columnconfigure(0, weight=1)

        self.file_label = ctk.CTkLabel(header, text="No file loaded", anchor="w")
        self.file_label.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(header, text="Remove Entry", command=self.remove_selected, width=120).grid(
            row=0, column=1, padx=(10, 0)
        )

        tree_container = ctk.CTkFrame(left)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        columns = ("status", "method", "url", "size", "time")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", lambda _e: self._on_tree_select())

        self.tree.heading("status", text="Status")
        self.tree.heading("method", text="Method")
        self.tree.heading("url", text="URL")
        self.tree.heading("size", text="Size")
        self.tree.heading("time", text="Time")

        self.tree.column("status", width=60, anchor="e")
        self.tree.column("method", width=70, anchor="center")
        self.tree.column("url", width=420, anchor="w")
        self.tree.column("size", width=90, anchor="e")
        self.tree.column("time", width=90, anchor="e")

        yscroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=yscroll.set)

    def _build_right(self, parent: ctk.CTkFrame) -> None:
        right = ctk.CTkFrame(parent)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(right, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))
        top.grid_columnconfigure(1, weight=1)
        top.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(top, text="URL").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        self.url_entry = ctk.CTkEntry(top, textvariable=self.url_var)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(8, 10))

        ctk.CTkLabel(top, text="Method").grid(row=0, column=2, sticky="w")
        self.edit_method_var = tk.StringVar(value="GET")
        self.edit_method_menu = ctk.CTkOptionMenu(
            top,
            variable=self.edit_method_var,
            values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            width=120,
        )
        self.edit_method_menu.grid(row=0, column=3, sticky="ew", padx=(8, 10))

        ctk.CTkLabel(top, text="Status").grid(row=0, column=4, sticky="w")
        self.status_var = tk.StringVar(value="200")
        self.status_entry = ctk.CTkEntry(top, textvariable=self.status_var, width=80)
        self.status_entry.grid(row=0, column=5, sticky="w", padx=(8, 0))

        actions = ctk.CTkFrame(right, fg_color="transparent")
        actions.grid(row=0, column=0, sticky="e", padx=10, pady=(10, 6))

        ctk.CTkButton(actions, text="Apply Changes", command=self.apply_changes, width=120).grid(
            row=0, column=0, padx=6
        )
        ctk.CTkButton(actions, text="Revert", command=self._refresh_details_from_selected, width=80).grid(
            row=0, column=1, padx=6
        )

        self.notebook = ttk.Notebook(right)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.summary_text = self._add_text_tab("Summary")
        self.req_headers_text = self._add_text_tab("Request Headers")
        self.res_headers_text = self._add_text_tab("Response Headers")
        self.req_body_text = self._add_text_tab("Request Body")
        self.res_body_text = self._add_text_tab("Response Body")

    def _add_text_tab(self, title: str) -> tk.Text:
        frame = ttk.Frame(self.notebook)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(frame, text=title)

        text = tk.Text(frame, wrap="none", undo=True)
        text.grid(row=0, column=0, sticky="nsew")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        text.configure(yscrollcommand=yscroll.set)
        return text

    def _set_empty_state(self) -> None:
        self.file_label.configure(text="No file loaded")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.selected_entry_id = None
        self.url_var.set("")
        self.edit_method_var.set("GET")
        self.status_var.set("200")
        for t in (
            self.summary_text,
            self.req_headers_text,
            self.res_headers_text,
            self.req_body_text,
            self.res_body_text,
        ):
            t.delete("1.0", "end")
        self.save_button.configure(state="disabled")
        self.save_as_button.configure(state="disabled")
        self.export_button.configure(state="disabled")
        self._set_detail_fields_enabled(False)

    def open_har(self) -> None:
        path = filedialog.askopenfilename(
            title="Open HAR file",
            filetypes=[("HAR files", "*.har *.json"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            self.har = load_har(path)
        except HarFormatError as e:
            messagebox.showerror("Invalid HAR", str(e))
            return
        except Exception as e:
            messagebox.showerror("Failed to open", str(e))
            return

        self.har_path = Path(path)
        self.file_label.configure(text=str(self.har_path))
        self.title(f"HAR Inspector (Desktop) — {self.har_path.name}")
        self.save_button.configure(state="normal")
        self.save_as_button.configure(state="normal")
        self.export_button.configure(state="normal")
        self._refresh_tree()

    def save_har_in_place(self) -> None:
        if not self.har:
            messagebox.showinfo("No file", "Load a HAR file first.")
            return
        if not self.har_path:
            self.save_har_as()
            return
        if not messagebox.askyesno("Overwrite file", f"Overwrite:\n{self.har_path}?"):
            return
        try:
            save_har(self.har_path, self.har)
        except Exception as e:
            messagebox.showerror("Save failed", str(e))
            return
        messagebox.showinfo("Saved", f"Saved HAR to:\n{self.har_path}")

    def save_har_as(self) -> None:
        if not self.har:
            messagebox.showinfo("No file", "Load a HAR file first.")
            return
        path = filedialog.asksaveasfilename(
            title="Save HAR As",
            defaultextension=".har",
            filetypes=[("HAR files", "*.har"), ("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="modified_capture.har",
        )
        if not path:
            return
        try:
            save_har(path, self.har)
        except Exception as e:
            messagebox.showerror("Save failed", str(e))
            return
        messagebox.showinfo("Saved", f"Saved HAR to:\n{path}")

    def export_csv_as(self) -> None:
        if not self.har:
            messagebox.showinfo("No file", "Load a HAR file first.")
            return
        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="network_log.csv",
        )
        if not path:
            return
        try:
            export_csv(path, self._filtered_rows())
        except Exception as e:
            messagebox.showerror("Export failed", str(e))
            return
        messagebox.showinfo("Exported", f"Exported CSV to:\n{path}")

    def _on_search_changed(self) -> None:
        self.filters.search = self.search_var.get()
        self._refresh_tree()

    def _on_method_changed(self) -> None:
        self.filters.method = self.method_var.get()
        self._refresh_tree()

    def _filtered_rows(self) -> list[EntryRow]:
        if not self.har:
            return []
        search = self.filters.search.lower().strip()
        method = self.filters.method.upper().strip() or "ALL"
        rows: list[EntryRow] = []
        for row in iter_entry_rows(self.har):
            if search and search not in row.url.lower():
                continue
            if method != "ALL" and row.method != method:
                continue
            rows.append(row)
        return rows

    def _refresh_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self._filtered_rows()
        for r in rows:
            self.tree.insert(
                "",
                "end",
                iid=r.entry_id,
                values=(r.status, r.method, r.url, r.size, f"{round(r.time_ms)}ms"),
            )

        # Keep selection if still present
        if self.selected_entry_id and self.tree.exists(self.selected_entry_id):
            self.tree.selection_set(self.selected_entry_id)
            self.tree.see(self.selected_entry_id)
            self._refresh_details_from_selected()
        else:
            self.selected_entry_id = None
            self._set_detail_fields_enabled(False)

    def _set_detail_fields_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.url_entry.configure(state=state)
        self.edit_method_menu.configure(state=state)
        self.status_entry.configure(state=state)
        for t in (self.req_headers_text, self.res_headers_text, self.req_body_text, self.res_body_text):
            t.configure(state=state)
        self.summary_text.configure(state="disabled" if not enabled else "normal")

    def _on_tree_select(self) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_entry_id = selection[0]
        self._refresh_details_from_selected()

    def _find_selected_entry(self) -> dict[str, Any] | None:
        if not self.har or not self.selected_entry_id:
            return None
        entries = _safe_get(self.har, "log", "entries", default=[])
        if not isinstance(entries, list):
            return None
        for entry in entries:
            if isinstance(entry, dict) and entry.get("_id") == self.selected_entry_id:
                return entry
        return None

    def _refresh_details_from_selected(self) -> None:
        entry = self._find_selected_entry()
        if not entry:
            self._set_detail_fields_enabled(False)
            return
        self._set_detail_fields_enabled(True)

        self.url_var.set(str(_safe_get(entry, "request", "url", default="")))
        self.edit_method_var.set(str(_safe_get(entry, "request", "method", default="GET")).upper() or "GET")
        self.status_var.set(str(int(_safe_get(entry, "response", "status", default=0) or 0)))

        summary_lines = [
            f"Started: {_safe_get(entry, 'startedDateTime', default='')}",
            f"Time (ms): {_safe_get(entry, 'time', default='')}",
            f"Server IP: {_safe_get(entry, 'serverIPAddress', default='')}",
            f"Protocol: {_safe_get(entry, 'request', 'httpVersion', default='')}",
            f"Content-Type: {_safe_get(entry, 'response', 'content', 'mimeType', default='')}",
        ]
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", "\n".join(summary_lines).strip() + "\n")
        self.summary_text.configure(state="disabled")

        self.req_headers_text.configure(state="normal")
        self.req_headers_text.delete("1.0", "end")
        self.req_headers_text.insert("1.0", _headers_to_text(_safe_get(entry, "request", "headers", default=[])))

        self.res_headers_text.configure(state="normal")
        self.res_headers_text.delete("1.0", "end")
        self.res_headers_text.insert("1.0", _headers_to_text(_safe_get(entry, "response", "headers", default=[])))

        self.req_body_text.configure(state="normal")
        self.req_body_text.delete("1.0", "end")
        self.req_body_text.insert("1.0", str(_safe_get(entry, "request", "postData", "text", default="")))

        self.res_body_text.configure(state="normal")
        self.res_body_text.delete("1.0", "end")
        self.res_body_text.insert("1.0", str(_safe_get(entry, "response", "content", "text", default="")))

    def apply_changes(self) -> None:
        entry = self._find_selected_entry()
        if not entry:
            messagebox.showinfo("No entry", "Select an entry first.")
            return

        try:
            status = int(self.status_var.get().strip() or "0")
        except ValueError:
            messagebox.showerror("Invalid status", "Status must be a number.")
            return

        _safe_set(entry, "request", "url", value=self.url_var.get())
        _safe_set(entry, "request", "method", value=self.edit_method_var.get().upper())
        _safe_set(entry, "response", "status", value=status)

        _safe_set(entry, "request", "headers", value=_text_to_headers(self.req_headers_text.get("1.0", "end")))
        _safe_set(entry, "response", "headers", value=_text_to_headers(self.res_headers_text.get("1.0", "end")))

        req_body = self.req_body_text.get("1.0", "end").rstrip("\n")
        if req_body:
            post_data = _safe_get(entry, "request", "postData", default=None)
            if not isinstance(post_data, dict):
                post_data = {"mimeType": "text/plain"}
            post_data["text"] = req_body
            _safe_set(entry, "request", "postData", value=post_data)
        else:
            # Keep postData shape if present, but clear text
            post_data = _safe_get(entry, "request", "postData", default=None)
            if isinstance(post_data, dict):
                post_data.pop("text", None)

        res_body = self.res_body_text.get("1.0", "end").rstrip("\n")
        if res_body:
            content = _safe_get(entry, "response", "content", default=None)
            if not isinstance(content, dict):
                content = {"size": 0, "mimeType": "text/plain"}
            content["text"] = res_body
            _safe_set(entry, "response", "content", value=content)
        else:
            content = _safe_get(entry, "response", "content", default=None)
            if isinstance(content, dict):
                content.pop("text", None)

        self._refresh_tree()

    def remove_selected(self) -> None:
        if not self.har or not self.selected_entry_id:
            messagebox.showinfo("No entry", "Select an entry first.")
            return
        if not messagebox.askyesno("Remove entry", "Remove the selected entry from the log?"):
            return
        entries = _safe_get(self.har, "log", "entries", default=[])
        if not isinstance(entries, list):
            return
        new_entries: list[Any] = []
        removed = False
        for e in entries:
            if isinstance(e, dict) and e.get("_id") == self.selected_entry_id and not removed:
                removed = True
                continue
            new_entries.append(e)
        _safe_set(self.har, "log", "entries", value=new_entries)
        self.selected_entry_id = None
        self._refresh_tree()


def run_gui() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = HarInspectorWindow()
    app.mainloop()
