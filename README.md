# Machine Learning — Complete Self-Study Notes

Single-page, self-contained study notes covering **23 machine learning algorithms**
across four units, organised by the kind of supervision signal each one learns from.

**Read them here → https://nrstatlab.github.io/Machine-Learning/**

## What's inside

Every algorithm is presented five times over, in five registers:

| Register | What it gives you |
|---|---|
| **Definition** | What the method is, in one paragraph |
| **Mathematics** | The objective, the update rule, the assumptions — rendered with MathJax |
| **Brief explanation** | The intuition, the hyperparameters that matter, the standard variants |
| **Assumptions & failure modes** | What the method takes for granted, and when it breaks |
| **Worked examples** | Three domains — finance, agriculture, medicine — for every algorithm |
| **Code** | Runnable Python *and* R, in switchable tabs |

## The four units

| Unit | Learns from | Algorithms |
|---|---|---|
| **1 · Supervised** | Labelled data | Naive Bayes · Logistic Regression · KNN · SVM · Decision Tree · Linear Regression · Polynomial Regression · Ridge · Lasso · Random Forest |
| **2 · Unsupervised** | Unlabelled data | K-Means · DBSCAN · Hierarchical Clustering · Apriori · FP-Growth · Isolation Forest |
| **3 · Semi-Supervised** | A few labels plus a large unlabelled pool | Self-Training · Co-Training *(inductive)* · Label Propagation *(transductive)* |
| **4 · Reinforcement** | A reward signal | Q-Learning · REINFORCE *(model-free)* · Dyna-Q · Value Iteration *(model-based)* |

## Running the code

Every Python pane is self-contained and generates its own data — nothing to download.

```bash
pip install numpy pandas scikit-learn mlxtend
```

All 23 Python panes are verified to run end-to-end against numpy 2.4, pandas 2.x
and scikit-learn 1.9. The R panes require `e1071`, `caret`, `class`, `rpart`,
`randomForest`, `glmnet`, `cluster`, `dbscan`, `arules` and `arulesViz`
depending on the card.

## A note on the example figures

The worked examples describe realistic settings, but the accompanying code
**simulates** its data. Accuracy and AUC figures printed by a pane are properties
of that simulation, not published results. Where an example evokes a real public
dataset — Wisconsin Diagnostic Breast Cancer, Pima Indians Diabetes — the dataset
is named so the figure can be reproduced.

## Repository layout

```
index.html                 the notes (single file, no build step)
ml_self_study_notes.html   redirect stub kept for old links
AUDIT_REPORT.md            conceptual audit: findings and remediation plan
CHANGELOG.md               what changed, and when
```

## Contributing

The notes are one hand-authored HTML file with no build step — edit `index.html`
directly. Two things to keep consistent when you do:

- **Every card carries all five registers.** A new algorithm needs a definition,
  mathematics, an explanation, an assumptions/failure-modes chip row, three
  domain examples, and both language tabs.
- **Escape code panes.** `<` and `&` inside `<pre><code>` must be written as
  `&lt;` and `&amp;`, or R's `<-` will break strict parsers.

CI validates the HTML and checks internal anchors on every push.

## Licence

Not yet chosen — please open an issue if you would like to reuse this material.
