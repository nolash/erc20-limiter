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
	address public owner;
	Limiter limiter;
	address holder;

	// Implements EIP173
	event OwnershipTransferred(address indexed previousOwner, address indexed newOwner); // EIP173


	constructor(address _holder, Limiter _limiter) {
		owner = msg.sender;
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
		require(msg.sender == owner || msg.sender == _holder, 'ERR_AXX');
		limiter.setLimitFor(_token, _holder, _value);
	}

	// Implements ACL
	function have(address _token) public view returns(bool) {
		return limiter.limitOf(_token, holder) > 0;
	}

	// Implements EIP173
	function transferOwnership(address _newOwner) public returns (bool) {
		address oldOwner;

		require(msg.sender == owner);
		oldOwner = owner;
		owner = _newOwner;

		emit OwnershipTransferred(oldOwner, owner);
		return true;
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // ERC165
			return true;
		}
		if (_sum == 0x3ef25013) { // ACL
			return true;
		}
		if (_sum == 0x23778613) { // TokenLimit
			return true;
		}
		if (_sum == 0x9493f8b2) { // ERC173
			return true;
		}
		return false;
	}
}
