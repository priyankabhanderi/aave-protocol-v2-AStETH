// SPDX-License-Identifier: agpl-3.0
pragma solidity 0.6.12;

import {IVariableDebtToken} from '../../../interfaces/IVariableDebtToken.sol';
import {IAaveIncentivesController} from '../../../interfaces/IAaveIncentivesController.sol';
import {WadRayMath} from '../../libraries/math/WadRayMath.sol';
import {Errors} from '../../libraries/helpers/Errors.sol';
import {DebtTokenBase} from '../base/DebtTokenBase.sol';
import {ISTETH} from '../../../interfaces/ISTETH.sol';
import {ILendingPool} from '../../../interfaces/ILendingPool.sol';
import {IERC20} from '../../../dependencies/openzeppelin/contracts/IERC20.sol';
import {SafeMath} from '../../../dependencies/openzeppelin/contracts/SafeMath.sol';
import {SignedSafeMath} from '../../../dependencies/openzeppelin/contracts/SignedSafeMath.sol';

interface ILido {
  function getPooledEthByShares(uint256 _sharesAmount) external view returns (uint256);

  function getSharesByPooledEth(uint256 _pooledEthAmount) external view returns (uint256);
}

contract VariableDebtStETH is DebtTokenBase, IVariableDebtToken {
  using WadRayMath for uint256;
  using SafeMath for uint256;
  using SignedSafeMath for int256;

  uint256 public constant DEBT_TOKEN_REVISION = 0x1;

  uint256 public _totalSharesBorrowed;
  uint256 public _totalStEthBorrowed;
  mapping(address => uint256) _stETHBorrows;

  constructor(
    address pool,
    address underlyingAsset,
    string memory name,
    string memory symbol,
    address incentivesController
  ) public DebtTokenBase(pool, underlyingAsset, name, symbol, incentivesController) {}

  /**
   * @dev Gets the revision of the stable debt token implementation
   * @return The debt token implementation revision
   **/
  function getRevision() internal pure virtual override returns (uint256) {
    return DEBT_TOKEN_REVISION;
  }

  /**
   * @dev Calculates the accumulated debt balance of the user
   * @return The debt balance of the user
   **/
  function balanceOf(address user) public view virtual override returns (uint256) {
    uint256 scaledBalance = super.balanceOf(user);

    if (scaledBalance == 0) {
      return 0;
    }

    return scaledBalance.rayMul(POOL.getReserveNormalizedVariableDebt(UNDERLYING_ASSET_ADDRESS));
  }

  function mint(
    address user,
    address onBehalfOf,
    uint256 amount,
    uint256 index
  ) external override onlyLendingPool returns (bool) {
    if (user != onBehalfOf) {
      _decreaseBorrowAllowance(onBehalfOf, user, amount);
    }

    uint256 previousBalance = super.balanceOf(onBehalfOf);
    uint256 amountScaled = amount.rayDiv(index);
    require(amountScaled != 0, Errors.CT_INVALID_MINT_AMOUNT);

    _mint(onBehalfOf, amountScaled);
    _totalSharesBorrowed = _totalSharesBorrowed.add(
      ILido(UNDERLYING_ASSET_ADDRESS).getSharesByPooledEth(amount)
    );
    _totalStEthBorrowed = _totalStEthBorrowed.add(amount);
    _stETHBorrows[user] = _stETHBorrows[user].add(amount);

    emit Transfer(address(0), onBehalfOf, amount);
    emit Mint(user, onBehalfOf, amount, index);

    return previousBalance == 0;
  }

  /**
   * @dev Burns user variable debt
   * - Only callable by the LendingPool
   * @param user The user whose debt is getting burned
   * @param amount The amount getting burned
   * @param index The variable debt index of the reserve
   **/
  function burn(
    address user,
    uint256 amount,
    uint256 index
  ) external override onlyLendingPool {
    uint256 amountScaled = amount.rayDiv(index);
    require(amountScaled != 0, Errors.CT_INVALID_BURN_AMOUNT);

    _burn(user, amountScaled);
    // _totalSharesBorrowed = _totalSharesBorrowed.sub(
    //   int256(ILido(UNDERLYING_ASSET_ADDRESS).getSharesByPooledEth(amount))
    // );
    // if (_stETHBorrows[user] >= amount) {
    //   _totalStEthBorrowed = _totalStEthBorrowed.sub(amount);
    //   _stETHBorrows[user] = _stETHBorrows[user].sub(amount);
    // } else {
    //   _totalStEthBorrowed = _totalStEthBorrowed.sub(_stETHBorrows[user]);
    //   _stETHBorrows[user] = 0;
    // }

    emit Transfer(user, address(0), amount);
    emit Burn(user, amount, index);
  }

  /**
   * @dev Returns the principal debt balance of the user from
   * @return The debt balance of the user since the last burn/mint action
   **/
  function scaledBalanceOf(address user) public view virtual override returns (uint256) {
    return _scaledBalanceOf(user);
  }

  /**
   * @dev Returns the total supply of the variable debt token. Represents the total debt accrued by the users
   * @return The total supply
   **/
  function totalSupply() public view virtual override returns (uint256) {
    return
      _scaledTotalSupply().rayMul(POOL.getReserveNormalizedVariableDebt(UNDERLYING_ASSET_ADDRESS));
  }

  /**
   * @dev Returns the scaled total supply of the variable debt token. Represents sum(debt/index)
   * @return the scaled total supply
   **/
  function scaledTotalSupply() public view virtual override returns (uint256) {
    return _scaledTotalSupply();
  }

  /**
   * @dev Returns the principal balance of the user and principal total supply.
   * @param user The address of the user
   * @return The principal balance of the user
   * @return The principal total supply
   **/
  function getScaledUserBalanceAndSupply(address user)
    external
    view
    override
    returns (uint256, uint256)
  {
    return (_scaledBalanceOf(user), _scaledTotalSupply());
  }

  function _rebasingIndex() internal view returns (uint256) {
    return ILido(UNDERLYING_ASSET_ADDRESS).getPooledEthByShares(1e27);
  }

  function _scaledBalanceOf(address user) internal view returns (uint256) {
    return super.balanceOf(user); //.rayMul(_rebasingIndex());
  }

  function _scaledTotalSupply() internal view returns (uint256) {
    return super.totalSupply(); //.rayMul(_rebasingIndex());
  }

  function getBorrowData() external view returns (uint256, uint256) {
    return (_totalStEthBorrowed, _totalSharesBorrowed);
  }
}
