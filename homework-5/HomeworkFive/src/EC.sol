// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

contract EC {
    struct ECPoint {
        uint256 x;
        uint256 y;
    }

    function ecAdd(ECPoint memory A, ECPoint memory B) internal view returns (ECPoint memory) {
      (bool ok, bytes memory data) = address(0x06).staticcall(abi.encode(A.x, A.y, B.x, B.y));
      require(ok, "Failed to call ec_add precompile");
      return abi.decode(data, (ECPoint));
    }

    function ecMul(ECPoint memory point, uint256 scalar) internal view returns (ECPoint memory) {
      (bool ok, bytes memory data) = address(0x07).staticcall(abi.encode(point.x, point.y, scalar));
      require(ok, "Failed to call ec_mul precompile");
      return abi.decode(data, (ECPoint));
    }
}