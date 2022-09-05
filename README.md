# Stacja pogodowa
Stacja pogodowa wykorzystująca Raspberry Pi Pico W. Czyta dane o temperaturze i wilgotności i pokazuje je na wyświetlaczu. Domyślnie ma te dane przesyłać na serwer do bazy danych.

Dodatkowo w głównym folderze powinien znajdować się folder ```netinfo.txt```, który zawiera SSID i hasło do naszego WiFi w następującym formacie:
>SSID:::HASŁO   

(trzy dwukropki wymagane, ponieważ mogą występować w haśle)


### Funkcjonalności
- [X] Podpięcie [wyświetlacza](https://botland.com.pl/wyswietlacze-alfanumeryczne-i-graficzne/19735-wyswietlacz-lcd-4x20-znakow-zielony-justpi-5903351243094.html) z [konwerterem I2C](https://botland.com.pl/konwertery-pozostale/2352-konwerter-i2c-dla-wyswietlacza-lcd-hd44780-5903351248693.html) i pokazywanie na nim informacji dla użytkownika
- [X] Łączenie się z WiFi
- [X] Czytanie informacji o temperaturze i wilgotności przez czujnik [DHT22](https://botland.com.pl/czujniki-multifunkcyjne/2637-czujnik-temperatury-i-wilgotnosci-dht22-am2302-modul-przewody-5904422372712.html)
- [X] Obsługa odbiornika podczerwieni dla komunikacji użytkownika z programem (zmiana godziny, zciemnianie wyświetlacza) z pomocą [repozytorium micropython_ir](https://github.com/peterhinch/micropython_ir)
- [X] Pobieranie aktualnej godziny
- [X] Wyświetlanie polskich znaków
- [ ] Łączenie się z lokalnym serwerem
- [ ] Wysyłanie informacji z czujników na serwer
