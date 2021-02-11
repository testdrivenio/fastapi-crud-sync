all:
	docker-compose up --build --force-recreate --remove-orphans -d

clean:
	docker-compose stop
	docker-compose down -v
