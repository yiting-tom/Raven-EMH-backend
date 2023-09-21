run:
	CUDA_VISIBLE_DEVICES=0 python3 main.py

staging:
	CUDA_VISIBLE_DEVICES=0 ENV=staging python3 main.py

dev:
	docker compose --env-file .env.dev up -d
	CUDA_VISIBLE_DEVICES=0 ENV=dev python3 main.py