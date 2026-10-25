# Lazar HI20 — Home Assistant

Wersja **2026.3.2**: panel **Lazar Home Glass** z tapetą, półprzezroczystym motywem i natywnymi kontrolkami Home Assistant.

## Panel Glass

- [Pobierz paczkę panelu 2026.3.2](releases/Lazar_Home_Glass_2026.3.2.zip?raw=true)
- [Instrukcja instalacji panelu](dashboard/glass/START_TUTAJ.md)
- [Pliki panelu, motywu i tapety](dashboard/glass/config)
- [Historia zmian](CHANGELOG.md)

Panel zawiera zakładki Klimat, Historia i Pompa, nastawy CWU Eco/Komfort oraz cztery punkty krzywej grzewczej. Korzysta z istniejących encji integracji. Nastawa pokojowa pozostaje tylko do odczytu. Nie uruchamia platformy climate ani nie zmienia protokołu sterowania pompą. Podstawowe działanie nie wymaga kart HACS; card-mod jest opcjonalnym dodatkiem do efektu szkła.

**Aktualizacja integracji sama nie instaluje panelu.** Skopiuj osobno pliki z paczki zgodnie z instrukcją. Paczka ZIP zawiera dashboard, a nie komponent custom_components.

## Integracja i dotychczasowy panel

- [Instalacja integracji i dashboard Lazar Home](INSTALACJA_PL.md)
- [Audyt, zakres poprawek i ograniczenia](AUDYT_PL.md)

Integrację konfiguruje się przez Ustawienia → Urządzenia i usługi, za pomocą loginu i hasła serwisu Lazar. Komunikacja odbywa się z chmurą hkslazar.net. Ta wersja nie obsługuje konfiguracji hosta LAN przez YAML.

Sprawdzono konfigurację plików i mapowanie encji. Panel Glass nie był testowany w działającej instancji Home Assistant ani na fizycznej pompie. Interpretacja trybów, potwierdzenie zapisu oraz obsługa brakujących danych alarmowych zachowują ograniczenia opisane w audycie.
