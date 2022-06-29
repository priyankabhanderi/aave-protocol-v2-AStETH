import "./AStETH_summerizations.spec"

using SymbolicLendingPool as LENDING_POOL
using DummyERC20A as UNDERLYING_ASSET
using DummyERC20B as RESERVE_TREASURY

methods {    

    getRevision() returns (uint256)
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

    isContractIsTrue(address) returns (bool) envfree

    UNDERLYING_ASSET.balanceOf(address) returns (uint256) envfree
    UNDERLYING_ASSET.totalSupply() returns (uint256) envfree

    LENDING_POOL.aToken() returns (address) envfree

}

rule balanceChangeIntegrity()
{
    address user1;
     address user2;
      method f;

	env e;
	require user1!=user2;
	uint256 beforeBalanceA = balanceOf(user1);
	uint256 beforeBalanceB = balanceOf(user2);
	 
	calldataarg arg;
	f(e, arg); 
	uint256 afterBalanceA = balanceOf(user1);
	uint256 afterBalanceB = balanceOf(user2);
	
	assert (beforeBalanceA == afterBalanceA || beforeBalanceB == afterBalanceB || 
        (beforeBalanceA != afterBalanceA && 
        beforeBalanceB != afterBalanceB && 
        beforeBalanceA+beforeBalanceB == afterBalanceA+afterBalanceB)
    );
}

rule MintIntegrity(address user, uint256 amount, uint256 index) {
	env e;
    mathint earlyTotalSupply = totalSupply();
    mathint earlyBalance = balanceOf(user);
    mint(e, user, amount, index);
    mathint totalSupplyAfter = totalSupply();
    mathint balanceAfter = balanceOf(user);
    assert e.msg.sender == LENDING_POOL;
    assert amount != 0 => earlyTotalSupply < totalSupplyAfter;
    assert amount != 0 => earlyBalance < balanceAfter;
}

rule mintAdditive(address user, uint256 amount1, uint256 amount2, uint256 index) {
    env e;
	storage initialStorage = lastStorage;
	mint(e, user, amount1, index);
	mint(e, user, amount2, index);
	mathint balance1 = balanceOf(user);
    mathint totalSupply1 = totalSupply();
	uint256 amount = amount1 + amount2;
	mint(e, user, amount, index) at initialStorage;
	mathint balance2 = balanceOf(user);
    mathint totalSupply2 = totalSupply();
	assert balance1 == balance2, "mint is not additive";
    assert totalSupply1 == totalSupply2;
}

rule burnAdditive(address user, address receiverOfUnderlying, uint256 amount1,  uint256 amount2, uint256 index) {
	env e;
	storage initialState = lastStorage;
	burn(e, user, receiverOfUnderlying, amount1, index);
	burn(e, user, receiverOfUnderlying, amount2, index);
	uint256 balance1 = balanceOf(user);
    mathint totalSupply1 = totalSupply();
	uint256 amount = amount1 + amount2;
	burn(e, user, receiverOfUnderlying, amount, index) at initialState;
	uint256 balance2 = balanceOf(user);
    mathint totalSupply2 = totalSupply();
	assert balance1 == balance2;
    assert totalSupply1 == totalSupply2;
}


/*
    @Rule

    @Description:
        The balance of a reciver in TransferUnderlyingTo() should increase by amount
        The balance of a sender in TransferUnderlyingTo() should decrease by amount

    @Formula:
        {
            user != currentContract;
        }

        transferUnderlyingTo(user, amount)
        
        {
            userBalanceAfter == userBalanceBefore + amountTransfered;
            totalSupplyAfter == totalSupplyBefore - amountTransfered;
        }

    @Note:

    @Link:
*/

/*
rule integrityOfTransferUnderlyingTo(address user, uint256 amount) {
    env e;
    require user != currentContract;

    mathint totalSupplyBefore = UNDERLYING_ASSET.balanceOf(currentContract);
    mathint userBalanceBefore = UNDERLYING_ASSET.balanceOf(user);

    uint256 amountTransfered = transferUnderlyingTo(e, user, amount);

    mathint totalSupplyAfter = UNDERLYING_ASSET.balanceOf(currentContract);
    mathint userBalanceAfter = UNDERLYING_ASSET.balanceOf(user);

    assert userBalanceAfter == userBalanceBefore + amountTransfered;
    assert totalSupplyAfter == totalSupplyBefore - amountTransfered;
}
*/

