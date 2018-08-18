define dw_check_variables
ifndef $1
$$(error Please define the variable '$1')
endif
endef

$(eval $(call dw_check_variables,DW_ROOT_DIR))
$(eval $(call dw_check_variables,DW_CHECK_CODE))
$(eval $(call dw_check_variables,DW_CONTAINER))
$(eval $(call dw_check_variables,DW_CONTAINER_NAME))

DW_RELATIVE_DIR:=$(shell bash -c "root_dir=$(abspath $(DW_ROOT_DIR)); pwd=$(CURDIR); echo \$${pwd\#\$${root_dir}};")

HOST=$(shell if $(DW_CHECK_CODE); then echo "false"; fi)

ifneq ($(HOST),)
# host environment
DW_HOST_DIR:=$(abspath $(DW_ROOT_DIR))
DW_SHARE_DIR:=/share

define docker_wrapper
	@docker rm $1 -f > /dev/null 2>&1 || :
	xhost + 127.0.0.1
	docker run -e DISPLAY=docker.for.mac.localhost:0 -d $(if $(CI),,-v $(DW_HOST_DIR):$(DW_SHARE_DIR)) -it --name $1 $2
	$(if $(CI),docker cp $(DW_HOST_DIR) $1:$(DW_SHARE_DIR))
	docker exec $1 sh -c "cd /share$(DW_RELATIVE_DIR) && $3"
	@echo ""
	docker rm -f $1
endef

.DEFAULT_GOAL:=default
default:
	$(call docker_wrapper,$(DW_CONTAINER_NAME),$(DW_CONTAINER),make)

attach_docker:
	docker exec -it $(DW_CONTAINER_NAME) /bin/bash

run_docker:
	docker run --rm -v $(HOST_DIR):$(DW_SHARE_DIR) -it $(DW_CONTAINER) /bin/bash

%:
	$(call docker_wrapper,$(DW_CONTAINER_NAME),$(DW_CONTAINER),make $@)
else
# guest environment
ifneq ($(PWD),$(CURDIR))
RECURSIVE=true
endif
endif
