test:
	coverage run --branch --source=floppyforms `which django-admin.py` test floppyforms
	coverage report --omit=floppyforms/test*
