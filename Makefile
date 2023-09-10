DOTENV_FILE=.env.dev
GTADIENT_SPEC_FILE=gradient-deployment.yaml

-include DOTENV_FILE

run:
	CUDA_VISIBLE_DEVICES=0 ENV=staging python3 main.py

dev:
	CUDA_VISIBLE_DEVICES=0 ENV=dev python3 main.py

docker_build:
	docker build -t $(PAPER_SPACE_DEPLOY_IMAGE) .

docker_run:
	docker run --gpus all -it \
		-p $(APP_PORT):$(APP_PORT) \
		--env-file $(DOTENV_FILE) \
		$(PAPER_SPACE_DEPLOY_IMAGE)

docker_run_bash:
	docker run --gpus all -it \
		-p $(APP_PORT):$(APP_PORT) \
		--env-file $(DOTENV_FILE) \
		--entrypoint /bin/bash \
		$(PAPER_SPACE_DEPLOY_IMAGE)

generate_gradient_spec:
	bash scripts/make_spec_from_env.sh -e $(DOTENV_FILE) -o $(GTADIENT_SPEC_FILE)

create_gradient_deployment: generate_gradient_spec
	gradient deployments create \
		--apiKey $(PAPER_SPACE_API_KEY)
		--project_id $(PAPER_SPACE_DEPLOY_PROJECT_ID) \
		--name $(APP_NAME)\
		--spec $(GTADIENT_SPEC_FILE)