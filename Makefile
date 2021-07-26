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
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com;
