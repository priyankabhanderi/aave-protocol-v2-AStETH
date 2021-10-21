// SPDX-FileCopyrightText: 2020 Lido <info@lido.fi>
// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.6.12;

import {SafeMath} from '../../dependencies/openzeppelin/contracts/SafeMath.sol';

contract stETHMocked {
  using SafeMath for uint256;

  uint256 private _totalSupply;
  uint256 private _totalShares;
  mapping(address => uint256) _shares;

  function _getPooledEthByShares(uint256 _sharesAmount) internal view returns (uint256) {
    return _sharesAmount.mul(_totalSupply).div(_totalShares);
  }

  function _getSharesByPooledEth(uint256 _pooledEthAmount) internal view returns (uint256) {
    return _pooledEthAmount.mul(_totalShares).div(_totalSupply);
  }

  function totalSupply() external view returns (uint256) {
    return _totalSupply;
  }

  /**
   * @notice Increases shares of a given address by the specified amount.
   *
   * @param _to Receiver of new shares
   * @param _sharesAmount Amount of shares to mint
   * @return The total amount of all holders' shares after new shares are minted
   */
  function mintShares(address _to, uint256 _sharesAmount) external returns (uint256) {
    _shares[_to] = _shares[_to].add(_sharesAmount);
    _totalShares = _totalShares.add(_sharesAmount);

    return _totalShares;
  }

  function getTotalShares() external view returns (uint256) {
    return _totalShares;
  }

  function balanceOf(address owner) external view returns (uint256) {
    uint256 _sharesOf = _shares[owner];
    if (_sharesOf == 0) {
      return 0;
    }
    return _getPooledEthByShares(_sharesOf);
  }

  function getPooledEthByShares(uint256 _sharesAmount) external view returns (uint256) {
    return _getPooledEthByShares(_sharesAmount);
  }

  function getSharesByPooledEth(uint256 _pooledEthAmount) external view returns (uint256) {
    return _getSharesByPooledEth(_pooledEthAmount);
  }
}
