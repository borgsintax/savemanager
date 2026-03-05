# Save Manager App

🇬🇧 [English](#english) | 🇮🇹 [Italiano](#italiano)

---

<a id="english"></a>
## 🇬🇧 English

A lightweight and modern desktop application written in Python to manage and secure your favorite games' save files.

### 🌟 Features
- **Modern UI**: Attractive and intuitive user interface based on `CustomTkinter` (dark theme).
- **Persistent Configuration**: Automatically remembers the last entered game, source folder, and backup folder.
- **Secure Backups**: Creates complete copies of the saves folder, automatically appending the date and time (timestamp) to the folder name.
- **Fast Restore**: Replaces the current game files using a backup selected from the list with a single click.
- **Cleanup**: Allows you to safely delete older or no longer needed backups.
- **Universal Compatibility**: Tested with games like **Star Trek Voyager** and **FTL**, but it can be used with **any game** that has a save folder!

### 🛠 Requirements
- **Python 3.10** or higher (if running from source).
- To work, it requires the installation of the libraries listed in `requirements.txt`.

### 🚀 Installation and Execution (Source)
1. Download or clone this repository:
   ```bash
   git clone <insert_repo_url>
   cd SaveManagerApp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

### 📦 Building the Executable for Windows
If you want to compile the project as a portable `.exe` executable (so you can use it or share it with friends without them needing to install Python):
1. Make sure you have PyInstaller installed:
   ```bash
   pip install pyinstaller
   ```
2. Run the build command from the main folder:
   ```bash
   pyinstaller --noconsole --onefile --collect-all customtkinter --name "SaveManager" app.py
   ```
3. You will find the standalone executable inside the `dist/` folder.

### 📝 Notes
The application creates and uses a local file (`config.json`) in its root to remember the configured paths. Do not upload this file online, it is already ignored via `.gitignore` along with `build/`, `dist/`, and other local folders.

---

<a id="italiano"></a>
## 🇮🇹 Italiano

Un'applicazione desktop leggera e moderna scritta in Python per gestire e mettere al sicuro i salvataggi dei tuoi giochi preferiti.

### 🌟 Caratteristiche
- **Grafica Moderna**: Interfaccia utente accattivante e intuitiva, basata su `CustomTkinter` (tema scuro).
- **Configurazione Persistente**: Ricorda in automatico l'ultimo gioco inserito, la cartella di origine e quella di backup.
- **Backup Sicuri**: Crea copie complete della cartella dei salvataggi, aggiungendo la data e l'ora (timestamp) al nome della cartella in automatico.
- **Ripristino Veloce**: Sostituisce i file attuali del gioco usando un backup da te selezionato dalla lista con un solo clic.
- **Pulizia**: Ti permette di eliminare i backup più vecchi o non più utili in tutta sicurezza.
- **Compatibilità Universale**: Testato con giochi come **Star Trek Voyager** e **FTL**, ma può essere utilizzato con **qualsiasi gioco** in cui c'è una cartella di salvataggio!

### 🛠 Requisiti
- **Python 3.10** o superiore (se eseguito dai sorgenti).
- Per funzionare, richiede l'installazione delle librerie presenti in `requirements.txt`.

### 🚀 Installazione ed Esecuzione (Sorgenti)
1. Scarica o clona questo repository:
   ```bash
   git clone <inserisci_url_repo>
   cd SaveManagerApp
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Lancia l'applicazione:
   ```bash
   python app.py
   ```

### 📦 Compilazione dell'Eseguibile per Windows
Se desideri compilare il progetto come eseguibile `.exe` portatile (così potrai usarlo o passarlo agli amici senza che debbano installare Python):
1. Assicurati di aver installato PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Esegui il comando di build dalla cartella principale:
   ```bash
   pyinstaller --noconsole --onefile --collect-all customtkinter --name "SaveManager" app.py
   ```
3. Troverai l'eseguibile indipendente all'interno della cartella `dist/`.

### 📝 Note
L'applicazione crea e utilizza un file locale (`config.json`) nella sua stessa root per ricordarsi i percorsi configurati. Non caricare questo file online, è già ignorato tramite `.gitignore` insieme a `build/`, `dist/` e altre cartelle locali.
