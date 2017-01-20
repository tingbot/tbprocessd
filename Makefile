.PHONY: build install-bin install-init-script install

install:
	pip uninstall tbprocessd
	pip install .
