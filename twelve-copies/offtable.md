# Cells outside the survey tables

Cells that DS1 rev. 18 does not list, where theorem D12 (this folder) or theorem D (`../seven-copies`) applied to a
known (k,s) lower bound gives more than the best value I could derive from published results. That baseline is the
survey tables and items 2.2.g, 2.3.g-i, 6.2.m-o, the google-research ramsey_number_bounds files and recent papers I
found (Yu 2026, Cremer 2026, Coniglio et al. 2026, AlphaEvolve 2026), closed under monotonicity and published recurrences.
It is not a full literature search, and nobody may have looked at these cells before; treat them as consequences of the
theorems, not as records. Only R(8,25) has a graph and a computer check (see README.md); the inputs of the others are known
bounds whose graphs are in the literature.

## Theorem D12, R(k+1, 4s-3) >= 12R(k,s) - 11

| cell | value | input | baseline |
|---|---|---|---|
| R(5,37) | 1093 | D12 R(4,10)>=92 | 1041 (2.3.i R(3,36)>=261) |
| R(5,45) | 1525 | D12 R(4,12)>=128 | 1389 (2.3.i R(3,44)>=348) |
| R(6,33) | 1585 | D12 R(5,9)>=133 | 1549 (2.3.i R(17,5)>=388) |
| R(6,37) | 1777 | D12 R(5,10)>=149 | 1641 (2.3.i R(19,5)>=411) |
| R(6,41) | 2185 | D12 R(5,11)>=183 | 1966 (2.3.g/h R(6,20)>=878 + R(6,22)>=1070 + 18) |
| R(6,45) | 2425 | D12 R(5,12)>=203 | 2182 (2.3.g/h R(6,3)>=18 + R(6,43)>=2160 + 4) |
| R(8,25) | 2449 | D12 R(7,7)>=205 | 2049 (2.3.i R(13,7)>=513) |
| R(8,29) | 2617 | D12 R(7,8)>=219 | 2353 (2.3.i R(15,7)>=589) |
| R(8,33) | 3013 | D12 R(7,9)>=252 | 2913 (2.3.i R(17,7)>=729) |
| R(8,45) | 5029 | D12 R(7,12)>=420 | 5009 (2.3.i R(23,7)>=1253) |
| R(10,33) | 6769 | D12 R(9,9)>=565 | 5641 (h10 (2.3.h on two 2.3.i graphs) R(9,9)>=565) |
| R(10,37) | 6961 | D12 R(9,10)>=581 | 6321 (2.3.i R(19,9)>=1581) |
| R(10,41) | 7393 | D12 R(9,11)>=617 | 7297 (2.3.i R(21,9)>=1825) |
| R(10,45) | 8737 | D12 R(9,12)>=729 | 8161 (2.3.i R(23,9)>=2041) |
| R(11,37) | 9565 | D12 R(10,10)>=798 | 9281 (2.3.i R(19,10)>=2321) |
| R(12,41) | 19153 | D12 R(11,11)>=1597 | 15961 (h10 (2.3.h on two 2.3.i graphs) R(11,11)>=1597) |
| R(12,45) | 19393 | D12 R(11,12)>=1617 | 17105 (2.3.i R(23,11)>=4277) |

## Theorem D, R(k+1, 3s-2) >= 7R(k,s) - 6

| cell | value | input | baseline |
|---|---|---|---|
| R(6,40) | 1863 | D R(5,14)>=267 | 1797 (2.3.g/h R(6,19)>=710 + R(6,22)>=1070 + 17) |
| R(8,31) | 2829 | D R(7,11)>=405 | 2593 (2.3.i R(16,7)>=649) |
| R(8,40) | 3865 | D R(7,14)>=553 | 3694 (2.3.g/h R(8,4)>=59 + R(8,37)>=3629 + 6) |
| R(9,22) | 1968 | D R(8,8)>=282 | 1841 (2.3.g/h R(9,2)>=9 + R(9,21)>=1825 + 7) |
| R(9,37) | 5713 | D R(8,13)>=817 | 4945 (2.3.i R(19,8)>=1237) |
| R(9,40) | 5811 | D R(8,14)>=831 | 5025 (2.3.g/h R(9,4)>=73 + R(9,37)>=4945 + 7) |
| R(10,25) | 3949 | D R(9,9)>=565 | 3489 (2.3.i R(13,9)>=873) |
| R(10,28) | 4061 | D R(9,10)>=581 | 3731 (2.3.g/h R(10,2)>=10 + R(10,27)>=3713 + 8) |
| R(10,43) | 7869 | D R(9,15)>=1125 | 7361 (2.3.i R(22,9)>=1841) |
| R(11,28) | 5580 | D R(10,10)>=798 | 4783 (h6 (2.3.h on 2.3.i graph) R(10,10)>=798) |
| R(11,31) | 5706 | D R(10,11)>=816 | 5321 (2.3.i R(16,10)>=1331) |
| R(12,31) | 11173 | D R(11,11)>=1597 | 9577 (h6 (2.3.h on 2.3.i graph) R(11,11)>=1597) |
| R(12,34) | 11313 | D R(11,12)>=1617 | 9715 (2.3.g/h R(12,4)>=128 + R(12,31)>=9577 + 10) |
