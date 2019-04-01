-- make virtual env
python -m venv env

-- activate venv
source env/bin/activate

-- activate in windows
./env/Scripts/Activate.ps1


-- deactivate venv
(env) $ deactivate

-- other commands
which python

pip install <package>

echo $PATH

-- https://realpython.com/python-virtual-environments-a-primer/


pip freeze > requirements.txt
pip install -r requirements.txt


# unicode error in poweshell
run chcp 65001