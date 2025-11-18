import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

def koneksi():
    con = sqlite3.connect("nilai.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi TEXT
    )
    """)
    con.commit()
    con.close()

def insertsiswa(name: str, biologi: int, fisika: int, inggris: int, prediksi: str):

    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO students (name, biologi, fisika, inggris, prediksi) VALUES (?, ?, ?, ?, ?)", (name, biologi, fisika, inggris, prediksi))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

def readsiswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, name, biologi, fisika, inggris, prediksi FROM students ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

def prediksi_jurusan(biologi, fisika, inggris):
    if biologi >= fisika and biologi >= inggris:
        return "Kedokteran"
    elif fisika >= biologi and fisika >= inggris:
        return "Teknik"
    else:
        return "Bahasa"


create_table()

class Nilai(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insert dan Read Data Nilai")
        self.geometry("600x420")

        frm = tk.Frame(self, bg="#ffffff", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        tk.Label(frm, text="nama:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="biologi:", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_biologi = tk.Entry(frm, width=30)
        self.ent_biologi.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="fisika:", bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.ent_fisika = tk.Entry(frm, width=30)
        self.ent_fisika.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Inggris:", bg="#ffffff").grid(row=3, column=0, sticky="w")
        self.ent_inggris = tk.Entry(frm, width=30)
        self.ent_inggris.grid(row=3, column=1, sticky="w", padx=6, pady=6)

        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(10,10))

        self.btn_add = tk.Button(btn_frame, text="Tambah", width=10, command=self.insertdata)
        self.btn_add.pack(side="left", padx=6)
        self.btn_refresh = tk.Button(btn_frame, text="Refresh", width=10, command=self.read_data)
        self.btn_refresh.pack(side="left", padx=6)

        cols = ("id", "name", "biologi", "fisika", "inggris", "prediksi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        self.tree.heading("name", text="Nama")
        self.tree.column("name", width=80)
        self.tree.heading("biologi", text="biologi")
        self.tree.column("biologi", width=40, anchor="center")
        self.tree.heading("fisika", text="fisika")
        self.tree.column("fisika", width=40, anchor="center")
        self.tree.heading("inggris", text="inggris")
        self.tree.column("inggris", width=40, anchor="center")
        self.tree.heading("prediksi", text="Prediksi Fakultas")
        self.tree.column("prediksi", width=120, anchor="center")
        self.tree.pack(padx=16, pady=(0,12), fill="both", expand=True)


        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.read_data()

    def clear_inputs(self):
        self.ent_name.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        biologi_str = self.ent_biologi.get().strip()
        fisika_str = self.ent_fisika.get().strip()
        inggris_str = self.ent_inggris.get().strip()
        if not name or not biologi_str or not fisika_str or not inggris_str:
            msg.showwarning("Peringatan", "Nama dan nilai-nilai tidak boleh kosong.")
            return None
        try:
            biologi = int(biologi_str)
            fisika = int(fisika_str)
            inggris = int(inggris_str)
            if biologi < 0 or fisika < 0 or inggris < 0:
                raise ValueError
        except ValueError:
            msg.showerror("Salah", "Nilai harus bilangan bulat >= 0.")
            return None
        return name, biologi, fisika, inggris

    def insertdata(self):
        val = self.validate_inputs()
        if not val:
            return
        name, biologi, fisika, inggris = val
        try:
            prediksi = prediksi_jurusan(biologi, fisika, inggris)
            new_id = insertsiswa(name, biologi, fisika, inggris, prediksi)
            msg.showinfo("Sukses", f"Data disimpan (id={new_id}).")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def on_tree_select(self):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _, name, biologi, fisika, inggris = item["values"]
        self.ent_name.insert(0, name)
        self.ent_biologi.insert(0, str(biologi))
        self.ent_fisika.insert(0, str(fisika))
        self.ent_inggris.insert(0, str(inggris))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readsiswa()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))

if __name__ =="__main__":
    app = Nilai()
    app.mainloop()