/*
    @Rule

    @Description:
        Minting AStETH must increase the AStETH totalSupply and user's balance

    @Formula:
        {

        }

        mint()
        
        {
            _ATokenInternalBalance < ATokenInternalBalance_ &&
            _ATokenScaledBalance < ATokenScaledBalance_ &&
            _ATokenBalance < ATokenBalance_ &&
            _ATokenInternalTotalSupply < ATokenInternalTotalSupply_ &&
            _ATokenScaledTotalSupply < ATokenScaledTotalSupply_ &&
            _ATokenTotalSupply < ATokenTotalSupply_
        }

    @Note:

    @Link:
*/

/*
rule monotonicityOfMint(address user, uint256 amount, uint256 index) {
	env e;

    mathint _ATokenInternalBalance = internalBalanceOf(user);
    mathint _ATokenScaledBalance = scaledBalanceOf(user);
    mathint _ATokenBalance = balanceOf(user);
    mathint _ATokenInternalTotalSupply = internalTotalSupply();
    mathint _ATokenScaledTotalSupply = scaledTotalSupply();
    mathint _ATokenTotalSupply = totalSupply();
    
    mint(e, user, amount, index);
    
    mathint ATokenInternalBalance_ = internalBalanceOf(user);
    mathint ATokenScaledBalance_ = scaledBalanceOf(user);
    mathint ATokenBalance_ = balanceOf(user);
    mathint ATokenInternalTotalSupply_ = internalTotalSupply();
    mathint ATokenScaledTotalSupply_ = scaledTotalSupply();
    mathint ATokenTotalSupply_ = totalSupply();
    
    assert _ATokenInternalBalance < ATokenInternalBalance_;
    assert _ATokenScaledBalance < ATokenScaledBalance_;
    assert _ATokenBalance < ATokenBalance_;
    assert _ATokenInternalTotalSupply < ATokenInternalTotalSupply_;
    assert _ATokenScaledTotalSupply < ATokenScaledTotalSupply_;
    assert _ATokenTotalSupply < ATokenTotalSupply_;
}
*/

/*
    @Rule

    @Description:
        Burning AStETH must decrease the AStETH totalSupply and user's balance.
        It should also not decrease reciver's underlying asset.

    @Formula:
        {

        }

        burn()
        
        {
            _ATokenInternalBalance > ATokenInternalBalance_ &&
            _ATokenScaledBalance > ATokenScaledBalance_ &&
            _ATokenBalance > ATokenBalance_ &&
            _ATokenInternalTotalSupply > ATokenInternalTotalSupply_ &&
            _ATokenScaledTotalSupply > ATokenScaledTotalSupply_ &&
            _ATokenTotalSupply > ATokenTotalSupply_ &&
            _underlyingReciverBalance <= underlyingReciverBalance_ &&
            _underlyingTotalSupply == underlyingTotalSupply_
        }

    @Note:

    @Link:
*/

/*

rule monotonicityOfBurn(address user, address reciver, uint256 amount, uint256 index) {
	env e;

    mathint _ATokenInternalBalance = internalBalanceOf(user);
    mathint _ATokenScaledBalance = scaledBalanceOf(user);
    mathint _ATokenBalance = balanceOf(user);
    mathint _ATokenInternalTotalSupply = internalTotalSupply();
    mathint _ATokenScaledTotalSupply = scaledTotalSupply();
    mathint _ATokenTotalSupply = totalSupply();
    mathint _underlyingReciverBalance = UNDERLYING_ASSET.balanceOf(reciver);
    
    burn(e, user, reciver, amount, index);
    
    mathint ATokenInternalBalance_ = internalBalanceOf(user);
    mathint ATokenScaledBalance_ = scaledBalanceOf(user);
    mathint ATokenBalance_ = balanceOf(user);
    mathint ATokenInternalTotalSupply_ = internalTotalSupply();
    mathint ATokenScaledTotalSupply_ = scaledTotalSupply();
    mathint ATokenTotalSupply_ = totalSupply();
    mathint underlyingReciverBalance_ = UNDERLYING_ASSET.balanceOf(reciver);
    
    
    assert _ATokenInternalBalance > ATokenInternalBalance_;
    assert _ATokenScaledBalance > ATokenScaledBalance_;
    assert _ATokenBalance > ATokenBalance_;
    assert _ATokenInternalTotalSupply > ATokenInternalTotalSupply_;
    assert _ATokenScaledTotalSupply > ATokenScaledTotalSupply_;
    assert _ATokenTotalSupply > ATokenTotalSupply_;
    
    assert _underlyingReciverBalance <= underlyingReciverBalance_;
}
*/

