# "Unit" Tests (actually e2e tests)

Install requirements and run unit tests (run from api directory of repo):

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt -r test/requirements.txt
    venv/bin/python -m unittest discover test/
