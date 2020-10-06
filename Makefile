lint:
ifndef CI
	docker run -it -e CI='1' -v ${CURDIR}:/src -w /src --rm python make check_code
else
	apt update
	apt install flake8 -y
	flake8 --ignore=E265,E501,W503,W505 --exclude=docs/,submodules/
endif

deadcode:
ifndef CI
	docker run -it -e CI='1' -v ${CURDIR}:/src -w /src --rm python make dead_code
else
	apt update
	apt install vulture -y
	vulture .
endif