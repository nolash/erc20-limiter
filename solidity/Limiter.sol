pragma solidity ^0.8.0;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier: AGPL-3.0-or-later
// File-Version: 1
// Description: Registry of allowed ERC20 balance limits per-token and per-holder.

contract Limiter {
	mapping ( address => mapping ( address => uint256 ) ) public limitOf;

	function setLimit(address _token, uint256 _value) public {
		limitOf[_token][msg.sender] = _value;
	}
}
