# SmartHome_FYP
before run 
use
git clone https://github.com/MatThen912/SmartHome_FYP.git
to clone this project to your vscode
cd SmartHome_FYP --goto the file
py -m venv yourvenvname --create virtual machine
pip install -r requirements.txt --install all package
py manage.py makemigrations
py manage.py migrate
py maage.py runsrever
"""
  IF mean the error "devivce table not found"
  use this
  py manage.py makemigrations devices
  py manage.py migrate devices
