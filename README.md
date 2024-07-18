# Schedule Compiler
This is a desktop application for Temple students that generates potential schedules for their next semester based on desired courses, professor ratings, and days they cannot attend class.

# How to run

## For Windows
1. Click on Releases to get the latest release
2. Click on zip file to download it
3. Go to the folder where you downloaded the zip file
4. Right-click on the zip file and click "Extract all"
5. Pick a folder to extract the file(s) to
6. Double-click on schedule_compiler.exe in the folder you selected to extract the file to to run

## For Linux
1. Click on Releases to get the latest release
2. Click on the tar.gz file to download it
3. In your terminal, navigate to the directory where the file was downloaded
4. Enter "tar -xvzf " and then the file name in the terminal and click enter
5. Type "./schedule_compiler" to run


# How to contribute
Follow this project board to know the latest status of the project in the project board. Submit a PR with working code.

### How to build

- Clone the repository in your desired IDE that works with Python
- Set up the virtual environment (done only once):
    - For Windows, run "py -3 -m venv .venv"
    - For Linux, run "python3 -m venv .venv"
-Run the virtual environment (done every time you open up the project):
    - For Windows, run ".venv/scripts/activate"
    - For Linux, run "source .venv/bin/activate"
- Run "pip install -r requirements.txt"
- In Linux, run "sudo apt-get install python3-tk"
- Run schedule_compiler.py
- User interface should show up with title "Schedule Compiler" and options for preferences in schedule creation
