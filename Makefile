local_lint:
ifndef CI
	docker run -it -e CI='1' -v ${CURDIR}:/src -w /src --rm python make local_lint
else
	apt update
	apt install flake8 -y
	$(MAKE) lint
endif

local_deadcode:
ifndef CI
	docker run -it -e CI='1' -v ${CURDIR}:/src -w /src --rm python make local_deadcode
else
	apt update
	apt install vulture -y
	$(MAKE) deadcode
endif

lint:
	flake8 --ignore=E265,E501,W503,W505 --exclude=docs/,submodules/ .

deadcode:
	vulture .
