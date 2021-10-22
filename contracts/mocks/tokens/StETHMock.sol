pragma solidity 0.8.9;

contract StETHMock {
  uint256 public decimals = 18;
  uint256 public totalSupply = 1;
  uint256 public totalShares = 1;
  string public symbol = 'stETH';

  function getSharesByPooledEther(uint256 _ethAmount) public view returns (uint256) {
    return (_ethAmount * totalShares) / totalSupply;
  }

  function getPooledEtherByShares(uint256 _sharesAmount) public view returns (uint256) {
    return (_sharesAmount * totalSupply) / totalShares;
  }
}