/*
    @Rule

    @Description:
        Minting and burning are invert operations within the AStETH context

    @Formula:
        {

        }

        mint()
        burn()
        
        {
            _ATokenInternalBalance == ATokenInternalBalance_ &&
            _ATokenScaledBalance == ATokenScaledBalance_ &&
            _ATokenBalance == ATokenBalance_ &&
            _ATokenInternalTotalSupply == ATokenInternalTotalSupply_ &&
            _ATokenScaledTotalSupply == ATokenScaledTotalSupply_ &&
            _ATokenTotalSupply == ATokenTotalSupply_
        }

    @Note:

    @Link:
*/

/*
rule mintBurnInvertability(address user, uint256 amount, uint256 index, address reciver){
    env e;
    
    mathint _ATokenInternalBalance = internalBalanceOf(user);
    mathint _ATokenScaledBalance = scaledBalanceOf(user);
    mathint _ATokenBalance = balanceOf(user);
    mathint _ATokenInternalTotalSupply = internalTotalSupply();
    mathint _ATokenScaledTotalSupply = scaledTotalSupply();
    mathint _ATokenTotalSupply = totalSupply();
    
    mint(e, user, amount, index);
    burn(e, user, reciver, amount, index);
    
    mathint ATokenInternalBalance_ = internalBalanceOf(user);
    mathint ATokenScaledBalance_ = scaledBalanceOf(user);
    mathint ATokenBalance_ = balanceOf(user);
    mathint ATokenInternalTotalSupply_ = internalTotalSupply();
    mathint ATokenScaledTotalSupply_ = scaledTotalSupply();
    mathint ATokenTotalSupply_ = totalSupply();
    
    assert _ATokenInternalBalance == ATokenInternalBalance_;
    assert _ATokenScaledBalance == ATokenScaledBalance_;
    assert _ATokenBalance == ATokenBalance_;
    assert _ATokenInternalTotalSupply == ATokenInternalTotalSupply_;
    assert _ATokenScaledTotalSupply == ATokenScaledTotalSupply_;
    assert _ATokenTotalSupply == ATokenTotalSupply_;
}
*/

/*
    @Rule

    @Description:
        AStETH cannot change the totalSupply of the underlying asset

    @Formula:
        {

        }

        < call any function >
        
        {
            _underlyingTotalSupply == underlyingTotalSupply_
        }

    @Note:

    @Link:
*/

/*
rule aTokenCantAffectUnderlying(){
    env e; calldataarg args; method f;

    mathint _underlyingTotalSupply = UNDERLYING_ASSET.totalSupply();
    f(e, args);
    mathint underlyingTotalSupply_ = UNDERLYING_ASSET.totalSupply();

    assert _underlyingTotalSupply == underlyingTotalSupply_;
}
*/

/*
    @Rule

    @Description:
        Check that each possible operation changes the balance of at most two users

    @Formula:
        {

        }

        < call any function >
        
        {
            _ATokenInternalBalance1 == ATokenInternalBalance1_ || _ATokenInternalBalance2 == ATokenInternalBalance2_ || _ATokenInternalBalance3 == ATokenInternalBalance3_
            _ATokenScaledBalance1 == ATokenScaledBalance1_ || _ATokenScaledBalance2 == ATokenScaledBalance2_ || _ATokenScaledBalance3 == ATokenScaledBalance3_
            _ATokenBalance1 == ATokenBalance1_ || _ATokenBalance2 == ATokenBalance2_ || _ATokenBalance3 == ATokenBalance3_
        }

    @Note:

    @Link:
*/

