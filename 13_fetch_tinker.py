import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
import webbrowser

MAX_PER_ROW = 1  # dla wrap-style
IMAGE_SIZE = (200, 200)

def fetch_nasa_images(query):
    url = "https://images-api.nasa.gov/search"
    params = {"q": query, "media_type": "image"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("collection", {}).get("items", [])[:5]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Błąd połączenia", str(e))
    except Exception as e:
        messagebox.showerror("Błąd", str(e))
    return []

def open_image_window(img_data, title="Obraz"):
    new_win = tk.Toplevel()
    new_win.title(title)

    img = Image.open(io.BytesIO(img_data))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(new_win, image=photo)
    label.image = photo  # Trzyma referencję
    label.pack(padx=10, pady=10)

def get_image_thumbnail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        img.thumbnail(IMAGE_SIZE)
        return ImageTk.PhotoImage(img), response.content  # thumbnail i oryginalne dane
    except:
        return None, None

def show_results(query, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    if not query.strip():
        messagebox.showwarning("Uwaga", "Wpisz zapytanie!")
        return

    items = fetch_nasa_images(query)
    if not items:
        label = tk.Label(frame, text="Brak wyników.", font=("Arial", 12))
        label.grid(row=0, column=0)
        return

    for i, item in enumerate(items):
        title = item.get("data", [{}])[0].get("title", "Brak tytułu")
        image_url = item.get("links", [{}])[0].get("href", "")

        thumb, full_data = get_image_thumbnail(image_url)

        row = i // MAX_PER_ROW
        col = (i % MAX_PER_ROW) * 2

        title_label = tk.Label(frame, text=f"{i+1}. {title}", font=("Arial", 10, "bold"), wraplength=400, justify="left")
        title_label.grid(row=row*3, column=col, sticky="w", padx=10, pady=5)

        if thumb:
            img_button = tk.Label(frame, image=thumb, cursor="hand2")
            img_button.image = thumb  # zapamiętaj miniaturę
            img_button.grid(row=row*3+1, column=col, padx=10, pady=5, sticky="w")
            img_button.bind("<Button-1>", lambda e, d=full_data, t=title: open_image_window(d, t))

        link_label = tk.Label(frame, text=image_url, fg="blue", cursor="hand2", wraplength=400)
        link_label.grid(row=row*3+2, column=col, sticky="w", padx=10, pady=2)
        link_label.bind("<Button-1>", lambda e, url=image_url: webbrowser.open(url))

def main():
    root = tk.Tk()
    root.title("NASA Image Search")
    root.geometry("700x500")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Wpisz zapytanie:").pack(side=tk.LEFT, padx=5)
    query_entry = tk.Entry(input_frame, width=40)
    query_entry.pack(side=tk.LEFT, padx=5)
    query_entry.focus()

    result_frame = tk.Frame(root)
    result_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(result_frame)
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    search_button = tk.Button(root, text="Szukaj", command=lambda: show_results(query_entry.get(), scrollable_frame))
    search_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
