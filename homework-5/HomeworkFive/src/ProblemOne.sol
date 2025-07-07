// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {EC} from "./EC.sol";
import {console} from "forge-std/console.sol";

contract ProblemOne is EC {
    uint256 public constant CURVE_P = 21888242871839275222246405745257275088548364400416034343698204186575808495617;

    error ZeroDenominator();
    error OutOfBounds();

    function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool verified) {
        if (den == 0) {
            revert ZeroDenominator();
        }

        if (num > CURVE_P || den > CURVE_P) {
            revert OutOfBounds();
        }

        ECPoint memory proof = ecAdd(A, B);

        uint256 s = mulmod(num, modInv(den, CURVE_P), CURVE_P);
        ECPoint memory G = ECPoint({x: 1, y: 2});
        ECPoint memory expectedProof = ecMul(G, s);

        return proof.x == expectedProof.x && proof.y == expectedProof.y;
    }

    function modInv(uint256 a, uint256 mod) internal view returns (uint256) {
        return modExp(a, mod - 2, mod);
    }

    function modExp(uint256 base, uint256 exp, uint256 mod) internal view returns (uint256) {
        bytes memory precompileData = abi.encode(32, 32, 32, base, exp, mod);
        (bool ok, bytes memory data) = address(0x05).staticcall(precompileData);
        require(ok, "modExp failed");
        return abi.decode(data, (uint256));
    }
}
