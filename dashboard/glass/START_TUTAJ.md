# Lazar Home Glass — instalacja

Panel do istniejącej integracji Wilczek85/lazar_HI20. Przygotowany na podstawie kodu f2355f5 i dokumentacji Home Assistant 2026.10. Zalecana aktualna wersja HA. Paczka zawiera sam dashboard, motyw, tapetę i narzędzie dopasowania encji. Nie instaluje ani nie aktualizuje integracji pompy i nie zawiera danych logowania.

## 1. Skopiuj pliki

Rozpakuj ZIP na komputerze. Przez dodatek Studio Code Server, File editor lub udział Samba skopiuj ZAWARTOŚĆ folderu `config` do katalogu konfiguracji HA (`/config`). Wynik:

- `/config/www/lazar_home/tapeta.jpg`
- `/config/themes/lazar_glass.yaml`
- `/config/dashboards/lazar_home.yaml`

Nie twórz `/config/config`. Jeśli pliki o tych nazwach już istnieją, najpierw zachowaj ich kopię. Nie nadpisuj folderu custom_components.

## 2. Włącz motyw i panel

Zrób kopię `configuration.yaml`. Plik `configuration_fragment.yaml` zawiera fragment DO SCALENIA z bieżącą konfiguracją. Nie zastępuj nim całego pliku!

Jeżeli nie masz sekcji frontend ani lovelace, dopisz fragment w całości. Jeśli masz je już, dodaj brakujące pola do istniejących sekcji. Każdy klucz główny może wystąpić tylko raz. Jeśli masz własny sposób ładowania motywów, dopasuj go zamiast dodawać drugi wpis themes. Jeśli dashboards już istnieje, dopisz pod nim tylko lazar-home. Zachowaj inne ustawienia i dashboardy.

Sprawdź konfigurację w Narzędzia deweloperskie → YAML i uruchom HA ponownie. W menu bocznym pojawi się **Lazar Home**. Panel zawiera zakładki **Klimat**, **Historia**, **Pompa**. Motyw jest przypisany do widoków; nie trzeba zmieniać motywu całego konta. Adres panelu: `/lazar-home/klimat`.

Alternatywa: zamiast wpisu lovelace utwórz nowy pusty dashboard z UI i wklej całość `config/dashboards/lazar_home.yaml` w jego edytorze surowej konfiguracji. Tapetę i motyw nadal trzeba skopiować oraz włączyć frontend.themes. Wybierz jedną metodę — nie instaluj tego samego panelu dwukrotnie.

## 3. Dopasuj encje

Domyślne nazwy odpowiadają encjom z repozytorium. Home Assistant może nadać inne nazwy, np. z końcówką `_2`. Jeśli pojawi się „Encja nie istnieje”, sprawdź aktualne identyfikatory w Ustawienia → Urządzenia i usługi → Encje, filtrując po Lazar. W pliku dashboardu zamień wszystkie wystąpienia identyfikatora. Samo zmienienie nazwy wyświetlanej kafelka nie wystarczy.

Możesz też użyć załączonego generatora na komputerze z Pythonem 3:

1. Wykonaj lokalną kopię `/config/.storage/core.entity_registry`; nie zmieniaj oryginału. Nie publikuj tej kopii.
2. W folderze `narzedzia` uruchom:

```sh
python3 build_dashboard.py /sciezka/do/kopii/core.entity_registry --output lazar_home_gotowy.yaml
```

3. Wynik skopiuj jako `/config/dashboards/lazar_home.yaml` lub wklej do edytora surowego panelu utworzonego w UI. Wynik to JSON akceptowany jako YAML przez Home Assistant.

Generator dopasowuje encje po unique_id, domenie i integracji. Przy kilku wpisach integracji dodaj `--entry-id ID_WPISU`. Brakujące, wyłączone lub niejednoznaczne encje zatrzymują generowanie. Narzędzie nie potrzebuje hasła ani internetu. Nie zapisuje nic do rejestru HA.

## 4. Efekt szkła — opcjonalnie

Tapeta, zaokrąglenia i półprzezroczystość działają z dołączonym motywem bez dodatkowych kart HACS. Dla dodatkowego rozmycia tła ZA kafelkami zainstaluj `card-mod` przez HACS (projekt thomasloven/lovelace-card-mod), według instrukcji projektu, i odśwież aplikację. Wpisy card_mod są już w dashboardzie. Bez card-mod pozostają standardowe, funkcjonalne karty.

