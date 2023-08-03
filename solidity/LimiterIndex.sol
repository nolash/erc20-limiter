pragma solidity ^0.8.0;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier: AGPL-3.0-or-later
// File-Version: 1
// Description: Registry of allowed ERC20 balance limits per-token and per-holder.

interface Limiter {
	function limitOf(address,address) external view returns(uint256);
	function setLimit(address,uint256) external;
	function setLimitFor(address,address,uint256) external;
}

contract LimiterTokenRegistry {
	Limiter limiter;
	address holder;

	constructor(address _holder, Limiter _limiter) {
		holder = _holder;
		limiter = _limiter;
	}

	function limitOf(address _token, address _holder) public view returns (uint256) {
		return limiter.limitOf(_token, _holder);
	}

	function setLimit(address _token, uint256 _value) public {
		setLimitFor(_token, msg.sender, _value);
	}

	function setLimitFor(address _token, address _holder, uint256 _value) public {
		limiter.setLimitFor(_token, _holder, _value);
	}

	function have(address _token) public view returns(bool) {
		return limiter.limitOf(_token, holder) > 0;
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // ERC165
			return true;
		}
		if (_sum == 0xb7bca625) { // AccountsIndex
			return true;
		}
		if (_sum == 0x23778613) { // TokenLimit
			return true;
		}
		return false;
	}
}
