user:
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com;

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations timer

cleardb:
	docker compose down
	docker volume prune --force
	docker compose up -d
	sleep 3
	python manage.py makemigrations timer
	python manage.py migrate
	#python manage.py loaddata manager
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com;

save_manager_fixtures:
	python manage.py dumpdata timer.Manager --indent 4 --output timer/fixtures/manager.json

build:
	docker compose up -d  --build

up:
	docker compose up -d

make_requirements:
	pipenv run pip freeze > requirements.txt

dockerbash:
	docker exec -it sandglass_db_1 bash
