# storm_software_2027
Code for our entry into the [2027 STORM competition](https://storm.soonerrobotics.org/), name TBD.

# Architecture
The repository is divided into 3 main sections: the Robot code, the Base Station code, and the robot firmware. The robot code is written in Python, and sort of based on last year's code. The base station code is written in HTML/JavaScript, and does away with the separate Python process that we had last year. The firmware is written in C++ using the Arduino library, and is based on work done over the summer that you can find on the `test/stormlib` branch in last year's repository.

More information can be found in the [STORM 2027 Software Architecture](https://docs.google.com/document/d/16evtjG1M5LncGTOwgNlK3MpllWmala_v4nvgPZLWfDY/edit?tab=t.0) document.

# Installation

## Installation: Robot
**NOTE**: You will need Python >= 3.15 installed!

To prepare to run the **Robot** code, follow these steps:

1. **Clone the Repository**:

    HTTPS: `git clone https://github.com/SoonerRobotics/storm_software_2027.git`
    SSH: `git@github.com:SoonerRobotics/storm_software_2027.git`

2. **Setup the Virtual Environment**:

   **Windows:**

   ```powershell
   py -m venv venv
   venv\Scripts\activate
   ```

   > **PowerShell users:** if `venv\Scripts\activate` fails with "running scripts is disabled on this system", run the command below, then run `venv\Scripts\activate` again. It only applies to the current PowerShell window.
   >
   > ```powershell
   > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   > ```


   **macOS/Linux:**

   ```bash
   python3.15 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Libhv**:

    If you do not already have libhv from last year, perform the following steps (5-6) to install it.

    Clone the repository if you don't already have it (in a different location from the STORM repository):

    `git clone https://github.com/ithewei/libhv.git`

    If you do not have a compiler, try

    ```bash
    sudo apt install build-essential cmake
    ```

5. **Install libhv**:

    Navigate to the libhv repository you just downloaded, and install it.

    ```bash
    cd libhv
    mkdir build
    cd build

    cmake ..
    cmake --build .
    sudo make install
    ```

6. **Clone the Websocket Server**:

    ```bash
    git clone https://github.com/antonioc76/Sockets-U-Serialization.git
    cd Sockets-U-Serialization
    ```

7. **Build & Install the Websocket Server**:

    ```bash
    mkdir build
    cmake -S ./ws_server -B ./build -DCMAKE_CXX_COMPILER=g++-13
    cmake --build ./build
    ```

That's it! You should be all good to run the robot code now.

## Installation: Base Station
There are no installation instructions for the base station code. Just clone the repository, and then follow the instructions below to run it.

# Running
## Robot
To run the robot code, perform the following steps:

TODO: we really should have an auto-run service or something for this...

TODO: also, we will need to change the IP address somewhere in the code, probably for both robot and base station. add a step for where it needs to be changed.

1. SSH into the robot

    ```bash
    ssh scr@192.168.1.79
    ```

2. Navigate to the websocket server repository

    ```bash
    cd ~/Documents/Sockets-U-Serialization/
    ```

3. Start the websocket server

    ```bash
    ./ws_server
    ```

4. Navigate to the STORM 2027 repository

    ```bash
    cd ~/Documents/storm_software_2027/robot
    ```


5. Start the robot code

    ```bash
    python3 ./main.py
    ```

## Base Station
To "run" the base station code, simply open `base_station/index.html` in a web browser.

# Button Bindings
The (tentative) controls for the robot are shown in the diagram below.

![STORM 2027 button bindings](<diagrams/STORM 2027 Controller Button Bindings.png>)

# Firmware
The firmware features an entirely new communications library, StormLib, for sending custom messages back and forth over RS-485. The full details are explained in the [STORM 2027 Serial Specification](https://docs.google.com/document/d/12uRvUI1vzKqb39eKWllWqqgihEtoIuftWWLzEFsb1ek/edit?tab=t.0), but the gist of it is that there are variable-length *Commands*, *Requests*, and *Responses*. Only the robot's computer is allowed to initiate communication, and individual board firmware only ever receives messages, or responds to an explicit *request* from the computer, and never sends messages of its own volition. This is described by the diagram below.

![firmware flowchart](<diagrams/Software Firmware Interface.drawio.png>)

## Firmware: Installation
To install the firmware on one of the PCBs, perform the following steps. The steps are exactly the same for either the Traversal or Cannon board, though the actual file you are uploading will be different.

1. Download and install the Arduino IDE from https://www.arduino.cc/en/software/

2. Install Earl's Arduino Pico Library by following the instructions in the [README](https://github.com/earlephilhower/arduino-pico), you may have to scroll down to find them.

3. Install the other following libraries:

    ```
    TODO...? RS-485? Servo?
    ```

# Contributing
We don't have to be super formal, especially with the lack of experienced software members, so just stick to the following general rules:
 * Prefix branch names with either `feat/` or `bug/` or `test/`, depending on what the branch is.
 * **Never** push directly to main, open a pull request and have at least 1 other member review it.
 * Don't clutter the repository with build files or other files generated by tools. If you need help adding something to the `.gitignore`, just ask.
 * Python class names are PascalCase, function names are snake_case, all file names are snake_case_like_this.
 * Otherwise, follow PEP 8 for other style guidelines I guess?
 * Folder names are snake_case / lowercase.


Software development done by Daniel Brown (captain), Brendan Richards, Josh Kernop, and Saul Harrison.
Firmware development done by Daniel Brown (captain), Tyler Afonien, Evan Woods, and  Diego Barrios.
Special thanks to mentors/alumni Noah Zemlin, Braden White, Dylan Zemlin, and Tyler Julian.

STORM Software 2027, Sooner Competitive Robotics.