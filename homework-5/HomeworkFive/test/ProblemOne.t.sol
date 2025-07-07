// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Test} from "forge-std/Test.sol";
import {EC} from "../src/EC.sol";
import {ProblemOne} from "../src/ProblemOne.sol";

contract ProblemOneTest is Test {
    ProblemOne public problemOne;

    uint256 public constant CURVE_P = 21888242871839275222246405745257275088548364400416034343698204186575808495617;

    function setUp() public {
        problemOne = new ProblemOne();
    }

    function test_setUpState() public view {
        assertEq(problemOne.CURVE_P(), CURVE_P);
    }

    function test_rationalAdd() public view {
        uint256 num = 3;
        uint256 den = 5;

        uint256 denInv = modInv(den, CURVE_P);
        uint256 a = mulmod(1, denInv, CURVE_P);
        uint256 b = mulmod(2, denInv, CURVE_P);
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        EC.ECPoint memory A = ecMul(G, a);
        EC.ECPoint memory B = ecMul(G, b);
        bool verified = problemOne.rationalAdd(A, B, num, den);
        assertTrue(verified);
    }

    function test_rationalAdd_NotEqual() public view {
        uint256 num = 4;
        uint256 den = 5;

        uint256 denInv = modInv(den, CURVE_P);
        uint256 a = mulmod(1, denInv, CURVE_P);
        uint256 b = mulmod(2, denInv, CURVE_P);
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        EC.ECPoint memory A = ecMul(G, a);
        EC.ECPoint memory B = ecMul(G, b);
        bool verified = problemOne.rationalAdd(A, B, num, den);
        assertFalse(verified);
    }

    function test_rationalAdd_ZeroDenominator() public {
        uint256 num = 3;
        uint256 den = 5;

        uint256 denInv = modInv(den, CURVE_P);
        uint256 a = mulmod(1, denInv, CURVE_P);
        uint256 b = mulmod(2, denInv, CURVE_P);
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        EC.ECPoint memory A = ecMul(G, a);
        EC.ECPoint memory B = ecMul(G, b);

        vm.expectRevert(ProblemOne.ZeroDenominator.selector);
        problemOne.rationalAdd(A, B, num, 0);
    }

    function test_rationalAdd_OutOfBounds_Numerator() public {
        uint256 den = 5;

        uint256 denInv = modInv(den, CURVE_P);
        uint256 a = mulmod(1, denInv, CURVE_P);
        uint256 b = mulmod(2, denInv, CURVE_P);
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        EC.ECPoint memory A = ecMul(G, a);
        EC.ECPoint memory B = ecMul(G, b);

        vm.expectRevert(ProblemOne.OutOfBounds.selector);
        problemOne.rationalAdd(A, B, CURVE_P + 1, den);
    }

    function test_rationalAdd_OutOfBounds_Denominator() public {
        uint256 num = 3;
        uint256 den = 5;

        uint256 denInv = modInv(den, CURVE_P);
        uint256 a = mulmod(1, denInv, CURVE_P);
        uint256 b = mulmod(2, denInv, CURVE_P);
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        EC.ECPoint memory A = ecMul(G, a);
        EC.ECPoint memory B = ecMul(G, b);

        vm.expectRevert(ProblemOne.OutOfBounds.selector);
        problemOne.rationalAdd(A, B, num, CURVE_P + 1);
    }

    function ecMul(EC.ECPoint memory point, uint256 scalar) internal view returns (EC.ECPoint memory) {
        bytes memory precompileData = abi.encode(point.x, point.y, scalar);
        (bool ok, bytes memory data) = address(0x07).staticcall(precompileData);
        require(ok, "Failed to call ec_mul precompile");
        return abi.decode(data, (EC.ECPoint));
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
