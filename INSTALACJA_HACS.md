# Aktualizacja 2026.10.3 przez HACS

Wydanie oparte na gałęzi `2026.10.2`. Numer manifestu i tag wydania są zgodne: `2026.10.3` / `v2026.10.3`.

## Aktualizacja integracji

1. W HACS otwórz Lazar HI20 Heat Pump. Jeśli repozytorium nie jest dodane, w menu repozytoriów niestandardowych dodaj `https://github.com/Wilczek85/lazar_HI20` z kategorią Integracja.
2. Odśwież informacje o repozytorium i wybierz aktualizację/pobranie wersji `v2026.10.3`. Zależnie od wersji HACS opcja może nazywać się Pobierz ponownie (Redownload).
3. Po pobraniu uruchom Home Assistant ponownie. Nie usuwaj skonfigurowanej integracji: zachowasz encje, ustawienia i historię.
4. Jeśli widoczna jest tylko starsza wersja, sprawdź, czy GitHub opublikował stabilne wydanie v2026.10.3 (nie tylko gałąź lub tag), a następnie ponownie odśwież HACS.

## Panel pobrany razem z integracją

HACS pobiera cały katalog `custom_components/lazar_hi20`. Pliki panelu są teraz dostarczane w `/config/custom_components/lazar_hi20/panel_glass/`.

Skopiuj zawartość jego folderu `config` do `/config` i scal `configuration_fragment.yaml` z istniejącym `configuration.yaml`, zgodnie z `panel_glass/START_TUTAJ.md`. Nie zastępuj całej konfiguracji. Jeśli panel już działa, zrób kopię dopasowanego YAML przed jego aktualizacją; nowe pliki z integracji nie nadpisują aktywnego panelu automatycznie.

To jednorazowa konfiguracja dashboardu, motywu i ścieżki tapety. Samo pobranie przez HACS nie dodaje dashboardu do menu i nie aktywuje motywu. Użytkownik zachowuje kontrolę nad istniejącą konfiguracją HA.

## Zakres

Poprawiona struktura HACS, podniesiona wersja, dołączony panel Glass oraz publikacja stabilnego wydania. Bez zmian logiki sterowania pompą. Pomiar pokojowy wymaga wskazania czujnika w opcjach integracji. Dotychczasowe ograniczenia API pozostają opisane w AUDYT_PL.md.

Integracja zachowuje dotychczasowe minimum HA 2026.1.0. Panel przygotowano według dokumentacji HA 2026.10; dla wszystkich jego funkcji zalecana jest ta lub nowsza wersja.
