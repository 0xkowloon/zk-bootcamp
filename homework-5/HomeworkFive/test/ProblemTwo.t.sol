// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Test} from "forge-std/Test.sol";
import {EC} from "../src/EC.sol";
import {ProblemTwo} from "../src/ProblemTwo.sol";

contract ProblemTwoTest is Test {
    ProblemTwo public problemTwo;

    function setUp() public {
        problemTwo = new ProblemTwo();
    }

    function test_matmul() public view {
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        uint256 n = 3;

        uint256[] memory matrix = new uint256[](9);
        matrix[0] = 1; matrix[1] = 2; matrix[2] = 3;
        matrix[3] = 4; matrix[4] = 5; matrix[5] = 6;
        matrix[6] = 7; matrix[7] = 8; matrix[8] = 9;

        EC.ECPoint[] memory s = new EC.ECPoint[](3);
        s[0] = G;
        s[1] = ecMul(G, 2);
        s[2] = ecMul(G, 3);

        uint256[] memory o = new uint256[](n);
        o[0] = 14; // 1*P + 2*Q + 3*R = 1*(1*G) + 2*(2*G) + 3*(3*G) = 1*G + 4*G + 9*G = 14*G
        o[1] = 32; // 4*P + 5*Q + 6*R = 4*(1*G) + 5*(2*G) + 6*(3*G) = 4*G + 10*G + 18*G = 32*G
        o[2] = 50; // 7*P + 8*Q + 9*R = 7*(1*G) + 8*(2*G) + 9*(3*G) = 7*G + 16*G + 27*G = 50*G

        assertTrue(problemTwo.matmul(matrix, n, s, o));

        o[0] += 1;

        assertFalse(problemTwo.matmul(matrix, n, s, o));
    }

    function test_matmul_RevertIf_InvalidVectorDimensions() public {
        uint256 n = 3;
        uint256[] memory matrix = new uint256[](9);
        EC.ECPoint[] memory s = new EC.ECPoint[](2); // Wrong length
        uint256[] memory o = new uint256[](3);

        vm.expectRevert(ProblemTwo.InvalidVectorDimensions.selector);
        problemTwo.matmul(matrix, n, s, o);
    }

    function test_matmul_RevertIf_InvalidMatrixDimensions() public {
        uint256 n = 3;
        uint256[] memory matrix = new uint256[](8); // Wrong length
        EC.ECPoint[] memory s = new EC.ECPoint[](3);
        uint256[] memory o = new uint256[](3);

        vm.expectRevert(ProblemTwo.InvalidMatrixDimensions.selector);
        problemTwo.matmul(matrix, n, s, o);
    }

    function test_matmul_RevertIf_InvalidOutputDimensions() public {
        uint256 n = 3;
        uint256[] memory matrix = new uint256[](9);
        EC.ECPoint[] memory s = new EC.ECPoint[](3);
        uint256[] memory o = new uint256[](2); // Wrong length

        vm.expectRevert(ProblemTwo.InvalidOutputDimensions.selector);
        problemTwo.matmul(matrix, n, s, o);
    }

    function test_matmul_RevertIf_ZeroN() public {
        EC.ECPoint memory G = EC.ECPoint({x: 1, y: 2});
        uint256 n = 3;

        uint256[] memory matrix = new uint256[](9);
        matrix[0] = 1; matrix[1] = 2; matrix[2] = 3;
        matrix[3] = 4; matrix[4] = 5; matrix[5] = 6;
        matrix[6] = 7; matrix[7] = 8; matrix[8] = 9;

        EC.ECPoint[] memory s = new EC.ECPoint[](3);
        s[0] = G;
        s[1] = ecMul(G, 2);
        s[2] = ecMul(G, 3);

        uint256[] memory o = new uint256[](n);
        o[0] = 14;
        o[1] = 32;
        o[2] = 50;

        vm.expectRevert(ProblemTwo.ZeroN.selector);
        problemTwo.matmul(matrix, 0, s, o);
    }

    function ecMul(EC.ECPoint memory point, uint256 scalar) internal view returns (EC.ECPoint memory) {
      (bool ok, bytes memory data) = address(0x07).staticcall(abi.encode(point.x, point.y, scalar));
      require(ok, "Failed to call ec_mul precompile");
      return abi.decode(data, (EC.ECPoint));
    }
}
