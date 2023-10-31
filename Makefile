define docker_build
	docker build -t ravenapp/emh-robot-core:v1.0.0 .
endef

define docker_run
	docker run -it --rm \
		--name emh-robot-core \
		-p 8000:8000 \
		--network v0_emh-robot-net \
		--env-file .env.dev \
		-v $(PWD):/app/ \
		ravenapp/emh-robot-core:v1.0.0
endef

define docker_compose_up
	docker compose --env-file .env.$(1) up -d
endef

define docker_compose_down
	docker compose --env-file .env.$(1) down
endef

define run_python
	CUDA_VISIBLE_DEVICES=0 ENV=$(1) python3 main.py
endef

# Environments
ENVS = dev stag prod

# General Rules
$(ENVS):
	$(call run_python,$@)

$(addsuffix -up,$(ENVS)):
	$(call docker_compose_up,$(subst -up,,$@))

$(addsuffix -run,$(ENVS)):
	$(call docker_run,$(subst -run,,$@))

$(addsuffix -build,$(ENVS)):
	$(call docker_build,$(subst -build,,$@))

$(addsuffix -down,$(ENVS)):
	$(call docker_compose_down,$(subst -down,,$@))

# Example usage:
# make dev - Will run docker compose up with .env.dev and run python script with ENV=dev
# make dev-up - Will only run docker compose up with .env.dev
# make dev-down - Will run docker compose down with .env.dev
