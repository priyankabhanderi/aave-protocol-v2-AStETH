using SymbolicLendingPool as LENDING_POOL

methods {
    // Summerizations:
    getPooledEthByShares(uint256 _sharesAmount) returns (uint256) => NONDET

    // Simplifications:



    balanceOf(address) returns (uint256) envfree
    scaledBalanceOf(address) returns (uint256) envfree
    internalBalanceOf(address) returns (uint256) envfree
    getScaledUserBalanceAndSupply(address) returns (uint256, uint256) envfree
    totalSupply() returns (uint256) envfree
    scaledTotalSupply() returns (uint256) envfree
    burn(address, address,uint256, uint256)
    mint(address, uint256, uint256)
    mintToTreasury(uint256, uint256)
    transferOnLiquidation(address, address, uint256)
    transferUnderlyingTo(address, uint256) returns (uint256)
    permit(address, address, uint256, uint256, uint8, bytes32, bytes32)

    // IncentivizedERC20 methods
}

// function onlyLendingPoolModifier() {
//     require e.msg.sender == LENDING_POOL;
// }

/**************************************************
 *               CVL FUNCS & DEFS                 *
 **************************************************/


 /**************************************************
 *                GHOSTS AND HOOKS                *
 **************************************************/


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
    assert false;
}




