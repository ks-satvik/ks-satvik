# Kumar Satvik Chaudhary

MS Computer Science student at Arizona State University and ML/NLP research intern.

I build LLM systems you can check: answers that cite their sources, graders that explain their scores, and agents that catch their own mistakes.

[Google Scholar](https://scholar.google.com/citations?hl=en&user=cb0Qe1sAAAAJ) · [LinkedIn](https://linkedin.com/in/kshchaudhary04) · [Email](mailto:kchaud13@asu.edu)

> 🏆 **Best Demo Paper Award, CIKM 2025** for CyberBOT, an LLM tutor for cybersecurity courses used by 150+ ASU students.

<br>

## Projects

### [Footnote](https://github.com/ks-satvik/footnote)

**Chat with your documents and check every answer.** Each sentence links to the exact passage it came from, and when your files don't have the answer, Footnote says so instead of guessing.

<a href="https://github.com/ks-satvik/footnote"><img src="https://raw.githubusercontent.com/ks-satvik/footnote/main/docs/screenshot.png" alt="Footnote: ask your documents anything, and every answer cites its source" width="100%"></a>

- Hybrid search (BM25 + embeddings, merged with reciprocal rank fusion) beats either one alone on 61 labelled questions: **MRR 0.74** vs 0.71 and 0.64, **Recall@5 86%**
- A cross-encoder gate refuses unanswerable questions before any LLM call (**92% balanced accuracy**), and a verifier checks every citation after the answer is written
- Streams answers over SSE, reads 6 document formats, and ships with 75+ tests, Docker and CI

<sub>Python · FastAPI · React · TypeScript · SQLite · Docker</sub> · [Demo video](https://youtu.be/b_wmAcPnmxA)

### [Tally](https://github.com/ks-satvik/tally-sql-agent)

**Ask a database questions in plain English, safely.** A LangGraph agent writes the SQL, runs it, reads the error if it fails, and repairs its own query.

- Layered guardrails: an sqlglot AST allow-list, read-only connections, an SQLite authorizer and row/time/size budgets block writes, PRAGMA, ATTACH and runaway queries
- BM25 schema linking with foreign-key join expansion sends the model **2.9 of 11 tables** per question while keeping **100%** of the tables it needs (51-question benchmark)
- Bring your own CSV, Excel or SQLite files; generated insights are checked against the actual result rows; 300 tests in CI

<sub>Python · LangGraph · FastAPI · React · TypeScript · SQLite</sub>

### Voot

**Accounts payable on autopilot.** Upload an invoice and it's extracted, validated, checked for duplicates and risk-scored before anyone approves it.

- Async pipeline across 5 Docker services: Azure Blob Storage, Storage Queues, Python workers and Azure Document Intelligence
- 7-stage document lifecycle with role-based access, review workflows, GL account suggestions, audit logging, dashboards and CSV export

<sub>Python · FastAPI · React · TypeScript · PostgreSQL · Azure · Docker</sub>

<br>

## Research

ML & NLP research intern at ASU since January 2025, working on LLMs for education.

**EssayCBM: Rubric-Aligned Concept Bottleneck Models for Transparent Essay Grading**<br>
**K. S. Chaudhary**, C. Zhao, F. Zhang, Y. H. Tse, G. Agrawal, Y. Deng, H. Liu · *ECML-PKDD 2026* · [Paper](https://arxiv.org/abs/2512.20817) · [Demo](https://youtu.be/TnJDOoZbVYE)<br>
<sub>Grades essays through 8 rubric concepts like thesis clarity and use of evidence instead of a black box, so an instructor can change one concept score and watch the grade update. Trained on 24K+ essays.</sub>

**CyberBOT: Towards Reliable Cybersecurity Education via Ontology-Grounded Retrieval Augmented Generation**<br>
C. Zhao, R. De Maria, T. Kumarage, **K. S. Chaudhary**, et al. · *CIKM 2025* · 🏆 Best Demo Paper · [Paper](https://arxiv.org/abs/2504.00389)<br>
<sub>A RAG tutor that checks its answers against a cybersecurity ontology before showing them. Deployed to 150+ students.</sub>

**SMoA: Improving Multi-agent Large Language Models with Sparse Mixture-of-Agents**<br>
D. Li, Z. Tan, P. Qian, Y. Li, **K. S. Chaudhary**, L. Hu, J. Shen · *PAKDD 2025* · [Paper](https://arxiv.org/abs/2411.03284)<br>
<sub>Makes multi-agent LLMs cheaper: a judge agent keeps only the best responses each round, and a moderator stops the discussion once the agents agree.</sub>

<br>

## Also built

**RISC-V emulator in the browser** (capstone, Aug 2025 – May 2026). An RV32I engine with 40+ instructions, single-step debugging and live register/memory views, so students can write assembly without setting up a VM. Includes assignment submission and grading for instructors.<br>
<sub>React · TypeScript · Python · PostgreSQL · Vercel</sub>

<br>

## Education

**Arizona State University**, 4.0 GPA<br>
MS Computer Science (accelerated), expected May 2027<br>
BS Computer Science, minor in Data Science, May 2026

<sub>**Tools I use:** Python, C++, SQL, R · PyTorch, Hugging Face Transformers, scikit-learn, LangChain, LangGraph · FastAPI, React, TypeScript · PostgreSQL, MySQL, MongoDB · Docker, Azure, GCP, GitHub Actions</sub>
