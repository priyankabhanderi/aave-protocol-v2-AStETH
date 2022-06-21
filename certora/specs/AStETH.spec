import "./AStETH_summerizations.spec"

using SymbolicLendingPool as LENDING_POOL
using DummyERC20A as UNDERLYING_ASSET
using DummyERC20B as RESERVE_TREASURY

methods {    

    getRevision() returns (uint256) envfree
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

    // IncentivizedERC20 methods:
    // handleAction(address user, uint256 userBalance, uint256 totalSupply) => DISPATCHER(true)
}

/**************************************************
 *               CVL FUNCS & DEFS                 *
 **************************************************/


 /**************************************************
 *                GHOSTS AND HOOKS                *
 **************************************************/

//  ghost totalSupply


 /**************************************************
 *                  VALID STATES                  *
 **************************************************/


 /**************************************************
 *                STATE TRANSITION                *
 **************************************************/


 /**************************************************
 *                METHOD INTEGRITY                *
 **************************************************/

//  deposit X stETH to mint X astETH * Total astETH supply increases by X.

rule integrityOfMint(address user, uint256 amount, uint256 index) {
	env e;
    // for onlyLendingPool modifier
    require e.msg.sender == LENDING_POOL;

    mathint totalSupplyBefore = totalSupply();
    mint(e, user, amount, index);
    mathint totalSupplyAfter = totalSupply();

    assert amount != 0 => totalSupplyBefore < totalSupplyAfter;
}


rule integrityOfTransferUnderlyingTo(address user, uint256 amount) {
    env e;
    // for onlyLendingPool modifier
    require e.msg.sender == LENDING_POOL;
    require user != currentContract;

    mathint totalSupplyBefore = totalSupply();
    mathint userBalanceBefore = balanceOf(user);

    uint256 amountTransfered = transferUnderlyingTo(e, user, amount);

    mathint totalSupplyAfter = totalSupply();
    mathint userBalanceAfter = balanceOf(user);

    assert userBalanceAfter == userBalanceBefore + amountTransfered;
}


rule AtokensPeggedToUndeerlyingBurn(address user, uint256 amount, uint256 index, address reciver){
    env e;
    // for onlyLendingPool modifier
    require e.msg.sender == LENDING_POOL;
    uint256 _ATokenBalance = internalBalanceOf(user);
    uint256 _ATokenTotalSupply = internalTotalSupply();
    mint(e, user, amount, index);
    burn(e, user, reciver, amount, index);
    uint256 ATokenBalance_ = internalBalanceOf(user);
    uint256 ATokenTotalSupply_ = internalTotalSupply();
    assert _ATokenBalance == ATokenBalance_;
    assert _ATokenTotalSupply == ATokenTotalSupply_;
}