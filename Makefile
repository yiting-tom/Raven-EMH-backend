dev:
	CUDA_VISIBLE_DEVICES=0 ENV=dev python3 main.py

docker_build:
	docker build \
		--build-arg MONGO_INITDB_ROOT_USERNAME=raven \
		--build-arg MONGO_INITDB_ROOT_PASSWORD=TLd2DVeAXdKC77nblKCKXpBK0COWU92zp9rc \
		-t raven-emh-robot:v1.0 .

docker_run:
	docker run -it \
		-p 8000:8000 \
		--env-file .env.dev \
		raven-emh-robot:v1.0

docker_run_bash:
	docker run --gpus all -it \
		-p 8000:8000 \
		--env-file .env.dev \
		--entrypoint /bin/bash \
		raven-emh-robot:v1.0
