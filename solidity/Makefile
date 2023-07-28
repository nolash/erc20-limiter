SOLC = /usr/bin/solc

all:
	$(SOLC) --bin Limiter.sol --evm-version byzantium | awk 'NR>3' > Limiter.bin
	$(SOLC) --abi Limiter.sol --evm-version byzantium | awk 'NR>3' > Limiter.json
	$(SOLC) --metadata Limiter.sol --evm-version byzantium | awk 'NR>3' > Limiter.metadata.json
	$(SOLC) --bin LimiterTokenRegistry.sol --evm-version byzantium | awk 'NR>7' > LimiterTokenRegistry.bin
	$(SOLC) --abi LimiterTokenRegistry.sol --evm-version byzantium | awk 'NR>7' > LimiterTokenRegistry.json
	$(SOLC) --metadata LimiterTokenRegistry.sol --evm-version byzantium | awk 'NR>7' > LimiterTokenRegistry.metadata.json

	truncate -s -1 Limiter.bin
	truncate -s -1 LimiterTokenRegistry.bin

install: all
	cp -v *.json ../python/erc20_limiter/data/
	cp -v *.bin ../python/erc20_limiter/data/

