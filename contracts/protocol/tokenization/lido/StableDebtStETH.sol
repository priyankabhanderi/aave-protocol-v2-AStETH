// SPDX-License-Identifier: agpl-3.0
pragma solidity 0.6.12;

import {StableDebtToken} from '../StableDebtToken.sol';

/**
 * @notice stETH specific stable debt token implementation.
 * @dev The StableDebtStETH protects AStETH from usage with stable debt borrowing,
 *   by overriding mint() method. Method mint() reverts with 'CONTRACT_NOT_ACTIVE' method on call.
 **/
contract StableDebtStETH is StableDebtToken {
  constructor(
    address pool,
    address underlyingAsset,
    string memory name,
    string memory symbol,
    address incentivesController
  ) public StableDebtToken(pool, underlyingAsset, name, symbol, incentivesController) {}

  function mint(
    address user,
    address onBehalfOf,
    uint256 amount,
    uint256 rate
  ) external override onlyLendingPool returns (bool) {
    revert('CONTRACT_NOT_ACTIVE');
  }
}
