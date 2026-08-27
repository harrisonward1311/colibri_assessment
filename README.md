# Colibri Assessment
My solution to Colibri's take home assessment.

The code is split into separate python files.
- **main.py** sequentially runs the functions defined in the below.
- **ingest.py** loads the provided CSV files into a single raw Spark DataFrame.
- **clean.py** removes NULLs, duplicates and outliers from the raw DataFrame. Currently only outliers from the wind speed column are removed, but the functionality is there to add other columns.
- **summarise.py** creates the results table as specified in the spec. Each turbine has a min, max and average power output over a given time period, as well as two flags identifying whether the time period mean is under/over 2 standard deviations from the expected mean. The given time period is defined in **main.py** and the expected mean is calculated from all the data *excluding* the data from the given time period. 

## Prerequisites for use

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

3. Run main script. 
   
        py .\src\turbine_pipeline\main.py

4. To open results file in notepad, run the below code in PowerShell terminal.

       notepad (Get-ChildItem "output/summary" -Filter "part-*.csv" | Select-Object -First 1 -ExpandProperty FullName)

    
