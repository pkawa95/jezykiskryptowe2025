import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import os

custom_logo_path = None  # Ścieżka do własnego loga

def generate_qr_code(data, logo_path=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        qr_width, qr_height = qr_img.size
        size = qr_width // 4
        logo = logo.resize((size, size), Image.LANCZOS)

        pos = ((qr_width - size) // 2, (qr_height - size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    return qr_img

def upload_logo():
    global custom_logo_path
    file_path = filedialog.askopenfilename(
        title="Wybierz plik z logiem",
        filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg")]
    )
    if file_path:
        custom_logo_path = file_path
        logo_label.config(text=f"Załadowano: {os.path.basename(file_path)}")

def show_qr():
    data = entry.get()
    if not data.strip():
        messagebox.showwarning("Błąd", "Wprowadź dane do zakodowania.")
        return

    img = generate_qr_code(data, custom_logo_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk
    qr_label.qr_image = img  # zapamiętaj oryginalny obraz

def save_qr():
    if not hasattr(qr_label, "qr_image"):
        messagebox.showwarning("Brak kodu", "Najpierw wygeneruj kod QR.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        qr_label.qr_image.save(file_path)
        messagebox.showinfo("Zapisano", f"Zapisano kod QR jako:\n{file_path}")

def main():
    global entry, qr_label, logo_label

    root = tk.Tk()
    root.title("Generator kodów QR z własnym logiem")
    root.geometry("420x600")
    root.resizable(False, False)

    tk.Label(root, text="Wprowadź tekst lub link:").pack(pady=5)
    entry = tk.Entry(root, width=45)
    entry.pack(pady=5)
    entry.focus()

    tk.Button(root, text="Wgraj własne logo", command=upload_logo).pack(pady=10)
    logo_label = tk.Label(root, text="Nie wybrano loga", fg="gray")
    logo_label.pack()

    tk.Button(root, text="Generuj kod QR", command=show_qr).pack(pady=15)

    qr_label = tk.Label(root)
    qr_label.pack(pady=20)

    # Przenosimy zapis niżej, żeby nie nachodził na obraz
    tk.Button(root, text="Zapisz jako PNG", command=save_qr).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
