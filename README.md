## PyBook

Modern, simple contact book built with Python and Tkinter. Create, update, delete, and browse contacts with a clean dark UI. Data is saved automatically to `contacts.json` in the app folder, and you can import/export JSON via the File menu.

### Features
- **Simple CRUD**: Add/update via a single button, delete with confirmation, reset form instantly.
- **Clean dark UI**: `ttk` styling with a responsive grid layout.
- **Auto-persistence**: Contacts are saved to `contacts.json` after every change.
- **Import/Export**: Bring your data in, or back it up as JSON from the File menu.
- **Validation**: Name is required; phone accepts digits, spaces, `+ - ( )`.

### Requirements
- Python 3.8+
- Tkinter (included with standard Python on Windows/macOS; available on most Linux distros)

### Install dependencies (pip)
- This app uses only Python's standard library. **No pip packages are required.**
- If Tkinter is missing on Linux, install it via your system package manager:
  - Ubuntu/Debian: `sudo apt update && sudo apt install -y python3-tk`
  - Fedora: `sudo dnf install -y python3-tkinter`
  - Arch: `sudo pacman -S tk`
  - macOS/Windows: Tkinter comes with the official Python installer from `https://python.org`.

### How to run
On Windows:

```bash
python "pybook for contacts and addresses.py"
```

On macOS/Linux:

```bash
python3 "pybook for contacts and addresses.py"
```

No extra dependencies are required.

### How to use
1. **Add a contact**
   - Fill in `Name`, optionally `Phone`, and `Address`.
   - Click `Add`. The contact appears in the list.
2. **Update a contact**
   - Click a contact in the list; fields populate and the button says `Update`.
   - Edit fields and click `Update`.
3. **Delete a contact**
   - Select a contact and click `Delete`. Confirm to remove it.
4. **Reset the form**
   - Click `Reset` to clear inputs and exit edit mode.
5. **Import/Export JSON**
   - Use `File → Import JSON...` to load a list of contacts from a JSON file.
   - Use `File → Export JSON...` to save the current list to a JSON file.

### Data format
Contacts are stored as a JSON list of objects in `contacts.json` in the same folder as the app.

Example:

```json
[
  {
    "name": "Ada Lovelace",
    "phone": "+44 1234 567890",
    "address": "10 Downing St, London"
  },
  {
    "name": "Alan Turing",
    "phone": "(555) 0100",
    "address": "Bletchley Park"
  }
]
```

The importer is forgiving and will also accept legacy list entries like `[name, phone, address]` and normalize them internally.

### How it works
- The UI is implemented as a class, `ContactBookApp`, using `ttk` widgets laid out with grid.
- A single button toggles between `Add` and `Update` based on the current selection.
- Validation requires a non-empty name; phone uses a simple regex: digits, spaces, `+ - ( )`.
- Data is auto-saved to `contacts.json` after add/update/delete operations.
- Import/Export exposes JSON open/save dialogs for easy backup and migration.

### Tips
- You can resize the window; the list and text area expand accordingly.
- If you ever need a fresh start, close the app and delete `contacts.json` (this permanently removes saved contacts).



