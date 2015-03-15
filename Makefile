.PHONY: build install

BIN := /usr/local/bin/

build:
	install -m 755 tbopen $(BIN)
	install -m 755 tbtail $(BIN)
	install -m 755 main.py $(BIN)/tbprocessd

install:
	rsync -rl --exclude '.DS_Store' build/* /
