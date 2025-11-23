### Zadanie: Implementacja endpointa MCP do predykcji cen mieszkań

Twoim zadaniem jest rozszerzenie istniejącego serwera **FastMCP** o nowy endpoint służący do **predykcji ceny mieszkania** na podstawie cech nieruchomości i dodanie bazy danych do starego entpointa. 

#### Kontekst

Masz już działający kod, który:

* czyści dane z pliku CSV (`adresowo_warszawa_wroclaw.csv`),
* trenuje model `RandomForestRegressor`,
* zapisuje model do pliku `model.pkl`,
* potrafi go wczytać i wykorzystać do predykcji.

Aktualnie w serwerze MCP istnieją dwa proste endpointy:

* `add(a, b)` – dodaje liczby,
* `multiply(a, b)` – mnoży liczby.

#### Twoje zadanie

1. Dodaj nowy endpoint MCP o nazwie **`predict_price`**, który będzie:

   * przyjmował parametry opisujące mieszkanie:

     * `rooms` (liczba pokoi, int),
     * `area_m2` (powierzchnia w m², float),
     * `locality` (dzielnica, str),
     * `street` (ulica, str),
     * `property_type` (typ nieruchomości, str, np. „Mieszkanie”),
     * `city` (miasto, str),
     * `photos` (liczba zdjęć w ogłoszeniu, int),
   * przygotowywał ramkę danych (`pandas.DataFrame`) z tymi parametrami,
   * kodował zmienne kategoryczne w taki sam sposób jak w procesie trenowania,
   * używał wytrenowanego modelu (`RandomForestRegressor` z pliku `model.pkl`) do predykcji,
   * zwracał przewidywaną cenę mieszkania w złotówkach (`float`).

2. Upewnij się, że:

   * model wczytuje się z pliku `model.pkl` (jeśli plik nie istnieje – wytrenuj model i zapisz go),
   * endpoint działa analogicznie do `add` i `multiply`, tj. jest udekorowany adnotacją `@mcp.tool()`,
   * serwer MCP startuje komendą:

     ```bash
     python app.py
     ```

     i komunikuje się przez `stdio`.

3. Sprawdź wywołanie się modelu. 
4. Dodaj bazę danych do Twojego rozwiązania. 
---

