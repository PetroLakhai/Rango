.PHONY: run
run:
	$(rangoenv) python manage.py runserver

.PHONY: fix
fix:
	$(rangoenv) isort .
	$(rangoenv) black .
