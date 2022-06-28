import "./AStETH_summerizations.spec"

using SymbolicLendingPool as LENDING_POOL
using DummyERC20A as UNDERLYING_ASSET
using DummyERC20B as RESERVE_TREASURY

methods {    

    getRevision() returns (uint256)
    initialize(uint8, string, string) envfree
    balanceOf(address) returns (uint256) envfree
    scaledBalanceOf(address) returns (uint256) envfree
    internalBalanceOf(address) returns (uint256) envfree
    getScaledUserBalanceAndSupply(address) returns (uint256, uint256) envfree
    totalSupply() returns (uint256) envfree
    scaledTotalSupply() returns (uint256) envfree
    internalTotalSupply() returns (uint256) envfree
    burn(address, address,uint256, uint256)
    mint(address, uint256, uint256)
    mintToTreasury(uint256, uint256)
    transferOnLiquidation(address, address, uint256) 
    transferUnderlyingTo(address, uint256) returns (uint256) 
    permit(address, address, uint256, uint256, uint8, bytes32, bytes32) 

    isContractIsTrue(address) returns (bool) envfree

    UNDERLYING_ASSET.balanceOf(address) returns (uint256) envfree
    UNDERLYING_ASSET.totalSupply() returns (uint256) envfree

    LENDING_POOL.aToken() returns (address) envfree

}

rule balanceChangeIntegrity()
{
    address user1;
     address user2;
      method f;

	env e;
	require user1!=user2;
	uint256 beforeBalanceA = balanceOf(user1);
	uint256 beforeBalanceB = balanceOf(user2);
	 
	calldataarg arg;
	f(e, arg); 
	uint256 afterBalanceA = balanceOf(user1);
	uint256 afterBalanceB = balanceOf(user2);
	
	assert (beforeBalanceA == afterBalanceA || beforeBalanceB == afterBalanceB || 
        (beforeBalanceA != afterBalanceA && 
        beforeBalanceB != afterBalanceB && 
        beforeBalanceA+beforeBalanceB == afterBalanceA+afterBalanceB)
    );
}

rule MintIntegrity(address user, uint256 amount, uint256 index) {
	env e;
    mathint earlyTotalSupply = totalSupply();
    mathint earlyBalance = balanceOf(user);
    mint(e, user, amount, index);
    mathint totalSupplyAfter = totalSupply();
    mathint balanceAfter = balanceOf(user);
    assert e.msg.sender == LENDING_POOL;
    assert amount != 0 => earlyTotalSupply < totalSupplyAfter;
    assert amount != 0 => earlyBalance < balanceAfter;
}

rule mintAdditive(address user, uint256 amount1, uint256 amount2, uint256 index) {
    env e;
	storage initialStorage = lastStorage;
	mint(e, user, amount1, index);
	mint(e, user, amount2, index);
	mathint balance1 = balanceOf(user);
    mathint totalSupply1 = totalSupply();
	uint256 amount = amount1 + amount2;
	mint(e, user, amount, index) at initialStorage;
	mathint balance2 = balanceOf(user);
    mathint totalSupply2 = totalSupply();
	assert balance1 == balance2, "mint is not additive";
    assert totalSupply1 == totalSupply2;
}