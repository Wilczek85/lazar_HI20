# Historia zmian

## 2026.10.3 — 2026-10-25

- Baza: gałąź 2026.10.2, commit c2463a6.
- Ujednolicono numer manifestu z wydaniem 2026.10.3.
- Przeniesiono hacs.json do katalogu głównego i usunięto nieobsługiwane pola.
- Dołączono panel Glass pod custom_components/lazar_hi20/panel_glass, aby był pobierany przez HACS.
- Dodano instrukcję aktualizacji HACS i jednorazowej aktywacji panelu.
- Dodano workflow publikujący tylko stabilne wydanie v2026.10.3 po push na gałąź 2026.10.2; używa tokenu repozytorium, bez zewnętrznych akcji.
- Zachowano działanie integracji oraz istniejące encje. Aktualizacja nie nadpisuje aktywnego panelu.


## 2026.3.2 — 2026-10-25

### Dodano
- Oddzielny wariant dashboardu Lazar Home Glass z tapetą domu i ogrodu o zmierzchu.
- Motyw z półprzezroczystymi kartami i opcjonalnym rozmyciem card-mod.
- Widoki Klimat, Historia i Pompa, sterowanie istniejącymi encjami switch/select/number.
- Przyciski −/+ dla CWU Eco/Komfort i czterech punktów krzywej grzewczej.
- Generator mapujący 22 encje po unique_id, z obsługą własnych nazw i sufiksów.
- Paczka ZIP do ręcznego wgrania panelu i instrukcja scalania konfiguracji.

### Zakres i sprawdzenie
- Numer wersji manifestu: 2026.3.1 → 2026.3.2.
- Zachowano poprzedni dashboard oraz logikę integracji i API.
- Temperatura pokojowa zadana pozostaje tylko do odczytu; nie aktywowano niegotowej platformy climate.
- Walidacja YAML/JSON, generatora encji i integralności ZIP. Testy regresji temperatur uruchomiono lokalnie.
- Brak testu interfejsu w działającym HA i komend na fizycznej pompie.
