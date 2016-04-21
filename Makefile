.PHONY: build install-bin install-init-script install

build:
	python setup.py build

install-bin: build
	python setup.py install

install-init-script:
	cp tbprocessd.service /etc/init.d

install: install-tbprocessd install-init-script
