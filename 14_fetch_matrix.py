import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
import webbrowser
import json

IMAGE_SIZE = (200, 200)
MAX_IMAGES_PER_PAGE= 3
IMAGES_PER_ROW= 3


def fetch_nasa_images(query, num_results):
    url = "https://images-api.nasa.gov/search"
    params = {
        "q": query,
        "media_type": "image"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("collection", {}).get("items", [])[:num_results]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Błąd połączenia", str(e))
    except Exception as e:
        messagebox.showerror("Błąd", str(e))
    return []


def get_image_thumbnail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        img.thumbnail(IMAGE_SIZE)
        return ImageTk.PhotoImage(img), response.content
    except:
        return None, None


def update_preview(image_data, image_label, image_frame):
    try:
        img = Image.open(io.BytesIO(image_data))
        frame_width = image_frame.winfo_width()
        frame_height = image_frame.winfo_height()

        if frame_width == 1:
            frame_width = 400
            frame_height = 400

        img.thumbnail((frame_width - 20, frame_height - 20))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    except Exception as e:
        print(f"Błąd podglądu: {e}")


def update_metadata(title, metadata, title_label, json_data):
    title_label.config(text=title)
    json_data.config(state="normal")
    json_data.delete("1.0", tk.END)
    json_data.insert(tk.END, json.dumps(metadata, indent=4, ensure_ascii=False))
    json_data.config(state="disabled")


def show_results(query, num_results, scrollable_frame, title_label, json_data, image_label, image_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if not query.strip():
        messagebox.showwarning("Uwaga", "Wpisz zapytanie!")
        return

    items = fetch_nasa_images(query, num_results)
    if not items:
        label = tk.Label(scrollable_frame, text="Brak wyników.", font=("Arial", 12), fg="green", bg="black")
        label.pack()
        return

    for i, item in enumerate(items):
        title = item.get("data", [{}])[0].get("title", "Brak tytułu")
        image_url = item.get("links", [{}])[0].get("href", "")

        thumb, full_data = get_image_thumbnail(image_url)

        title_label_widget = tk.Label(scrollable_frame, text=f"{i+1}. {title}", font=("Courier", 10, "bold"), fg="green", bg="black", wraplength=200, justify="left")
        title_label_widget.pack(padx=5, pady=2, anchor="w")

        if thumb:
            img_button = tk.Label(scrollable_frame, image=thumb, cursor="hand2", bg="black")
            img_button.image = thumb
            img_button.pack(padx=5, pady=2, anchor="w")
            img_button.bind("<Button-1>", lambda e, d=full_data, t=title, m=item.get("data", [{}])[0]: (update_preview(d, image_label, image_frame), update_metadata(t, m, title_label, json_data)))

        link_label = tk.Label(scrollable_frame, text=image_url, fg="cyan", bg="black", cursor="hand2", wraplength=200)
        link_label.pack(padx=5, pady=2, anchor="w")
        link_label.bind("<Button-1>", lambda e, url=image_url: webbrowser.open(url))


def main():
    root = tk.Tk()
    root.title("NASA Matrix Viewer")
    root.configure(bg="black")
    root.geometry("1200x600")
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # INPUT
    input_frame = tk.Frame(root, bg="black")
    input_frame.grid(row=0, column=0, sticky="ew")

    tk.Label(input_frame, text="Zapytanie:", fg="green", bg="black").pack(side=tk.LEFT, padx=5)
    query_entry = tk.Entry(input_frame, width=30, bg="black", fg="green", insertbackground="green")
    query_entry.pack(side=tk.LEFT, padx=5)
    query_entry.focus()

    tk.Label(input_frame, text="Ilość:", fg="green", bg="black").pack(side=tk.LEFT, padx=5)
    num_results_entry = tk.Entry(input_frame, width=5, bg="black", fg="green", insertbackground="green")
    num_results_entry.insert(0, "9")
    num_results_entry.pack(side=tk.LEFT, padx=5)

    # MAIN GRID
    main_frame = tk.Frame(root, bg="black")
    main_frame.grid(row=1, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=2)  # LEFT
    main_frame.columnconfigure(1, weight=3)  # CENTER
    main_frame.columnconfigure(2, weight=2)  # RIGHT
    main_frame.rowconfigure(0, weight=1)

    # COLUMN 1 - MINIATURY + SCROLL
    left_container = tk.Frame(main_frame, bg="black")
    left_container.grid(row=0, column=0, sticky="nsew")

    canvas = tk.Canvas(left_container, bg="black", highlightthickness=0)
    scrollbar = tk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="black")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # COLUMN 2 - PODGLĄD
    image_frame = tk.Frame(main_frame, bg="black")
    image_frame.grid(row=0, column=1, sticky="nsew")
    image_frame.rowconfigure(0, weight=1)
    image_frame.columnconfigure(0, weight=1)
    image_label = tk.Label(image_frame, bg="black")
    image_label.pack(expand=True, fill="both")

    # COLUMN 3 - METADANE
    right_frame = tk.Frame(main_frame, bg="black")
    right_frame.grid(row=0, column=2, sticky="nsew")

    title_label = tk.Label(right_frame, text="", font=("Courier", 12, "bold"), fg="green", bg="black", wraplength=250, justify="left")
    title_label.pack(padx=5, pady=5, anchor="nw")

    json_data = tk.Text(right_frame, wrap="word", height=25, width=40, bg="black", fg="green")
    json_data.pack(padx=5, pady=5, expand=True, fill="both")
    json_data.config(state="disabled")

    search_button = tk.Button(input_frame, text="Szukaj", bg="black", fg="green", command=lambda: show_results(query_entry.get(), int(num_results_entry.get()), scrollable_frame, title_label=title_label, json_data=json_data, image_label=image_label, image_frame=image_frame))
    search_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()
