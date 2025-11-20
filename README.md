# KOZTS Hyper League

Odświeżona, nowoczesna nakładka na ligę KOZTS, która dynamicznie scrappuje dane z `https://liga.kozts.pl/` i renderuje je w eleganckim interfejsie. Projekt działa jako lekki backend FastAPI + front typu single-page hostowany statycznie.

## Funkcje
- Live scraping fazy rozgrywek KOZTS (mecze, tabela drużyn, ranking indywidualny).
- Frontend w stylu "glassmorphism" z kartami, tabelami i toastami.
- API REST do dalszych integracji: `/api/phase/{id}`, `/api/phase/{id}/matches`, `/teams`, `/players`.
- Zapasowe dane demo dla fazy `364` (działa offline, gdy źródło jest niedostępne).

## Wymagania
- Python 3.11+
- Pakiety z `requirements.txt` (`pip install -r requirements.txt`).

## Skąd pobrać pliki projektu
- Wejdź w repozytorium (np. widok GitHub), kliknij zielony przycisk **Code** i wybierz **Download ZIP** – to pobierze cały folder na Twój komputer.
- Jeśli wolisz terminal i masz zainstalowanego gita: `git clone https://github.com/<twoja-nazwa-uzytkownika>/SocieTTy.git` (podmień adres na ten, pod którym hostujesz repo).
- Po pobraniu rozpakuj ZIP i przejdź do folderu `SocieTTy`.

## Uruchomienie
### Ekspresowa wersja (dla osób obytego z terminalem)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Potem wejdź w przeglądarce na `http://localhost:8000` i wpisz ID fazy z oryginalnej strony (np. `364`).

### Instrukcja „jak dla dziecka”
1. **Sprawdź, czy masz Pythona** – na Windows otwórz „Wiersz polecenia” i wpisz `python --version`. Jeśli nie działa, pobierz z [python.org/downloads](https://www.python.org/downloads/) i podczas instalacji zaznacz „Add Python to PATH”.
2. **Pobierz projekt** – kliknij „Code” → „Download ZIP” na GitHubie lub skopiuj folder z repozytorium. Rozpakuj go w dowolne miejsce.
3. **Otwórz folder w terminalu** – w Windows wpisz `cd C:\sciezka\do\SocieTTy`, w macOS/Linux `cd /ścieżka/do/SocieTTy`.
4. **Zainstaluj zależności** – skopiuj i wklej do terminala:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Uruchom serwer** – w tym samym terminalu wpisz:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Terminal powinien pokazać, że nasłuchuje na `http://127.0.0.1:8000`.
6. **Wejdź w przeglądarkę** – wpisz w pasku adresu `http://localhost:8000`. W formularzu podaj numer fazy (np. `364`) i kliknij pobieranie.
7. **Zatrzymanie** – zamknij serwer wciskając `Ctrl + C` w terminalu.

Jeśli coś pójdzie nie tak, upewnij się, że: (a) wirtualne środowisko jest aktywne (w terminalu widać `venv` na początku wiersza), (b) żaden inny program nie używa portu 8000, (c) jesteś połączony z internetem, aby scraper mógł pobrać dane.

## Jak to działa
- `kozts_scraper.service.KoztsScraper` pobiera HTML fazy i uruchamia parsery dla meczów, tabeli drużyn i zawodników.
- `kozts_scraper.parser` inteligentnie odczytuje nagłówki tabel (PL/EN), potrafi dopasować różne nazwy kolumn i parsuje daty w popularnych formatach.
- API zwraca ujednolicone struktury danych (`kozts_scraper.models`) gotowe do dalszego użycia.
- W razie problemów sieciowych dla fazy `364` zostaną zwrócone wbudowane dane z `kozts_scraper.sample_data`.

## Personalizacja
- Styl: edytuj `static/styles.css` i `static/index.html`.
- Logika scrapowania: dodaj kolejne selektory lub transformacje w `kozts_scraper/parser.py`.
- Endpointy: rozbuduj FastAPI w `app/main.py` o kolejne trasy lub filtrowanie.