/*
rule operationAffectMaxTwo(address user1, address user2, address user3)
{
	env e; calldataarg arg; method f;
	require user1!=user2 && user1!=user3 && user2!=user3;
    mathint _ATokenInternalBalance1 = internalBalanceOf(user1);
    mathint _ATokenInternalBalance2 = internalBalanceOf(user2);
    mathint _ATokenInternalBalance3 = internalBalanceOf(user3);
    mathint _ATokenScaledBalance1 = scaledBalanceOf(user1);
    mathint _ATokenScaledBalance2 = scaledBalanceOf(user2);
    mathint _ATokenScaledBalance3 = scaledBalanceOf(user3);
    mathint _ATokenBalance1 = balanceOf(user1);
    mathint _ATokenBalance2 = balanceOf(user2);
    mathint _ATokenBalance3 = balanceOf(user3);
	
    f(e, arg);

    mathint ATokenInternalBalance1_ = internalBalanceOf(user1);
    mathint ATokenInternalBalance2_ = internalBalanceOf(user2);
    mathint ATokenInternalBalance3_ = internalBalanceOf(user3);
    mathint ATokenScaledBalance1_ = scaledBalanceOf(user1);
    mathint ATokenScaledBalance2_ = scaledBalanceOf(user2);
    mathint ATokenScaledBalance3_ = scaledBalanceOf(user3);
    mathint ATokenBalance1_ = balanceOf(user1);
    mathint ATokenBalance2_ = balanceOf(user2);
    mathint ATokenBalance3_ = balanceOf(user3);

	assert (_ATokenInternalBalance1 == ATokenInternalBalance1_ || _ATokenInternalBalance2 == ATokenInternalBalance2_ || _ATokenInternalBalance3 == ATokenInternalBalance3_);
	assert (_ATokenScaledBalance1 == ATokenScaledBalance1_ || _ATokenScaledBalance2 == ATokenScaledBalance2_ || _ATokenScaledBalance3 == ATokenScaledBalance3_);
	assert (_ATokenBalance1 == ATokenBalance1_ || _ATokenBalance2 == ATokenBalance2_ || _ATokenBalance3 == ATokenBalance3_);

}

/*
    @Rule

    @Description:
        Check that the changes to total supply are coherent with the changes to balance

    @Formula:
        {

        }

        < call any function >
        
        {
            ((ATokenInternalBalance1_ != _ATokenInternalBalance1) && (ATokenInternalBalance2_ != _ATokenInternalBalance2)) =>
            (ATokenInternalBalance1_ - _ATokenInternalBalance1) + (ATokenInternalBalance2_ - _ATokenInternalBalance2)  == (ATokenInternalTotalSupply_ - _ATokenInternalTotalSupply);
            
            ((ATokenScaledBalance1_ != _ATokenScaledBalance1) && (ATokenScaledBalance2_ != _ATokenScaledBalance2)) =>
            (ATokenScaledBalance1_ - _ATokenScaledBalance1) + (ATokenScaledBalance2_ - _ATokenScaledBalance2)  == (ATokenScaledTotalSupply_ - _ATokenScaledTotalSupply);
            
            ((ATokenBalance1_ != _ATokenBalance1) && (ATokenBalance2_ != _ATokenBalance2)) =>
            (ATokenBalance1_ - _ATokenBalance1) + (ATokenBalance2_ - _ATokenBalance2)  == (ATokenTotalSupply_ - ATokenTotalSupply_);
        }

    @Note:

    @Link:
*/

/*
invariant atokenPeggedToUnderlying(env e)
    UNDERLYING_ASSET.balanceOf(currentContract) >= totalSupply()
    filtered { f -> f.selector != mint(address ,uint256 ,uint256).selector &&
                    f.selector != mintToTreasury(uint256, uint256).selector }
    {
        preserved with (env e2) {
            require currentContract != LENDING_POOL;
        }
    }
*/

/*
    @Rule

    @Description:
        Checks that the totalSupply of AStETH must be backed by underlying asset in the contract when deposit is called (and hence mint)
        Checks that the totalSupply of AStETH must be backed by underlying asset in the contract when withdraw is called (and hence burn)

    @Formula:
        {
            _underlyingBalance >= _aTokenTotalSupply
        }

        LENDING_POOL.deposit(UNDERLYING_ASSET, amount, user, referralCode);
                                    OR
        LENDING_POOL.withdraw(e, UNDERLYING_ASSET, amount, user);

        {
            msg.sender != currentContract => underlyingBalance_ >= aTokenTotalSupply_
        }

    @Note:

    @Link:
    
*/

rule atokenPeggedToUnderlying(env e, uint256 amount, address user, uint16 referralCode){
    uint8 case;
    mathint _underlyingBalance = UNDERLYING_ASSET.balanceOf(currentContract);
    mathint _aTokenTotalSupply = totalSupply();

    require _underlyingBalance >= _aTokenTotalSupply;
    require LENDING_POOL.aToken() == currentContract;
    
    if (case == 0){
        LENDING_POOL.deposit(e, UNDERLYING_ASSET, amount, user, referralCode);
    }
    else if (case == 1){
        LENDING_POOL.withdraw(e, UNDERLYING_ASSET, amount, user);
    }
    // else if (case == 2){
    //     LENDING_POOL.borrow(e, UNDERLYING_ASSET, amount, user);
    // }
    // else if (case == 3){
    //     LENDING_POOL.flashLoan(e, UNDERLYING_ASSET, amount, user);
    // }
    
    mathint underlyingBalance_ = UNDERLYING_ASSET.balanceOf(currentContract);
    mathint aTokenTotalSupply_ = totalSupply();

    // Here the LHS of the implication is vital since a case where AStETH calls deposit will cause the backing token to be unchanged while Atokens will be minted.
    // This LHS demand is fine since AStETH cannot actively call deposit from lending pool, nor there is an `execute` method that allows calling methods externally from other contracts.
    assert e.msg.sender != currentContract => underlyingBalance_ >= aTokenTotalSupply_;
}

