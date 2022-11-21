# Stacja pogodowa
Projekt wykorzystuje:
- [Raspberry Pi Pico](https://botland.com.pl/moduly-i-zestawy-do-raspberry-pi-pico/18767-raspberry-pi-pico-rp2040-arm-cortex-m0-0617588405587.html)
- [Wyświetlacz LCD 4x20](https://botland.com.pl/wyswietlacze-alfanumeryczne-i-graficzne/19735-wyswietlacz-lcd-4x20-znakow-zielony-justpi-5903351243094.html)
- [Konwerter I2C](https://botland.com.pl/konwertery-pozostale/2352-konwerter-i2c-dla-wyswietlacza-lcd-hd44780-5903351248693.html)
- [Czujnik temperatury i wilgotności DHT22](https://botland.com.pl/czujniki-multifunkcyjne/2637-czujnik-temperatury-i-wilgotnosci-dht22-am2302-modul-przewody-5904422372712.html)
- Moduł internetowy [ESP-01](https://botland.com.pl/produkty-wycofane/4527-modul-wifi-esp-01-esp8266-black-3-gpio-1mb-pcb-antena-5904422332877.html)
- Dowolny [odbiornik podczerwieni](https://botland.com.pl/odbiorniki-podczerwieni/4931-odbiornik-podczerwieni-tsop31236-36-khz-5904422302757.html)





# Funkcjonalności i plany
- [X] Podpięcie [wyświetlacza](https://botland.com.pl/wyswietlacze-alfanumeryczne-i-graficzne/19735-wyswietlacz-lcd-4x20-znakow-zielony-justpi-5903351243094.html) z [konwerterem I2C](https://botland.com.pl/konwertery-pozostale/2352-konwerter-i2c-dla-wyswietlacza-lcd-hd44780-5903351248693.html) i pokazywanie na nim informacji dla użytkownika
- [X] Łączenie się z WiFi za pomocą [modułu ESP-01](https://botland.com.pl/produkty-wycofane/4527-modul-wifi-esp-01-esp8266-black-3-gpio-1mb-pcb-antena-5904422332877.html) i [komend AT](https://docs.espressif.com/projects/esp-at/en/latest/esp32/AT_Command_Set/Basic_AT_Commands.html)
- [X] Czytanie informacji o temperaturze i wilgotności przez czujnik [DHT22](https://botland.com.pl/czujniki-multifunkcyjne/2637-czujnik-temperatury-i-wilgotnosci-dht22-am2302-modul-przewody-5904422372712.html)
- [X] Obsługa odbiornika podczerwieni dla komunikacji użytkownika z programem z pomocą [repozytorium micropython_ir](https://github.com/peterhinch/micropython_ir)
  - [X] zmiana godziny
  - [X] zciemnianie wyświetlacza
- [X] Pobieranie aktualnej godziny
- [X] Wyświetlanie polskich znaków
- [X] Tworzenie serwera wyświetlającego informację z czujników w formacie czytelnym i JSON
- [ ] Dodanie czujników i sensorów
  - [ ] Czujnik pyłów




# Diagram połączenia
![diagram połączenia](img/stacja_pogodowa.png)