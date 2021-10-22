import { expect } from 'chai';
import { makeSuite, TestEnv } from './helpers/make-suite';
import { ProtocolErrors, TokenContractId, eContractid } from '../../helpers/types';
import { getVariableDebtToken } from '../../helpers/contracts-getters';

makeSuite('Variable debt token tests', (testEnv: TestEnv) => {
  const { CT_CALLER_MUST_BE_LENDING_POOL } = ProtocolErrors;

  it('Deb Token initialized', async () => {
    const { deployer, pool, dai, helpersContract, stETH } = testEnv;

    const variableDebtTokenAddress = (
      await helpersContract.getReserveTokensAddresses(stETH.address)
    ).variableDebtTokenAddress;

    const variableDebtContract = await getVariableDebtToken(variableDebtTokenAddress);
  });
});
