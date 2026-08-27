# Colibri Assessment
My solution to Colibri's take home assessment
**Prerequisites for use**

Python, Java and Git must all be installed on local machine. To check, run this command in a powershell terminal.
    
- **Python** — https://www.python.org/downloads/
  During install, tick "Add python.exe to PATH".
- **Java** — required by PySpark. https://adoptium.net/
  During install, ensure "Set JAVA_HOME" and "Add to PATH" are enabled.
- **Git** — https://git-scm.com/
  Use default options during install.
    
To verify each is installed correctly:

    python --version
    java -version
    git --version

## Instructions to run

This project was created and tested on Windows and as such the below setup instructions are Windows-specific. All lines of code should be run in a PowerShell terminal.

1. Clone the repo onto your local machine and change directory.
   
        git clone https://github.com/harrisonward1311/colibri_assessment.git
        cd colibri_assessment

2. Run setup PowerShell script. This will create and activate the virtual environment, install dependencies and setup the .env file.

        .\setup.ps1

3. Run main script. Currently all API data is already loaded in data/raw_stock_prices for speed purposes. If you want to run a full load, you can set the refresh_data flag to True in the main.py script. Optionally, you can delete specific files from storage and only those will be ingested from the API in the run. 
   
        py .\src\turbine_pipeline\main.py

4. To open results file in notepad, run the below code in PowerShell terminal.

       notepad output/summary.csv

    