/*
    @Rule

    @Description:ֿ
        The AStETH totalSupply, tracked by the contract, is the sum of AStETH balances across all users.

    @Formula:
        totalsGhost() == internalTotalSupply()

    @Note:

    @Link:
    
*/

invariant totalSupplyIsSumOfBalances()
    totalsGhost() == internalTotalSupply()

/*
    @Rule

    @Description:ֿ
        The AStETH balance of a single user is less or equal to the total supply

    @Formula:
        totalsGhost() >= internalBalanceOf(user)

    @Note: 
        For every function that implements a transfer between 2 users within the system, we required that the sum of balances of the 2 users start as less than the totalSupply.
        

    @Link:
    
*/

invariant totalSupplyGESingleUserBalance(address user, env e)
    totalsGhost() >= internalBalanceOf(user)
    {
        preserved transferFrom(address spender, address reciever, uint256 amount) with (env e2) {
            require internalBalanceOf(user) + internalBalanceOf(spender) <= totalsGhost();
        }
        preserved transfer(address reciever, uint256 amount) with (env e3) {
            require e3.msg.sender == e.msg.sender;
            require internalBalanceOf(user) + internalBalanceOf(e3.msg.sender) <= totalsGhost();
        }
        preserved transferOnLiquidation(address from, address to, uint256 amount) with (env e4) {
            require internalBalanceOf(user) + internalBalanceOf(from) <= totalsGhost(); 
        }
        preserved burn(address owner, address recieverUnderlying, uint256 amount, uint256 index)  with (env e5) {
            require internalBalanceOf(user) + internalBalanceOf(owner) <= totalsGhost(); 
        }
    }


/*****************************
 *         UNFINISHED        *
 *****************************/

/*
    @Rule

    @Description:
        Verify conditions in which burn should revert

    @Formula:
        {
            user != 0 &&
		    e.msg.value == 0 &&
		    e.msg.sender == LENDING_POOL && LENDING_POOL != 0 &&
		    totalSupply() >= amount &&
		    to != 0 && 
		    (UNDERLYING_ASSET.balanceOf(currentContract) > amount  ) &&
		    UNDERLYING_ASSET.balanceOf(to) + amount < max_uint &&
		    balanceOf(user) < amount
        }

        burn@withrevert(e, user, to, amount, index)
        
        {
            !lastReverted
        }

    @Note:

    @Link:
*/

/* 
rule nonrevertOfBurn(address user, address to, uint256 amount) {
	env e;
	uint256 index;
    uint256 totalSupply = totalSupply();
    uint256 underlyingAStETHBalance = UNDERLYING_ASSET.balanceOf(currentContract);
    uint256 underlyingReciverBalance = UNDERLYING_ASSET.balanceOf(to);
    uint256 AStETHBalance = balanceOf(currentContract);
    uint256 reciverBalance = balanceOf(to);
    uint256 senderBalance = balanceOf(user);
    bool isContract = isContractIsTrue(UNDERLYING_ASSET);
	require (
		user != 0 && //user is not zero
		e.msg.value == 0 && //sends assets
		e.msg.sender == LENDING_POOL && LENDING_POOL != 0 && //sender is Lending pool
        amount != 0 && //amount is non-zero (for line 109 in AStETH.sol )
		totalSupply >= amount && //enough total supply is system (for line 214 in IncentivizedERC20.sol )
		to != 0 && //valid reciever
		(underlyingAStETHBalance >= amount)  && //enough balance in the underlying asset
		(AStETHBalance >= amount)  && //enough balance in the underlying asset
		underlyingReciverBalance + amount <= max_uint && //balance of reviever will not overflow, why not <
		reciverBalance + amount <= max_uint && //balance of reviever will not overflow, why not <
		senderBalance >= amount && //user have enough balance (for line 217 in IncentivizedERC20.sol )
        isContract //underlying asset is a contract
	 );
	burn@withrevert(e, user, to, amount, index);
	assert !lastReverted; 
}