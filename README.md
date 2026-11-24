# storm_software_2027
Code for our entry into the [2027 STORM competition](https://storm.soonerrobotics.org/), name TBD.

# Architecture
The repository is divided into 3 main sections: the Robot code, the Base Station code, and the robot firmware. The robot code is written in Python, and sort of based on last year's code. The base station code is written in HTML/JavaScript, and does away with the separate Python process that we had last year. The firmware is written in C++ using the Arduino library, and is based on work done over the summer that you can find on the `test/stormlib` branch in last year's repository.

TODO: insert diagram here, and maybe a link to the software architecture document.

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

    TODO: instructions for what packages you will need to install for building libhv

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

6. **Build the Websocket Server**:

    TODO: same steps as last year?

That's it! You should be all good to run the robot code now.

## Installation: Base Station
To prepare to run the **base station** code, perform the following steps:

1. **Clone the repository**:

    TODO

2. **???**:
    
    ??? are there any other steps?


# Running
## Robot
To run the robot code, perform the following steps:

TODO: we really should have an auto-run service or something for this...

1. SSH into the robot (TODO: IP address subject to change. definitely at competition there will be a different address)

    ```bash
    ssh scr@192.168.1.79
    ```

2. Navigate to the repository

    ```bash
    cd ~/Documents/storm_software_2027/robot
    ```

3. Start the websocket server

    ```bash
    ./ws_server
    ```

4. Start the robot code

    ```bash
    python3 ./main.py
    ```

## Base Station
To "run" the base station code, simply open `base_station/index.html` in a web browser.

# Button Bindings
The controls for the robot are shown in the diagram below.

TODO: insert diagram

# Firmware
TODO: about the firmware

## Firmware: Installation
To install the firmware on one of the PCBs, perform the following steps. The steps are exactly the same for either the Traversal or Cannon board.

Libraries needed:
 - TODO

# Contributing
TODO: branch names, schemes, PR formats, etc.

Sooner Competitive Robotics, 2027.