To implementacja inspirowana makietą, nie jej identyczna kopia. Wykorzystuje standardowe kafelki oraz nawigację HA. Nie dodaje własnego bocznego menu ani pionowego regulatora termostatu. Na telefonie sekcje układają się jedna pod drugą; na większym ekranie w maksymalnie trzech kolumnach.

## Co obsługuje panel

- Rzeczywisty pomiar pokoju, temperatury CWU, zewnętrzna i powrotu CO.
- Odczyt nastawy pokojowej — bez przycisków zmiany.
- Włączenie/wyłączenie całej pompy przez istniejący switch.
- Wybór trybu przez istniejącą encję select (lista rozwijana).
- CWU Eco i Komfort oraz cztery punkty krzywej grzewczej: natywne przyciski −/+.
- Stan alarmu, historia 24 h i dodatkowe odczyty diagnostyczne.

Panel pokazuje wartości encji, nie dane demonstracyjne. Historia wymaga ich zapisywania przez recorder. Bez danych historycznych wykresy będą puste. Brak czujnika pokojowego skonfigurowanego w integracji oznacza niedostępny pomiar pokoju; wybranie go służy do odczytu, nie wysyła temperatury do pompy.

## Pierwsze sprawdzenie

1. Otwórz `/local/lazar_home/tapeta.jpg` pod adresem swojego HA; powinna pojawić się tapeta. Jeśli folder www został utworzony pierwszy raz, może być potrzebny restart HA.
2. Porównaj temperatury z aplikacją Lazar i czujnikiem pokojowym.
3. Sprawdź wszystkie encje. Stan alarmu jest przekazywany z integracji: jej aktualny kod ma ograniczenia przy brakujących lub uszkodzonych danych alarmowych. Panel ich nie naprawia.
4. Pojedynczą zmianę nastawy zweryfikuj w aplikacji producenta. Kod integracji nie potwierdza treści odpowiedzi na zapis; sam sukces HTTP nie gwarantuje wykonania polecenia. Nie klikaj szybko wielokrotnie przy odświeżaniu chmurowym.
5. Nie interpretuj wybranego trybu jako bieżącej pracy sprężarki. Nazwy trybów i ich mapowanie pochodzą z integracji i wymagają potwierdzenia na urządzeniu. Przyciski krzywej respektują limity encji, ale integracja nie sprawdza zależności pomiędzy czterema punktami.

Nie dodano energii, COP ani temperatury zasilania CO, ponieważ nie ma wystarczająco potwierdzonych danych. Karta powrotu CO nie zastępuje pomiaru zasilania.

## Rozwiązywanie problemów i usunięcie

- Brak tła: sprawdź ścieżkę www, adres /local, restart i odświeżenie pamięci aplikacji.
- Jasne, nieprzezroczyste karty: sprawdź załadowanie motywu Lazar Glass; po zmianie wykonaj frontend.reload_themes, potem odśwież panel.
- Brak funkcji numeric-input lub select-options: zaktualizuj HA. Awaryjnie usuń listę features danego kafelka i steruj przez okno szczegółów po dotknięciu.
- Błąd encji: wykonaj punkt 3 powyżej.
- Usunięcie: usuń wpis lazar-home z lovelace.dashboards (lub dashboard UI), następnie trzy skopiowane pliki. Pozostaw ustawienia frontend/themes, jeśli używają ich inne motywy. Nie usuwaj integracji pompy.

## Walidacja i źródła

Sprawdzono odczyt YAML/JSON, mapowanie 22 encji według unique_id z repozytorium, generator z syntetycznym rejestrem i niestandardowymi nazwami oraz zawartość ZIP. Nie uruchomiono panelu w prawdziwej instancji HA i nie testowano poleceń na fizycznej pompie. Wygląd może różnić się zależnie od wersji HA i szerokości ekranu.

https://github.com/Wilczek85/lazar_HI20
https://www.home-assistant.io/dashboards/views/
https://www.home-assistant.io/dashboards/features/
https://github.com/thomasloven/lovelace-card-mod

Tapeta wygenerowana dla tego panelu: dom i ogród o zmierzchu, ciepłe oświetlenie, granatowe niebo, rozmycie fotograficzne. Brak interfejsu na obrazie tła.
