
# **Zadanie: Dodanie miasta Szczecin + refaktor workflow + praca w GitFlow**

### **Repozytorium:**

* użyj forka repozytorium:
  [https://github.com/marcin119a/scraper](https://github.com/marcin119a/scraper)
  *lub własnego repo z podobną strukturą*

---

# **Cel zadania**

1. Wprowadzić nową funkcjonalność — obsługę miasta **Szczecin**
2. Przeprowadzić **refaktor workflow GitHub Actions**
3. Zrobić to zgodnie z **GitFlow**, pracując na osobnych branchach
4. Dostarczyć PR-y, które zostaną zreviewowane i połączone.

---

# **1. Przygotowanie branchy (GitFlow)**

W repo wykonaj:

### **A. Stwórz brancha dla nowej funkcjonalności:**

```
git checkout develop
git pull
git checkout -b feature/add-szczecin-scraping
```

---

# **2. Etap 1 — Dodanie Szczecin do obecnego workflow**

W pliku:

```
.github/workflows/weekly-scraper.yml
```

* po sekcji dotyczącej Łodzi dodaj sekcję dla **Szczecin**
* scraper powinien zostać uruchomiony z:

```
--city szczecin
--pages 10
```

* zapisz dane do:

```
scraper/data/ogloszenia_szczecin.csv
```

* dodaj blok uploadu artefaktów identyczny jak dla pozostałych miast

### Po zakończeniu:

1. Zacommituj zmiany
2. Otwórz Pull Request do `develop`:

**PR: `feature/add-szczecin-scraping` → `develop`**

PR powinien zawierać:

* opis zmian,
* dlaczego zostały wprowadzone,
* co zostało dodane i gdzie.

---
