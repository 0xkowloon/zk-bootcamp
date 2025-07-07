// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {console} from "forge-std/console.sol";
import {EC} from "./EC.sol";

contract ProblemTwo is EC {
    error InvalidMatrixDimensions();
    error InvalidVectorDimensions();
    error InvalidOutputDimensions();
    error ZeroN();

    function matmul(uint256[] calldata matrix, uint256 n, ECPoint[] calldata s, uint256[] calldata o) public view returns (bool verified) {
        if (n == 0) {
          revert ZeroN();
        }

        if (s.length != n) {
          revert InvalidVectorDimensions();
        }

        if (matrix.length != n ** 2) {
          revert InvalidMatrixDimensions();
        }

        if (o.length != n) {
          revert InvalidOutputDimensions();
        }

        ECPoint memory G = ECPoint({x: 1, y: 2});

        for (uint256 i = 0; i < n * n; i += n) {
          ECPoint memory sum;

          for (uint256 j = 0; j < n; j++) {
            uint256 scalar = matrix[i + j];
            sum = ecAdd(sum, ecMul(s[j], scalar));
          }

          ECPoint memory oG = ecMul(G, o[i / n]);
          if (sum.x != oG.x || sum.y != oG.y) {
            return false;
          }
        }

        return true;
    }
}