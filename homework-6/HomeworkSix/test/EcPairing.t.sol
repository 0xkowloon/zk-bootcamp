// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import {Test, console} from "forge-std/Test.sol";
import {EcPairing} from "../src/EcPairing.sol";

contract EcPairingTest is Test {
    EcPairing public ecPairing;

    function setUp() public {
        ecPairing = new EcPairing();
    }

    function test_verify() public view {
        // -30G1
        EcPairing.G1Point memory A1 = EcPairing.G1Point(
            1527465159374431915328497116935179161014331322368960485951268517950184093102,
            4614198164681446572522695455355058658980462909090786533120711656845158145809
        );

        // 5G2
        EcPairing.G2Point memory B2 = EcPairing.G2Point(
            [
                4540444681147253467785307942530223364530218361853237193970751657229138047649,
                20954117799226682825035885491234530437475518021362091509513177301640194298072
            ],
            [
                11631839690097995216017572651900167465857396346217730511548857041925508482915,
                21508930868448350162258892668132814424284302804699005394342512102884055673846
            ]
        );

        // 4G1
        EcPairing.G1Point memory C1 = EcPairing.G1Point(
            3010198690406615200373504922352659861758983907867017329644089018310584441462,
            4027184618003122424972590350825261965929648733675738730716654005365300998076
        );

        uint256 x1 = 8;
        uint256 x2 = 3;
        uint256 x3 = 1;

        assertTrue(ecPairing.verify(A1, B2, C1, x1, x2, x3));
    }
}
