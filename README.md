Lazar HI20 - Home Assistant Integration
Integracja dla Home Assistant umożliwiająca komunikację z urządzeniami Lazar HI20. Dodatek ten pozwala na monitorowanie parametrów pracy urządzenia bezpośrednio w Twoim panelu sterowania.

📋 Spis treści
Funkcje

Instalacja

Konfiguracja

Wspierane sensory

Rozwiązywanie problemów

✨ Funkcje
Odczyt danych w czasie rzeczywistym z kontrolera Lazar HI20.

Łatwa integracja z Home Assistant poprzez HACS.

Automatyczne tworzenie encji sensorów.

🚀 Instalacja
Metoda 1: HACS (Zalecana)

Otwórz HACS w swoim Home Assistant.

Kliknij trzy kropki w prawym górnym rogu i wybierz Custom repositories (Niestandardowe repozytoria).

Wklej adres URL swojego repozytorium: https://github.com/Wilczek85/lazar_HI20.

Wybierz kategorię Integration i kliknij Add.

Znajdź "Lazar HI20" na liście i kliknij Download.

Zrestartuj Home Assistant.

Metoda 2: Ręczna

Pobierz zawartość folderu custom_components/lazar_hi20 z tego repozytorium.

Wklej go do folderu config/custom_components/lazar_hi20/ w swojej instancji Home Assistant.

Zrestartuj Home Assistant.

⚙️ Konfiguracja
Obecnie integracja wymaga dodania wpisu w pliku configuration.yaml.

Przykład:

YAML
lazar_hi20:
  host: 192.168.1.100  # Adres IP Twojego urządzenia
  scan_interval: 30    # Czas odświeżania w sekundach
Uwaga: Pamiętaj o sprawdzeniu, czy adres IP urządzenia jest stały (DHCP Reservation).

📊 Wspierane sensory
Integracja dostarcza następujące dane (zależnie od modelu):

Temperatura kotła

Stan pracy palnika

Temperatura CWU

I inne parametry diagnostyczne.

🛠 Rozwiązywanie problemów
Logi (Debugowanie)

Jeśli napotkasz problemy, włącz logowanie debugujące w configuration.yaml:

YAML
logger:
  default: info
  logs:
    custom_components.lazar_hi20: debug
Częste błędy

Connection Timeout: Sprawdź połączenie sieciowe z kontrolerem Lazar.

HACS Version Error: Upewnij się, że zainstalowana wersja posiada poprawny tag (np. v1.0.0).

👨‍💻 Autor
Wilczek85 - Profil GitHub
