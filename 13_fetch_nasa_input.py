import requests

def fetch_nasa_images(query):
    url = "https://images-api.nasa.gov/search"
    params = {"q": query, "media_type": "image"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        items = data.get("collection", {}).get("items", [])

        if not items:
            print("Brak wyników dla zapytania:", query)
            return

        for i, item in enumerate(items[:5]):
            title = item.get("data", [{}])[0].get("title", "Brak tytułu")
            image_link = item.get("links", [{}])[0].get("href", "Brak linku")

            print(f"\nObraz {i+1}:")
            print("Tytuł:", title)
            print("Link :", image_link)

    except requests.exceptions.RequestException as e:
        print("Błąd połączenia z API NASA:", e)
    except Exception as e:
        print("Wystąpił błąd podczas przetwarzania danych:", e)


def main():
    query = input("Wpisz zapytanie do wyszukiwarki NASA (np. Supernova): ")
    if not query.strip():
        print("Nie podano zapytania.")
        return
    print(f"\nWyszukiwanie obrazów dla zapytania: \"{query}\"\n")
    fetch_nasa_images(query)


if __name__ == "__main__":
    main()
