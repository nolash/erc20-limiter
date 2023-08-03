# erc20-limiter

These smart contract implementations define value limits for tokens by holders.

The contracts satisfy the [CIC TokenLimit](https://git.grassecon.net/cicnet/cic-contracts/#tokenlimit) interface.


## Defining limits

The `setLimit(token, value)` method set the limit of `token` that the transaction signer will accept to `value`.

Values are _inclusive_; if `42` is returned, a balance up to and including `42` should be approved.

A limit of `0` means that the "holder" will categorically not accept a token.


### Defining limits for contracts

An alternative `setLimitFor(token, holder, value)` method exists, where the contract `owner` may change the limit for a _smart contract_.

If smart contract capable of transacting against this method itself does so, the result is the same as if that contract called `setLimit()`.

The `owner` for the contract defined and managed according to the [ERC173](https://eips.ethereum.org/EIPS/eip-173) standard.


## Honoring limits

Limits will only be honored if integrated into the proper context.

One example of context is to implement a limit check in the `transfer` and `transferFrom` methods of ERC20 tokens.


## ACL Index variant

The `LimitIndex.sol` contract variant includes an implementation of the [CIC ACL](https://git.grassecon.net/cicnet/cic-contracts/#acl) interface.

In this case, any non-zero limit of a token for a holder results in a `true` value being returned. Otherwise, `false` is returned.

The `LimitIndex.sol` contract takes a regular `Limit.sol` token address as argument, or more specifically a contract that satisfies this interface:

```
interface Limiter {
	function limitOf(address,address) external view returns(uint256);
	function setLimit(address,uint256) external;
	function setLimitFor(address,address,uint256) external;
}
```
