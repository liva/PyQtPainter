# sample
DW_ROOT_DIR=$(CURDIR)
DW_CHECK_CODE:=[ ! -e /etc/docker_pyside_env ]
DW_CONTAINER:=livadk/pyside:35e18d2f8b9111c94675c187ffeffb6f32739196
DW_CONTAINER_NAME:=docker_pyside_sample

include docker_wrapper/rules.mk

ifeq ($(HOST),)

.PHONY: hello

default: hello

hello:
	python test.py
	uname -r
endif
