certoraRun contracts/protocol/tokenization/lido/AStETH.sol:AStETH \
    --verify AStETH:certora/specs/complexity.spec \
    --solc solc6.12 \
    --optimistic_loop \
    --staging  \
    --msg "AStETH complexity check"
