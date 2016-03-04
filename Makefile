.PHONY: build install

BUILD_ROOT = build
BIN := $(BUILD_ROOT)/usr/bin

build:
	rm -rf $(BUILD_ROOT) || true
	mkdir -p "$(BIN)"
	install -m 755 tbopen $(BIN)
	install -m 755 tbtail $(BIN)
	install -m 755 main.py $(BIN)/tbprocessd
	mkdir -p "$(BUILD_ROOT)/etc/init"
	install -m 644 upstart.conf $(BUILD_ROOT)/etc/init/tbprocessd.conf
	mkdir -p "$(BUILD_ROOT)/etc/init.d"
	install -m 755 init.sh $(BUILD_ROOT)/etc/init.d/tbprocessd

install: build
	rsync -rl --exclude '.DS_Store' build/* /
