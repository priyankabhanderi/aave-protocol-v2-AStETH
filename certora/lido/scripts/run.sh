certoraRun certora/lido/harness/AStETHHarness.sol \
    certora/lido/harness/SymbolicLendingPool.sol \
    certora/lido/harness/DummyERC20A.sol \
    certora/lido/harness/DummyERC20B.sol \
    --verify AStETHHarness:certora/lido/specs/AStETH.spec \
    --link AStETHHarness:POOL=SymbolicLendingPool AStETHHarness:UNDERLYING_ASSET_ADDRESS=DummyERC20A AStETHHarness:RESERVE_TREASURY_ADDRESS=DummyERC20B \
    --solc solc6.12 \
    --optimistic_loop \
    --staging  \
    --msg "AStETH rule sanity" \
    --rule integrityOfMint




certoraRun certora/lido/harness/AStETHHarness.sol certora/lido/harness/SymbolicLendingPool.sol certora/lido/harness/DummyERC20A.sol certora/lido/harness/DummyERC20B.sol --verify AStETHHarness:certora/lido/specs/AStETH.spec --link AStETHHarness:POOL=SymbolicLendingPool AStETHHarness:UNDERLYING_ASSET_ADDRESS=DummyERC20A AStETHHarness:RESERVE_TREASURY_ADDRESS=DummyERC20B --solc solc6.12 --optimistic_loop --staging --msg "AStETH rule sanity" --rule integrityOfMint




certoraRun contracts/protocol/tokenization/lido/AStETH.sol \
    certora/lido/harness/SymbolicLendingPool.sol \
    certora/lido/harness/DummyERC20A.sol \
    certora/lido/harness/DummyERC20B.sol \
    --verify AStETH:certora/lido/specs/AStETH.spec \
    --link AStETH:POOL=SymbolicLendingPool AStETH:UNDERLYING_ASSET_ADDRESS=DummyERC20A AStETH:RESERVE_TREASURY_ADDRESS=DummyERC20B \
    --solc solc6.12 \
    --optimistic_loop \
    --staging  \
    --msg "AStETH rule sanity" \
    --rule integrityOfMint


certoraRun contracts/protocol/tokenization/lido/AStETH.sol certora/lido/harness/SymbolicLendingPool.sol certora/lido/harness/DummyERC20A.sol certora/lido/harness/DummyERC20B.sol --verify AStETH:certora/lido/specs/AStETH.spec --link AStETH:POOL=SymbolicLendingPool AStETH:UNDERLYING_ASSET_ADDRESS=DummyERC20A AStETH:RESERVE_TREASURY_ADDRESS=DummyERC20B --solc solc6.12 --optimistic_loop --staging  --msg "AStETH rule sanity" --rule integrityOfMint


# RUN THIS
certoraRun certora/lido/harness/AStETHHarness.sol certora/lido/harness/IncentivesControllerMock.sol certora/lido/harness/SymbolicLendingPool.sol certora/lido/harness/DummyERC20A.sol certora/lido/harness/DummyERC20B.sol --verify AStETHHarness:certora/lido/specs/AStETH.spec --link AStETHHarness:POOL=SymbolicLendingPool AStETHHarness:UNDERLYING_ASSET_ADDRESS=DummyERC20A AStETHHarness:RESERVE_TREASURY_ADDRESS=DummyERC20B --solc solc6.12 --optimistic_loop --staging  --msg "AStETH rule sanity" --rule integrityOfMint
