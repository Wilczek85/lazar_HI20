# Lazar HI20 — Home Assistant

Wersja **2026.10.3**, oparta na gałęzi `2026.10.2`: aktualizacja przez HACS i panel Lazar Home Glass dołączony do integracji.

- [Instalacja i aktualizacja przez HACS](INSTALACJA_HACS.md)
- [Panel Glass — konfiguracja](custom_components/lazar_hi20/panel_glass/START_TUTAJ.md)
- [Historia zmian](CHANGELOG.md)
- [Ograniczenia integracji](AUDYT_PL.md)

W HACS wybierz wydanie **v2026.10.3** i po pobraniu uruchom ponownie HA. Jeśli używasz repozytorium jako niestandardowego, jego URL to `https://github.com/Wilczek85/lazar_HI20`, kategoria: Integracja.

Panel jest pobierany do `/config/custom_components/lazar_hi20/panel_glass/`. Jego jednorazowa konfiguracja wymaga skopiowania tapety, motywu i YAML według instrukcji. Aktualizacja nie nadpisuje aktywnego dashboardu ani istniejącej konfiguracji HA.

Panel ma zakładki Klimat, Historia i Pompa, CWU Eco/Komfort oraz cztery punkty krzywej grzewczej. Pokojowa nastawa pozostaje tylko do odczytu. Standardowe karty nie wymagają dodatków HACS; card-mod jest opcjonalny.

Integracja komunikuje się z chmurą hkslazar.net przez login i hasło. Konfiguracja hosta LAN przez YAML nie jest obsługiwana. Nie zmieniono logiki API ani nie aktywowano platformy climate.

Testy lokalne obejmują odczyty temperatur, pliki konfiguracji i paczkę panelu. Nie testowano na fizycznej pompie ani w działającej instancji HA.

Dotychczasowa instrukcja: [INSTALACJA_PL.md](INSTALACJA_PL.md).
