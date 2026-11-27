# A (3,3)-split-critical graph on 45 vertices

This red/blue colouring of $K_{45}$ has no partition into a red side with no red $K_4$ and a blue side with no blue $K_4$. Deleting any one of its 45 vertices gives such a partition. The colouring contains a blue $K_9$. It shows that this partition property can hold at order 45 even in the presence of a monochromatic $K_5$.

The property is necessary for a hypothetical 45-vertex colouring with no monochromatic $K_5$. A split of the whole colouring would let us add a 46th vertex by joining it to each side in that side's colour, contradicting the published upper bound. After deleting any vertex, its original red and blue neighbourhoods give a split. Gyárfás proves the general observation for extremal Ramsey graphs in Proposition 2. [Gyárfás, *Generalized Split Graphs and Ramsey Numbers*](https://www.renyi.hu/~gyarfas/Cikkek/84_gensplitramsey.pdf) · [Angeltveit and McKay, *R(5,5) ≤ 46*](https://doi.org/10.1002/jgt.70029)

## Reproduce the checks

Run these commands from the repository root. The first needs only Python 3. It rebuilds the red adjacency matrix, compares it with the stored graph, searches exhaustively for a split, and checks an explicit partition for every vertex deletion. The second also needs `drat-trim` on PATH, or `--drat-trim /path/to/drat-trim`. [Stored graph](split45.txt) · [Construction checker](check_split45.py) · [DRAT-trim](https://github.com/marijnheule/drat-trim)

```sh
python3 r55-split45/check_split45.py
python3 r55-split45/check_controls.py
```

## Construction

Number the rows and columns from zero. The first three rows have one vertex in each of 12 columns. In row $r$, place labels $0,0,3,6$ in that order in the four columns $4r$ through $4r+3$. Place the nonzero squares modulo 17 in increasing order in the other eight columns. Two vertices in the same row are joined in red exactly when their labels differ by a nonzero square modulo 17.

The last row has nine vertices and all its internal edges are blue. Its first vertex $x$ belongs to all four columns 0 through 3. The other eight vertices occupy columns 4 through 11, one per column. Vertices from different rows are joined in red exactly when they share a column. In the matrix file, the top three rows of the construction are listed in row-major order, followed by $x$ and the other eight vertices.

## Why the colouring is split-critical

The red $K_4$s are exactly the 12 columns. In each of the first three rows, the four vertices labelled $0,0,3,6$ form its unique blue $K_4$. Enumerating four-sets verifies both facts. Two smaller row checks used below are also in the script. Every nine vertices in one row contain a blue triangle, and the eight vertices in columns 4 through 11 of each row contain a blue triangle.

The blue side of a split must meet every red $K_4$. First suppose it omits $x$. Select one representative from each column in the blue side. Representatives in different rows are joined in blue, so their maximum blue clique sizes add over rows. A single row containing all 12 representatives already contains its blue $K_4$. If two rows are used, one must have blue clique size at most one and the other at most two. They can contribute at most $3+8=11$ vertices, by the row checks. Three rows can contribute at most $3+3+3=9$. Four nonempty rows already give a blue $K_4$.

If the blue side contains $x$, take representatives from the eight remaining columns. Each is joined to $x$ in blue, so together they must avoid a blue triangle. Eight in one row contain a blue triangle. Two rows can contribute at most three each, and three nonempty rows give a blue triangle.

Now delete a vertex in column $c$. For $x$, choose $c=0$. Take as the blue side the 11 vertices outside column $c$ in the row whose unique blue $K_4$ contains column $c$. This breaks that blue $K_4$ and meets every still-complete red column. The remaining vertices form the red side. Restricting a split to fewer vertices also gives a split, proving minimality for every proper induced subgraph.

## Comparison colourings

The 92 records represent 87 distinct labelled graph6 strings. Vertex numbers in the table start at zero.

| Input | Records | Certified result |
|---|---:|---|
| 45-vertex search and strongly regular graph controls | 89 | All 89 graphs still have no split after deleting vertex 0. |
| Known 42-vertex (5,5)-graphs | 3 | Each full graph has no split. The original neighbourhoods give valid splits for all 126 vertex deletions. |

Each SAT variable assigns one vertex to the blue side. Every red $K_4$ gives a clause requiring at least one of its vertices on that side. Every blue $K_4$ gives the opposite clause. For a deletion, the checker drops all clauses containing the deleted vertex. It reconstructs each CNF from the graph6 string, checks its SHA-256, and runs DRAT-trim on the archived Glucose4 proof. The 126 positive assignments are checked directly. [Input and result table](controls.tsv) · [92 text proofs in ZIP format](control-proofs.zip) · [Control checker](check_controls.py)

The 45-vertex records comprise 12 near-Ramsey witnesses, 31 search outputs, eight strongly regular graph controls and 38 further comparison colourings. The strongly regular inputs come from descendants of Edward Spence's order-46 conference two-graphs. The three 42-vertex inputs are the first three graphs in the copy of Brendan McKay's list already in this repository. These are sample checks. [Spence's catalogue](https://www.maths.gla.ac.uk/~es/twograph/conf2Graph.php) · [McKay's Ramsey graphs](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html) · [Repository copy](../r55-pair2424/data/r55_42some.g6)

The construction, proof and checks were developed with assistance from OpenAI Codex.
