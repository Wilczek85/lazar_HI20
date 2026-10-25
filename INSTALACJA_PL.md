> Nowy wariant 2026.3.2 z tapetą: [Lazar Home Glass — instrukcja](dashboard/glass/START_TUTAJ.md). Poniższa instrukcja opisuje dotychczasowy panel.

# Lazar HI20 — poprawka temperatury i dashboard Lazar Home

Pakiet opracowany na podstawie commita `2e738d9004e98ff1983ce40f4da9a569558eecb1`.
To lokalna poprawka do sprawdzenia na urządzeniu, nie oficjalne wydanie autora.

## Instalacja poprawki

1. Wykonaj kopię zapasową bieżącego katalogu `/config/custom_components/lazar_hi20` oraz konfiguracji Home Assistant.
2. Skopiuj cały katalog `custom_components/lazar_hi20` z paczki do `/config/custom_components/`, zastępując pliki integracji. Nie usuwaj integracji z interfejsu HA — zachowa to istniejące encje i historię.
3. Uruchom ponownie Home Assistant.
4. W Ustawienia → Urządzenia i usługi → Heatpump Lazar HI20 → Konfiguruj wybierz rzeczywisty pokojowy czujnik temperatury, np. Zigbee. Nie wybieraj sensora utworzonego przez samą integrację Lazar. Czujnik musi mieć jednostkę °C, °F lub K.
5. Porównaj „Temperatura pokojowa (odczyt)” z wybranym czujnikiem. Nowa encja „Temperatura pokojowa zadana” powinna pokazywać nastawę sterownika, niezależnie od pomiaru.

Bez skonfigurowanego, dostępnego czujnika pokojowego pomiar będzie niedostępny. Nie podstawiamy temperatury powrotu CO ani zadanej jako pomiaru pokoju. Usunięcie wyboru w opcjach teraz rzeczywiście odłącza czujnik. Odczyt jest lokalny; nie jest wysyłany do sterownika pompy. Zachowano dotychczasowe unique_id.

## Motyw w stylu Apple Home

Panel jest inspirowany Apple Home: duże zaokrąglone karty, jasne tło, pomarańczowy akcent, wariant nocny. To dashboard Home Assistant, nie integracja HomeKit ani identyczna kopia aplikacji Apple. Nie wymaga Mushroom, card-mod ani innych kart HACS.

1. Skopiuj `dashboard/lazar_home_theme.yaml` do `/config/themes/lazar_home.yaml`.
2. W `configuration.yaml` dodaj lub uzupełnij istniejącą sekcję (nie twórz drugiego klucza `frontend`):

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

3. Sprawdź konfigurację i uruchom ponownie HA. Przy późniejszych zmianach motywu wystarczy akcja `frontend.reload_themes`.
4. W Ustawienia → Panele utwórz nowy pusty panel. Otwórz edycję panelu i edytor surowej konfiguracji. Wklej zawartość `dashboard/lazar_home.yaml` (całość, razem z `views`).
5. W profilu wybierz motyw „Lazar Home” oraz jasny/ciemny tryb. Widoki również wskazują ten motyw.

Widok „Dom”: pomiar pokojowy, CWU, temperatura zewnętrzna, alarm, zasilanie, wybór trybu i nastawy CWU, wykres temperatur i mocy. Widok „Pompa”: hydraulika, EEV, przepływy, krzywa grzewcza. Dotknięcie kafelka otwiera szczegóły, z których można sterować obsługiwanymi encjami. Wykres mocy pokazuje W; nie udaje zużycia energii w kWh.

## Dopasowanie encji — ważne w istniejącej instalacji

Dołączony YAML ma domyślne identyfikatory bez `_2`. Repozytorium zawierało lokalne nazwy z `_2`, więc w Twojej instalacji może być potrzebne dopasowanie. Możesz zmienić encje ręcznie w edytorze kart albo wygenerować panel automatycznie:

1. Po restarcie integracji zrób lokalną kopię pliku `/config/.storage/core.entity_registry`. Nie edytuj oryginału i nie przesyłaj go publicznie.
2. Na komputerze z Pythonem 3 uruchom w katalogu paczki:

```sh
python3 dashboard/build_dashboard.py /sciezka/do/kopii/core.entity_registry --output lazar_home_gotowy.yaml
```

3. Wklej wynik `lazar_home_gotowy.yaml` do surowego edytora panelu. Plik ma zapis JSON, który jest również poprawnym YAML. Generator dopasowuje po domenie, platformie i unique_id, więc uwzględnia końcówki `_2` oraz własne nazwy encji. Nie potrzebuje hasła, tokenu, internetu ani bibliotek Pythona.
4. Jeśli zgłosi brak encji, sprawdź aktualizację integracji i włączenie encji. Przy wielu wpisach podaj `--entry-id ID_WPISU`. Generator nie nadpisuje rejestru HA i nie zapisuje wyniku przy brakach lub niejednoznaczności.

## Sprawdzenie po aktualizacji

- Pomiar 21,5°C powinien pozostać 21,5°C, nie 215°C.
- Zmiana pomiaru pokojowego nie może zmieniać nastawy wyświetlanej z API.
- Odłączenie czujnika ma dać stan niedostępny, nie zero.
- Sprawdź zgodność CWU, temperatury zewnętrznej i powrotu ze sterownikiem pompy.
- Sprawdź stan i pojedynczą zmianę nastawy CWU w panelu i w aplikacji Lazar. Brak dostępu do urządzenia uniemożliwił test rzeczywistych zapisów.

W razie problemu przywróć poprzedni katalog integracji i uruchom HA ponownie. Aktualizacja z HACS może nadpisać tę lokalną poprawkę.

## Walidacja i ograniczenia

Przeszły testy konwersji, wartości błędnych i braku nadpisywania nastaw; sprawdzono składnię Pythona, YAML oraz mapowanie encji. Nie uruchomiono pełnego Home Assistant ani panelu w przeglądarce HA, nie wykonano testów na fizycznej pompie ani zalogowanym API. Szczegóły audytu: `AUDYT_PL.md`.

Podstawa dokumentacyjna: https://www.home-assistant.io/dashboards/tile/ oraz https://www.home-assistant.io/integrations/frontend/. Niektóre zmienne wizualne motywu (np. promień narożników) są zależne od wersji frontendowej HA.
