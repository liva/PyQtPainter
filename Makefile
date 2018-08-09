# sample
DW_CHECK_CODE:=[ ! -e /cpputest/lib/libCppUTest.a ]
DW_CONTAINER:=livadk/cpputest:aac118d572d3c41bc9e3bed32c7ae8c19249784c
DW_CONTAINER_NAME:=docker_wrapper_sample

include rules.mk

ifeq ($(HOST),)

.PHONY: hello

default: hello

hello:
	@echo "<<<<'hello!' from docker enviroment.>>>>"
	uname -r
endif