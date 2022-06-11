certoraRun contracts/protocol/tokenization/lido/AStETH.sol:AStETH certora/harness/DummyERC20A.sol certora/harness/SymbolicLendingPool.sol certora/harness/IncentivesControllerMock.sol certora/harness/DummyERC20B.sol \
    --verify AStETH:certora/specs/complexity.spec \
    --link AStETH:UNDERLYING_ASSET_ADDRESS=DummyERC20A AStETH:POOL=SymbolicLendingPool AStETH:_incentivesController=IncentivesControllerMock AStETH:RESERVE_TREASURY_ADDRESS=DummyERC20B \
    --solc solc6.12 \
    --optimistic_loop \
    --staging \
    --msg "AStETH complexity check"
