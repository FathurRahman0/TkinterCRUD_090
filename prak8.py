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

def updatenilai(id, name, biologi, fisika, inggris):
    con = koneksi()
    cur = con.cursor()
    hasil = prediksi_jurusan(biologi, fisika, inggris)
    cur.execute(""" 
        UPDATE students SET name = ?, biologi = ?, fisika = ?, inggris = ?, prediksi = ? 
        WHERE id = ?""", (name, biologi, fisika, inggris, hasil, id))
    con.commit()
    con.close()

def deletenilai(id):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (id,))
    con.commit()
    con.close()

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

        self.btn_edit = tk.Button(btn_frame, text="Edit", width=10, command=self.edit_selected)
        self.btn_edit.pack(side="left", padx=6)
        self.btn_delete = tk.Button(btn_frame, text="Hapus", width=10, command=self.delete_selected)
        self.btn_delete.pack(side="left", padx=6)

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
    
    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            msg.showwarning("Peringatan", "Pilih data dulu!")
            return None
        return self.tree.item(sel[0])["values"]

    def edit_selected(self):
        sel = self.get_selected()
        if not sel:
            return
        record_id, nama, bio, fis, ing, prediksi = sel

        win = tk.Toplevel(self)
        win.title(f'Edit Entri ID {record_id}')
        win.transient(self)
        win.grab_set()
        win.geometry('420x260')
        ttk.Label(win, text=f'Edit data ID{record_id}', style='Header.TLabel').pack(anchor='w', padx=12, pady=(10,5))

        frm = ttk.Frame(win, padding=12)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text='Nama: ').grid(row=0, column=0, sticky='w')
        e_nama = ttk.Entry(frm, width=40)
        e_nama.grid(row=0, column=1, pady=6)
        e_nama.insert(0, nama)

        ttk.Label(frm, text='Biologi: ').grid(row=1, column=0, sticky='w')
        e_bio = ttk.Entry(frm, width=12)
        e_bio.grid(row=1, column=1, pady=6)
        e_bio.insert(0, bio)

        ttk.Label(frm, text='Fisika: ').grid(row=2, column=0, sticky='w')
        e_fis = ttk.Entry(frm, width=12)
        e_fis.grid(row=2, column=1, pady=6)
        e_fis.insert(0, fis)

        ttk.Label(frm, text='Inggris: ').grid(row=3, column=0, sticky='w')
        e_ing = ttk.Entry(frm, width=12)
        e_ing.grid(row=3, column=1, pady=6)
        e_ing.insert(0, ing)

        def save_changes():
            try:
                name = e_nama.get().strip()
                b = int(e_bio.get().strip())
                f = int(e_fis.get().strip())
                i = int(e_ing.get().strip())

                if not name:
                    msg.showerror("Error", "Nama tidak boleh kosong")
                    return

                updatenilai(record_id, name, b, f, i)
                msg.showinfo("Sukses", "Data berhasil diperbarui")
                self.read_data()
                win.destroy()
            except ValueError:
                msg.showerror("Error", "Nilai harus angka!")
            except Exception as e:
                msg.showerror("DB Error", str(e))

        btn_frame = tk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(8,0))

        tk.Button(btn_frame, text="Simpan Perubahan", width=16, command=save_changes).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Batal", width=10, command=win.destroy).pack(side="left", padx=6)
    
    def delete_selected(self):
        sel = self.get_selected()
        if not sel:
            return
        record_id = sel[0]
        if msg.askyesno("Konfirmasi", f"Yakin ingin menghapus data ID {record_id}?"):
            try:
                deletenilai(record_id)
                self.read_data()
                msg.showinfo("Sukses", "Data berhasil dihapus.")
            except Exception as e:
                msg.showerror("DB Error", str(e))

if __name__ =="__main__":
    app = Nilai()
    app.mainloop()