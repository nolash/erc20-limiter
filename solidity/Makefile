SOLC = /usr/bin/solc

all:
	$(SOLC) --bin Limiter.sol --evm-version byzantium | awk 'NR>3' > Limiter.bin
	$(SOLC) --abi Limiter.sol --evm-version byzantium | awk 'NR>3' > Limiter.json
	$(SOLC) --metadata Limiter.sol --evm-version byzantium | awk 'NR>3' > Limiter.metadata.json
	$(SOLC) --bin LimiterIndex.sol --evm-version byzantium | awk 'NR>7' > LimiterIndex.bin
	$(SOLC) --abi LimiterIndex.sol --evm-version byzantium | awk 'NR>7' > LimiterIndex.json
	$(SOLC) --metadata LimiterIndex.sol --evm-version byzantium | awk 'NR>7' > LimiterIndex.metadata.json

	truncate -s -1 Limiter.bin
	truncate -s -1 LimiterIndex.bin

install: all
	cp -v *.json ../python/erc20_limiter/data/
	cp -v *.bin ../python/erc20_limiter/data/

