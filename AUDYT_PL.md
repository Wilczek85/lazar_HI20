# Audyt kodu Lazar HI20

Przegląd źródeł wszystkich modułów integracji i dashboardu. Baza: commit `2e738d9004e98ff1983ce40f4da9a569558eecb1`. Bez dostępu do konta Lazar, dokumentacji protokołu urządzenia i instalacji HA użytkownika.

## Znalezione i poprawione

| Waga | Miejsce | Problem i poprawka |
| --- | --- | --- |
| Wysoka | coordinator.py | Pomiar pokojowy był wpisywany w `troomsetheat` i `troomsetcool`, zacierając rzeczywiste nastawy. Usunięto mutację danych API. |
| Wysoka | const.py / sensor.py | „Temperatura pokojowa (odczyt)” była nastawą, a przy lokalnym czujniku miała dziesięciokrotnie zawyżony wynik. Zachowano unique_id i nazwę starej encji, ale podłączono prawdziwy pomiar; dodano oddzielny sensor nastawy ze skalą 0,1. |
| Średnia | sensor.py / values.py | Mnożenie tekstu z API powodowało błędy. Normalizacja liczb, odrzucanie -9999 również jako tekstu, bool, NaN, nieskończoności i danych uszkodzonych. Brak pomiaru nie jest zerem. |
| Średnia | sensor.py | Pokojowy pomiar odświeża się przy zmianie encji źródłowej, także gdy API chmury jest niedostępne. Dostępność pomiaru lokalnego nie zależy od chmury. |
| Średnia | config_flow.py | Usunięcie czujnika z opcji wcześniej przywracało wartość z entry.data. Teraz zapisuje jawne None. |
| Średnia | config_flow.py / __init__.py | Sesja aiohttp mogła pozostać otwarta po nieudanym logowaniu lub pierwszym odświeżeniu. Dodano zamykanie w ścieżkach błędu. |
| Średnia | switch.py | Optymistyczny stan mógł pozostać w interfejsie po zakończeniu operacji. Po wyczyszczeniu stanu publikowany jest wynik koordynatora. |
| Średnia | dashboard.yaml | Obce encje korekty temperatury pokazano jako przepływy; EEV grzania/chłodzenia zamieniono; Carter wskazywał pokój. Poprawiono powiązania. Usunięto zależność od przypadkowych końcówek `_2`, dodano generator mapowania. |
| Niska | dashboard.yaml | Wykresy mocy opisano jako energię. Nazwy i jednostki rozdzielono. |
| Niska | number.py / climate.py | Ujednolicono parsowanie liczbowych odczytów. W nieaktywnej platformie climate poprawiono również źródło current_temperature. |

## Istotne kwestie pozostające do weryfikacji

1. **Platforma climate nie jest ładowana** — brak jej w PLATFORMS. Celowo jej nie uruchomiono w tej poprawce: jej logika interpretuje każde włączenie jako HEAT, chociaż integracja ma także chłodzenie i CWU. `async_set_hvac_mode(HEAT)` tylko włącza urządzenie. Pełny termostat wymaga potwierdzenia mapowania trybów, zakresów i komend API. Dashboard używa istniejących switch/select/number.
2. **Protokół zapisu niepotwierdzony** — set_param uznaje HTTP 200 za sukces, nie sprawdzając treści odpowiedzi. Szerokie przechwytywanie Exception ponawia zapis po dowolnym błędzie. Bez próbek odpowiedzi sukcesu i błędu nie dodano zgadywanego parsera. Odczyt po zapisie i stan sterownika wymagają testu na urządzeniu.
3. **Tryby 0/1/2, jednostki mocy i skala temperatur** — zachowano interpretację autora. Przykłady API i dokumentacja producenta nie występują w repozytorium. Szczególnie `comprpow` i `powerneed` jako W wymagają potwierdzenia. Skala 0,1 dla nastawy wynika z istniejącego climate.py, a nie z niezależnie zweryfikowanego protokołu.
4. **Wiele urządzeń/kont** — globalne unique_id oraz identyfikator urządzenia `main_unit` mogą kolidować. Nie zmieniono ich bez migracji rejestru, aby nie uszkodzić obecnych powiązań. Pakiet jest przeznaczony do istniejącej instalacji jednej pompy.
5. **Błędy logowania** — po ponowieniu są opakowane jako UpdateFailed; brak pełnego przepływu reauth. Do osobnej poprawki.
6. **Alarmy** — brak alarmcnt jest interpretowany jako zero; odpowiedź tekstowa może dać TypeError. Obsługa statusów switch/select/binary_sensor wymaga dalszego ujednolicenia i testów odpowiedzi API.
7. **Dokumentacja repozytorium była niezgodna z kodem** — opis hosta LAN i wpisu YAML nie odpowiada cloud polling z loginem/hasłem. Nowa instrukcja opisuje rzeczywisty flow. `api.py` jest alternatywnym nieużywanym klientem; hacs.json umieszczono w katalogu komponentu zamiast głównym. W tej paczce zalecana instalacja ręczna.
8. **Historia pokoju** — poprzednia encja mogła już zapisać błędne wartości ×10 do historii. Poprawka nie modyfikuje historycznej bazy danych ani wcześniejszych wykresów.

## Testy

`python3 -m unittest discover -s tests -v` — sześć testów regresji. Część metod koordynatora wyodrębniono przez AST i uruchomiono z atrapami odpowiedzi, więc nie są to testy integracyjne Home Assistant. Sprawdzono również kompilację plików, parsowanie YAML/JSON i generator dashboardu na syntetycznym rejestrze z sufiksami `_2`, w tym odrzucenie brakujących encji. Nie sprawdzono rzeczywistego renderowania kart ani działania usług na urządzeniu.
