using SymbolicLendingPool as LENDING_POOL

methods {
    // Summerizations:
    // getPooledEthByShares(uint256 _sharesAmount) returns (uint256) => NONDET

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



