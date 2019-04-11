-- make virtual env
python -m venv env

-- activate venv
source env/bin/activate

-- activate in windows
./env/Scripts/Activate.ps1


-- deactivate venv (even on windows)
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

# Tutorials
https://blog.morizyun.com/python/library-boto3-aws-dynamodb.html

#To Do
- add tags to resources (done)
- play with indexes
- put python stuff in a separate directory
- make a directory for front end??
- reduce memory for lambdas
- use ssm (done)
- make functoin parameters correct
- purge functionality
- get tweet functionality
- cost control limits

# gotchas
- make sure to save requirements.txt in utf-8
- to reduce size of zip uploaded try https://github.com/UnitedIncome/serverless-python-requirements