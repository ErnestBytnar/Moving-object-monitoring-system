# System monitoringu poruszających się obiektów - Raspberry Pi, Python i Flask

## 📖 Opis Projektu

Projekt to system monitoringu oparty na Raspberry Pi, który integruje detekcję ruchu, nagrywanie wideo oraz kontrolę serwomechanizmów. System umożliwia streamowanie wideo w czasie rzeczywistym, a pliki wideo mogą być pobierane po zakończeniu nagrywania. Interfejs użytkownika jest zbudowany w Flask, a piny GPIO Raspberry Pi kontrolują czujniki ruchu oraz serwomechanizm.

**Główne funkcje:**
- Detekcja ruchu za pomocą czujników PIR z kontrolą serwomechanizmu.
- Streamowanie wideo na żywo z kamery Raspberry Pi.
- Automatyczne nagrywanie wideo po wykryciu ruchu.
- Zarządzanie nagraniami wideo z możliwością pobierania.
- Aktualizacje statusu w czasie rzeczywistym oraz zegar odliczający czas nagrywania.


## 🛠️ Konfiguracja GPIO

Piny GPIO w projekcie są przypisane w następujący sposób:  
- **servo_pin = 25** — sterowanie serwomechanizmem,  
- **left_sensor = 22** — czujnik PIR po lewej stronie,  
- **center_sensor = 27** — czujnik PIR na środku,  
- **right_sensor = 17** — czujnik PIR po prawej stronie.  

Czujniki należy ustawić samodzielnie w jednej płaszczyźnie, aby pozostawały nieruchome podczas działania systemu.

## ⚙️ Wymagania

### Sprzęt:
- **Raspberry Pi** (dowolny model z obsługą GPIO i kamery).
- **Kamera** kompatybilna z Raspberry Pi (np. moduł kamery Raspberry Pi).
- **Serwomechanizm** do kontroli pozycji kamery.
- **Czujniki PIR (3)** do detekcji ruchu.

### Oprogramowanie:
- **System operacyjny**: Raspbian lub inna kompatybilna dystrybucja Linux.
- **Python 3.x**.
- Wymagane biblioteki Python:
  - `Flask`
  - `opencv-python`
  - `pigpio` do obsługi pinów GPIO.

## 📦 Instalacja

### 1. Zainstaluj zależności

Zainstaluj wymagane pakiety systemowe i biblioteki Pythona:
```bash
sudo apt-get update
sudo apt-get install pigpio python-pigpio
pip install flask opencv-python pigpio
```
### 2. Uruchom pigpiod


Aby korzystać z GPIO, musisz uruchomić demona pigpiod:

```bash
sudo pigpiod
```
### 3. Klonowanie repozytorium
Skopiuj repozytorium na swoje Raspberry Pi:
```bash
git clone <URL_REPO>
cd <NAZWA_REPO>
```

### 4. Uruchomienie projektu

Po zainstalowaniu wszystkich zależności, uruchom aplikację Flask:

```bash
python app.py
```
### 5. Uruchomienie interfejsu użytkownika
Po uruchomieniu aplikacji Flask otwórz przeglądarkę i wejdź na adres:

```bash
http://<IP_RASPBERRY_PI>:5000
```
Adres IP Raspberry pi sprawdź za pomocą komendy: 
```bash
ping raspberrypi -4
```



### 🖥️ Interfejs Użytkownika
Po uruchomieniu aplikacji, dostępne będą następujące funkcje:

- **Start Monitoring:** Rozpoczyna nagrywanie wideo i detekcję ruchu.
- **Stop Monitoring:** Zatrzymuje nagrywanie.
- **Live View:** Otwiera nowe okno z transmisją na żywo z kamery.
- **Recordings:** Lista dostępnych nagrań wideo, które można pobrać.

### ⚙️ Struktura Projektu
Projekt składa się z kilku plików:

```bash
/app.py              # Główny plik uruchamiający aplikację Flask
/templates/index.html  # Szablon HTML dla interfejsu użytkownika
/recordings          # Folder, w którym przechowywane są nagrania wideo
```
