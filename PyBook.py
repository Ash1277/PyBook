import json #for writing contact data to a JSON file
import re #for regular expression validation of the phone number format.
import tkinter as tk #The main GUI library
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path #For platform-independent handling of the data file path.


class ContactBookApp:

	DATA_FILE = Path("contacts.json")

	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("PyBook - Contacts")
		self.root.geometry("520x520")
		self.root.minsize(520, 520)

		self.contacts = []
		self.selected_index = None

		self._create_vars()
		self._create_widgets()
		self._layout_widgets()
		self._bind_events()
		self._load()
		self._refresh_list()
		self._apply_dark_theme()

	def _create_vars(self) -> None:
		self.name_var = tk.StringVar()
		self.phone_var = tk.StringVar()

	def _create_widgets(self) -> None:
		self.container = ttk.Frame(self.root, padding=12)

		self.name_label = ttk.Label(self.container, text="Name")
		self.name_entry = ttk.Entry(self.container, textvariable=self.name_var, width=40)

		self.phone_label = ttk.Label(self.container, text="Phone")
		self.phone_entry = ttk.Entry(self.container, textvariable=self.phone_var, width=40)

		self.addr_label = ttk.Label(self.container, text="Address")
		self.addr_text = tk.Text(self.container, width=40, height=8, wrap=tk.WORD)

		self.add_update_btn = ttk.Button(self.container, text="Add", command=self.on_add_or_update)
		self.delete_btn = ttk.Button(self.container, text="Delete", command=self.on_delete)
		self.reset_btn = ttk.Button(self.container, text="Reset", command=self.on_reset)

		self.list_label = ttk.Label(self.container, text="Contacts")
		self.scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL)
		self.listbox = tk.Listbox(
			self.container,
			listvariable=tk.StringVar(),
			height=14,
			yscrollcommand=self.scrollbar.set,
		)
		self.scrollbar.config(command=self.listbox.yview)

		self._create_menu()

	def _create_menu(self) -> None:
		menubar = tk.Menu(self.root)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Import JSON...", command=self.on_import)
		filemenu.add_command(label="Export JSON...", command=self.on_export)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.root.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		self.root.config(menu=menubar)

	def _layout_widgets(self) -> None:
		self.container.grid(column=0, row=0, sticky="nsew")
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		for i in range(4):
			self.container.columnconfigure(i, weight=1)
		for i in range(8):
			self.container.rowconfigure(i, weight=0)
		self.container.rowconfigure(7, weight=1)

		self.name_label.grid(column=0, row=0, sticky="w", padx=(0, 8), pady=(0, 6))
		self.name_entry.grid(column=1, row=0, columnspan=3, sticky="ew", pady=(0, 6))

		self.phone_label.grid(column=0, row=1, sticky="w", padx=(0, 8), pady=(0, 6))
		self.phone_entry.grid(column=1, row=1, columnspan=3, sticky="ew", pady=(0, 6))

		self.addr_label.grid(column=0, row=2, sticky="nw", padx=(0, 8))
		self.addr_text.grid(column=1, row=2, columnspan=3, sticky="nsew")

		self.add_update_btn.grid(column=1, row=3, sticky="w", pady=8)
		self.delete_btn.grid(column=2, row=3, sticky="w", pady=8)
		self.reset_btn.grid(column=3, row=3, sticky="e", pady=8)

		self.list_label.grid(column=0, row=4, sticky="w", pady=(8, 0))
		self.listbox.grid(column=0, row=5, columnspan=4, sticky="nsew")
		self.scrollbar.grid(column=4, row=5, sticky="nsw")

	def _bind_events(self) -> None:
		self.listbox.bind("<<ListboxSelect>>", self.on_select)
		self.listbox.bind("<Double-Button-1>", self.on_double_click)

	def _apply_dark_theme(self) -> None:
		style = ttk.Style(self.root)
		# Use a stable base theme before customizing
		try:
			style.theme_use("clam")
		except Exception:
			pass
		bg = "#1e1f22"
		fg = "#ffffff"
		muted = "#a9b0b8"
		accent = "#4c92ff"
		self.root.configure(bg=bg)
		self.container.configure(style="Dark.TFrame")
		style.configure("Dark.TFrame", background=bg)
		style.configure("Dark.TLabel", background=bg, foreground=fg)
		style.configure("Dark.TButton", foreground=fg)
		style.map("Dark.TButton", foreground=[("active", fg)], background=[("active", "#2a2d31")])
		style.configure("Dark.TEntry", fieldbackground="#2a2d31", foreground=fg)
		# Apply styles to widgets
		for label in (self.name_label, self.phone_label, self.addr_label, self.list_label):
			label.configure(style="Dark.TLabel")
		for btn in (self.add_update_btn, self.delete_btn, self.reset_btn):
			btn.configure(style="Dark.TButton")
		self.name_entry.configure(style="Dark.TEntry")
		self.phone_entry.configure(style="Dark.TEntry")
		# Non-ttk widgets require direct config
		self.addr_text.configure(bg="#2a2d31", fg=fg, insertbackground=fg)
		self.listbox.configure(bg="#2a2d31", fg=fg, selectbackground=accent, selectforeground="#000000", highlightthickness=0)
		self.scrollbar.configure()

	def on_add_or_update(self) -> None:
		name = self.name_var.get().strip()
		phone = self.phone_var.get().strip()
		addr = self.addr_text.get("1.0", "end-1c").strip()

		if not name:
			messagebox.showwarning("Validation", "Name is required.")
			return
		if phone and not self._is_valid_phone(phone):
			messagebox.showwarning("Validation", "Phone may contain digits, spaces, +, -, ().")
			return

		contact = {"name": name, "phone": phone, "address": addr}

		if self.selected_index is not None:
			self.contacts[self.selected_index] = contact
		else:
			self.contacts.append(contact)

		self._save()
		self._refresh_list()
		self.on_reset()

	def on_delete(self) -> None:
		if self.selected_index is None:
			messagebox.showinfo("Delete", "Select a contact to delete.")
			return
		name = self.contacts[self.selected_index]["name"]
		if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
			del self.contacts[self.selected_index]
			self.selected_index = None
			self._save()
			self._refresh_list()
			self.on_reset()

	def on_reset(self) -> None:
		self.name_var.set("")
		self.phone_var.set("")
		self.addr_text.delete("1.0", "end")
		self.add_update_btn.config(text="Add")
		self.listbox.selection_clear(0, tk.END)
		self.selected_index = None

	def on_select(self, event=None) -> None:
		selection = self.listbox.curselection()
		if not selection:
			return
		index = int(selection[0])
		self.selected_index = index
		contact = self.contacts[index]
		self.name_var.set(contact.get("name", ""))
		self.phone_var.set(contact.get("phone", ""))
		self.addr_text.delete("1.0", "end")
		self.addr_text.insert("1.0", contact.get("address", ""))
		self.add_update_btn.config(text="Update")

	def on_double_click(self, event=None) -> None:
		self.on_select()

	def on_import(self) -> None:
		file_path = filedialog.askopenfilename(
			title="Import contacts JSON",
			filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")),
		)
		if not file_path:
			return
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				data = json.load(f)
				if isinstance(data, list):
					self.contacts = self._normalize_contacts(data)
					self._save()
					self._refresh_list()
					self.on_reset()
				else:
					raise ValueError("Invalid JSON format: expected a list")
		except Exception as exc:
			messagebox.showerror("Import failed", str(exc))

	def on_export(self) -> None:
		file_path = filedialog.asksaveasfilename(
			title="Export contacts JSON",
			defaultextension=".json",
			filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")),
		)
		if not file_path:
			return
		try:
			with open(file_path, "w", encoding="utf-8") as f:
				json.dump(self.contacts, f, indent=2, ensure_ascii=False)
		except Exception as exc:
			messagebox.showerror("Export failed", str(exc))

	def _refresh_list(self) -> None:
		self.listbox.delete(0, tk.END)
		for contact in self.contacts:
			name = contact.get("name", "")
			phone = contact.get("phone", "")
			display = f"{name}" + (f"  —  {phone}" if phone else "")
			self.listbox.insert(tk.END, display)

	def _is_valid_phone(self, phone: str) -> bool:
		return bool(re.fullmatch(r"[0-9+()\-\s]+", phone))

	def _normalize_contacts(self, data):
		normalized = []
		for item in data:
			if isinstance(item, dict):
				name = str(item.get("name", "")).strip()
				phone = str(item.get("phone", "")).strip()
				addr = str(item.get("address", "")).strip()
				normalized.append({"name": name, "phone": phone, "address": addr})
			elif isinstance(item, (list, tuple)) and len(item) >= 3:
				name, phone, addr = item[0], item[1], item[2]
				normalized.append({"name": str(name), "phone": str(phone), "address": str(addr)})
		return normalized

	def _load(self) -> None:
		if self.DATA_FILE.exists():
			try:
				with open(self.DATA_FILE, "r", encoding="utf-8") as f:
					self.contacts = self._normalize_contacts(json.load(f))
			except Exception:
				self.contacts = []

	def _save(self) -> None:
		try:
			with open(self.DATA_FILE, "w", encoding="utf-8") as f:
				json.dump(self.contacts, f, indent=2, ensure_ascii=False)
		except Exception:
			pass


def main() -> None:
	root = tk.Tk()
	ContactBookApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()