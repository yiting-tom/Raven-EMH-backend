dev:
	ENV=dev python3 main.py

docker_build:
	docker build \
		--build-arg MONGO_INITDB_ROOT_USERNAME=raven \
		--build-arg MONGO_INITDB_ROOT_PASSWORD=TLd2DVeAXdKC77nblKCKXpBK0COWU92zp9rc \
		-t raven-emh-robot:v6-wcuda .
