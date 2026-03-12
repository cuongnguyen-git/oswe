# Steps to Prepare Decompiled `.jar` Application for OSWE Exam

### 1. Open the `.jar` with Java Decompiler and Save Sources as ZIP
- Install JD-GUI:
  ```bash
  sudo apt update
  sudo apt install jd-gui
  ```
- Launch JD-GUI:
  ```bash
  jd-gui
  ```
- Open `application.jar`: Click **File > Open File**, select `~/oswe-exam/application.jar`.
- Save sources: Click **File > Save All Sources**, save as `application-sources.zip` in `~/oswe-exam`.

### 2. Decompress the ZIP and Open in VSCode
- Unzip the file:
  ```bash
  cd ~/oswe-exam
  unzip application-sources.zip -d application-sources
  ```
- Open in VSCode:
  ```bash
  code ~/oswe-exam/application-sources
  ```

### 3. Import the Dependencies
- Create library directory:
  ```bash
  mkdir -p ~/oswe-exam/application-sources/application/lib
  ```
- Extract dependencies:
  ```bash
  unzip -j ~/oswe-exam/application.jar "lib/*" -d ~/oswe-exam/application-sources/application/lib/
  ```
- Add to VSCode classpath:
  - Open **Java Projects** view (`Ctrl+Shift+P`, “Java: Configure Classpath”).
  - Add `~/oswe-exam/application-sources/application/lib/*.jar` to **Referenced Libraries**.

### 4. Change the Java Version to 1.8.0
- Install Java 8:
  ```bash
  sudo apt install openjdk-8-jdk
  ```
- Set Java 8 as default:
  ```bash
  sudo update-alternatives --config java
  ```
  Select Java 8 (e.g., `/usr/lib/jvm/java-8-openjdk-amd64/bin/java`).
- Configure VSCode:
  - Open Command Palette (`Ctrl+Shift+P`, “Java: Configure Java Runtime”).
  - Select JDK 1.8.

### 5. Set Up the `launch.json` (Port 9000)
- In VSCode, open the **Run and Debug** view (`Ctrl+Shift+D`).
- Open the provided launch.json file
- Replace the port to 9000 so that you can debug.

- Find the main class:
  - Check `application.jar`’s `MANIFEST.MF`:
    ```bash
    unzip -p ~/oswe-exam/application.jar META-INF/MANIFEST.MF
    ```
    Look for `Main-Class`.
  - Or search `.java` files in `application-sources` for `public static void main`.
- Update `mainClass` and `projectName` in `launch.json`.
