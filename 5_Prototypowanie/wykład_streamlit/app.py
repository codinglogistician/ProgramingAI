import joblib
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime

# Mapowanie lokalizacji na format URL adresowo.pl
LOCALITY_URL_MAP = {
    "Łódź Bałuty": "lodz-baluty",
    "Łódź Górna": "lodz-gorna",
    "Łódź Śródmieście": "lodz-srodmiescie",
    "Łódź Widzew": "lodz-widzew",
    "Łódź Polesie": "lodz-polesie"
}

# Wartości domyślne (fallback)
DEFAULT_MARKET_PRICES = {
    "Łódź Bałuty": 380000,
    "Łódź Górna": 420000,
    "Łódź Śródmieście": 500000,
    "Łódź Widzew": 450000,
    "Łódź Polesie": 400000
}

# Nagłówki HTTP, aby udawać przeglądarkę
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

BASE_URL = 'https://adresowo.pl'


def parse_price(price_text):
    """Parsuje tekst ceny do liczby (usuwa spacje, znaki itp.)"""
    if not price_text:
        return None
    # Usuń wszystkie znaki oprócz cyfr
    price_clean = re.sub(r'[^\d]', '', price_text.replace('\xa0', '').replace(' ', ''))
    try:
        return float(price_clean) if price_clean else None
    except ValueError:
        return None


def scrape_market_prices(pages=8, progress_callback=None):
    """Scrapuje średnie ceny rynkowe z adresowo.pl dla wszystkich lokalizacji"""
    market_prices = {}
    total_locations = len(LOCALITY_URL_MAP)
    
    with requests.Session() as session:
        session.headers.update(HTTP_HEADERS)
        
        for idx, (locality, url_suffix) in enumerate(LOCALITY_URL_MAP.items()):
            if progress_callback:
                progress_callback((idx + 0.1) / total_locations, f"Scrapowanie {locality}...")
            
            prices = []
            
            # Scrapuj strony dla danej lokalizacji
            for page_num in range(1, pages + 1):
                url = f'{BASE_URL}/mieszkania/{url_suffix}/_l{page_num}'
                
                try:
                    response = session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    listings = soup.select('section.search-results__item')
                    
                    if not listings:
                        break
                    
                    # Parsuj ceny z ogłoszeń
                    for item in listings:
                        try:
                            price_total_tag = item.select_one('.result-info__price--total span')
                            if price_total_tag:
                                price_text = price_total_tag.get_text(strip=True).replace('\xa0', '')
                                price = parse_price(price_text)
                                if price:
                                    prices.append(price)
                        except Exception as e:
                            continue
                    
                    # Opóźnienie między requestami
                    time.sleep(0.5)
                    
                except requests.RequestException as e:
                    continue
            
            # Oblicz średnią cenę dla lokalizacji
            if prices:
                market_prices[locality] = sum(prices) / len(prices)
            else:
                # Użyj wartości domyślnej jeśli nie znaleziono danych
                market_prices[locality] = DEFAULT_MARKET_PRICES.get(locality, 400000)
            
            if progress_callback:
                progress_callback((idx + 1) / total_locations, f"Zakończono {locality}")
    
    return market_prices


@st.cache_data
def load_model():
    """Cache'uje wczytanie modelu"""
    return joblib.load("best_random_forest_model.pkl")


def predict_price(area_m2, rooms, photos, locality):
    # Wczytanie modelu z cache
    model = load_model()
    # Kolejność kolumn zgodna z treningiem: area_m2, locality, rooms, photos
    X_new = pd.DataFrame([[area_m2, locality, rooms, photos]],
                         columns=['area_m2', 'locality', 'rooms', 'photos'])
    return model.predict(X_new)[0]

def main():
   st.title("Predykcja ceny mieszkania (Adresowo)")
   st.write("Podaj dane mieszkania, aby uzyskać szacowaną cenę:")

   # Inicjalizacja session_state dla cache'owania cen
   if 'market_prices' not in st.session_state:
       st.session_state.market_prices = DEFAULT_MARKET_PRICES.copy()
   if 'last_scraped' not in st.session_state:
       st.session_state.last_scraped = None
   if 'scraping_in_progress' not in st.session_state:
       st.session_state.scraping_in_progress = False

   # Sekcja scrapowania cen rynkowych
   st.sidebar.header("Ceny rynkowe")
   
   if st.sidebar.button("Pobierz aktualne ceny rynkowe"):
       st.session_state.scraping_in_progress = True
       progress_bar = st.sidebar.progress(0)
       status_text = st.sidebar.empty()
       
       def update_progress(progress, message):
           progress_bar.progress(progress)
           status_text.text(message)
       
       try:
           market_prices = scrape_market_prices(pages=8, progress_callback=update_progress)
           st.session_state.market_prices = market_prices
           st.session_state.last_scraped = datetime.now()
           st.session_state.scraping_in_progress = False
           progress_bar.progress(1.0)
           status_text.success("✅ Pobrano ceny rynkowe!")
           st.sidebar.success("Ceny rynkowe zostały zaktualizowane!")
       except Exception as e:
           st.session_state.scraping_in_progress = False
           st.sidebar.error(f"Błąd podczas scrapowania: {str(e)}")
           status_text.error("❌ Błąd podczas scrapowania")
   
   if st.session_state.scraping_in_progress:
       st.sidebar.info("⏳ Scrapowanie w toku...")
   
   if st.session_state.last_scraped:
       st.sidebar.caption(f"Ostatnie scrapowanie: {st.session_state.last_scraped.strftime('%Y-%m-%d %H:%M:%S')}")

   # Komponenty UI
   area = st.number_input("Powierzchnia (m²)", min_value=10.0, max_value=300.0, value=50.0)
   rooms = st.slider("Liczba pokoi", 1, 6, 3)
   photos = st.number_input("Liczba zdjęć", 0, 50, 10)
  
   locality = st.selectbox("Dzielnica", [
       "Łódź Bałuty", "Łódź Górna", "Łódź Śródmieście",
       "Łódź Widzew", "Łódź Polesie"
   ])

   show_chart = st.checkbox("Pokaż wykres porównawczy")

   if st.button("Oblicz cenę"):
      predicted_price = predict_price(area, rooms, photos, locality)
      market_avg_price = st.session_state.market_prices.get(locality, DEFAULT_MARKET_PRICES[locality])
      
      # Wyświetlanie metryk
      col1, col2 = st.columns(2)
      
      with col1:
          st.metric("Szacowana cena", f"{predicted_price:,.0f} zł")
      
      with col2:
          st.metric("Średnia cena rynkowa", f"{market_avg_price:,.0f} zł")
      
      # Wykres słupkowy
      if show_chart:
          st.subheader("Porównanie cen")
          chart_data = pd.DataFrame({
              'Cena': [predicted_price, market_avg_price],
              'Typ': ['Przewidywana cena', 'Średnia cena rynkowa']
          })
          chart_data = chart_data.set_index('Typ')
          st.bar_chart(chart_data)

# === Punkt wejścia ===
# W Streamlit kod musi być wykonany na najwyższym poziomie
main()