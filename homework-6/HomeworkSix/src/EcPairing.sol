// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

contract EcPairing {
  struct G1Point {
    uint256 x;
    uint256 y;
  }

  struct G2Point {
    uint256[2] x;
    uint256[2] y;
  }

  uint256 internal constant P = 21888242871839275222246405745257275088548364400416034343698204186575808495617;

  G1Point internal G1 = G1Point(1, 2);

  // 5G1
  G1Point internal ALPHA = G1Point(10744596414106452074759370245733544594153395043370666422502510773307029471145, 848677436511517736191562425154572367705380862894644942948681172815252343932);

  // 6G2
  G2Point internal BETA = G2Point(
    [
      12345624066896925082600651626583520268054356403303305150512393106955803260718,
      10191129150170504690859455063377241352678147020731325090942140630855943625622
    ],
    [
      13790151551682513054696583104432356791070435696840691503641536676885931241944,
      16727484375212017249697795760885267597317766655549468217180521378213906474374
    ]
  );

  // 7G2
  G2Point internal GAMMA = G2Point(
    [
      18551411094430470096460536606940536822990217226529861227533666875800903099477,
      15512671280233143720612069991584289591749188907863576513414377951116606878472
    ],
    [
      1711576522631428957817575436337311654689480489843856945284031697403898093784,
      13376798835316611669264291046140500151806347092962367781523498857425536295743
    ]
  );

  // 9G2
  G2Point internal DELTA = G2Point(
    [
      4821341333500639427117806840255663771228880693152568023710381392280915109763,
      13193736976255674115506271204866518055492249136949196233486205080643750676277
    ],
    [
      5830427496645529367349790160167113194176899755997018131088404969293864912751,
      18281872490245496509379794148214936771631698359916681711594256455596877716636
    ]
  );

  error EcMulFailed();
  error EcPairingFailed();

  function verify(
    G1Point calldata A1,
    G2Point calldata B2,
    G1Point calldata C1,
    uint256 x1,
    uint256 x2,
    uint256 x3
  ) external view returns (bool) {
    G1Point memory X1 = ecMul(G1, (x1 + x2 + x3) % P);

    (bool success, bytes memory data) = address(0x08).staticcall(
      abi.encode(
        A1.x,
        A1.y,
        B2.x[0],
        B2.x[1],
        B2.y[0],
        B2.y[1],

        ALPHA.x,
        ALPHA.y,
        BETA.x[0],
        BETA.x[1],
        BETA.y[0],
        BETA.y[1],

        X1.x,
        X1.y,
        GAMMA.x[0],
        GAMMA.x[1],
        GAMMA.y[0],
        GAMMA.y[1],

        C1.x,
        C1.y,
        DELTA.x[0],
        DELTA.x[1],
        DELTA.y[0],
        DELTA.y[1]
      )
    );

    if (!success) revert EcPairingFailed();

    return abi.decode(data, (bool));
  }

  function ecMul(G1Point memory point, uint256 s) internal view returns (G1Point memory) {
    (bool success, bytes memory data) = address(0x07).staticcall(abi.encode(point.x, point.y, s));
    if (!success) revert EcMulFailed();
    return abi.decode(data, (G1Point));
  }
}
