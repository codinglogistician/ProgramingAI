

# **Zadanie: Dodanie miasta Kraków + refaktor workflow**

Opcjonalnie (fork https://github.com/marcin119a/scraper) lub swoje repozytorium
## 1. **Dodaj obsługę miasta Kraków w istniejącym workflow GitHub Actions**

W obecnym pliku `.github/workflows/weekly-scraper.yml`:

* po sekcji dotyczącej Łodzi
* dodaj analogiczny blok dla miasta **Kraków**
* scraper powinien zostać uruchomiony z parametrami:

  * `--city krakow`
  * `--pages 10`
  * zapisz wyniki do:

    * `scraper/data/ogloszenia_krakow.csv`
* dodaj etap wysyłki artefaktów podobny do pozostałych miast

## 2. **Wykonaj refaktor z użyciem kursora workflow (drugi etap)**

Po dodaniu Krakowa:

* zrefaktoruj cały workflow, aby usunąć powtarzalność

* użyj **GitHub Actions matrix strategy**, aby automatycznie obsługiwać wiele miast

## 3. **Efekt końcowy**

* workflow najpierw działa w starej formie (z dopisanym Krakowem)
* po refaktorze workflow ma być krótszy, czytelniejszy i łatwy w rozbudowie
* dodanie nowego miasta po refaktorze sprowadza się do dopisania jednego wpisu w matrix

---
