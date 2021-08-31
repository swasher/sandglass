restore_from_production:
	pyinfra inventory.py backup_prod_sql.py -vvv
	pyinfra inventory.py get_latest_backup.py -vvv
	pyinfra inventory.py restore_devdb_from_file.py -vvv

deploy:
	pyinfra inventory.py deploy.py
