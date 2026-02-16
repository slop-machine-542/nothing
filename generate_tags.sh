#!/bin/bash
# Generate tag pages for Math Digest

TAGS_DIR="/root/.openclaw/workspace/nothing/tags"
POSTS_DIR="/root/.openclaw/workspace/nothing/posts"

# List of all tags from the index page
TAGS=(
  "algebra" "algebraic-geometry" "algebraic-topology" "analysis" "arithmetic-geometry"
  "bayesian-statistics" "category-theory" "cellular-automata" "chaos-theory" "coding-theory"
  "combinatorics" "commutative-algebra" "complex-analysis" "control-theory" "convex-optimization"
  "cryptography" "differential-equations" "dynamical-systems" "eigenvalues" "elliptic-curves"
  "ergodic-theory" "field-theory" "financial-math" "fixed-point" "fluid-dynamics"
  "fractals" "functional-analysis" "galois-theory" "game-theory" "geometric-group-theory"
  "geometry" "graph-theory" "harmonic-analysis" "homotopy-theory" "information-geometry"
  "information-theory" "knot-theory" "lie-groups" "linear-algebra" "logic"
  "machine-learning" "markov-chains" "mathematical-art" "mathematical-biology" "matroid-theory"
  "measure-theory" "modular-forms" "network-science" "non-standard-analysis" "number-theory"
  "numerical-analysis" "operations-research" "operator-algebras" "optimal-transport" "optimization"
  "p-adic-numbers" "partial-differential-equations" "probability-theory" "quantum-computing"
  "ramsey-theory" "random-matrix-theory" "representation-theory" "set-theory" "signal-processing"
  "spectral-graph-theory" "statistical-mechanics" "stochastic-calculus" "stochastic-processes"
  "surreal-numbers" "symplectic-geometry" "topology" "tropical-geometry" "visualization"
)

for tag in "${TAGS[@]}"; do
  cat > "$TAGS_DIR/${tag}.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Math Digest — Posts tagged with ${tag}">
    <meta name="theme-color" content="#2c3e50">
    <title>Math Digest — Tag: ${tag}</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header class="site-header">
        <h1>📐 Math Digest</h1>
        <p class="site-description">A curated collection of mathematical insights</p>
    </header>

    <nav>
        <ul>
            <li><a href="../index.html">Home</a></li>
            <li><a href="../posts/index.html">All Posts</a></li>
            <li><a href="./index.html">Tags</a></li>
            <li><a href="https://github.com/slop-machine-542/nothing">GitHub</a></li>
        </ul>
    </nav>

    <main>
        <h1>🏷️ Tag: ${tag}</h1>
        <p>Posts tagged with "${tag}"</p>
        
        <div id="posts-list">
            <!-- Posts will be listed here -->
            <p><em>Posts with this tag will appear here.</em></p>
        </div>
        
        <p style="margin-top: 2rem;">
            <a href="./index.html" class="tag">← Back to all tags</a>
        </p>
    </main>

    <footer>
        <p><strong>Math Digest</strong> — Powered by curiosity and mathematics</p>
        <p>
            <a href="https://github.com/slop-machine-542/nothing">View on GitHub</a> |
            <a href="../index.html">Home</a> |
            <a href="../posts/index.html">All Posts</a>
        </p>
    </footer>
</body>
</html>
EOF
  echo "Created: ${tag}.html"
done

echo "All tag pages created!"
