# FlashFill++: Scaling Programming by Example by Cutting to the Chase - Microsoft Research

Source: https://www.microsoft.com/en-us/research/publication/flashfill-scaling-programming-by-example-by-cutting-to-the-chase/
First opened: 2026-09-19

AI-generated from selected main-body sections; verify against the full paper.

## Summary points

- The paper introduces cuts, which combine input- and output-derived information to prune synthesis and enable a middle-out strategy that can handle operators poorly suited to either bottom-up enumeration or top-down inversion.
- It also introduces guarded DSLs with operator precedence, allowing larger DSLs with redundant operators while prioritizing preferred search branches and providing a default program ranking.
- FlashFill++ applies these techniques to string, datetime, and numeric transformations; the reported benchmark and survey results indicate broader task coverage, faster synthesis, similar example requirements, and more readable generated code than compared systems.

## Main takeaway

Cuts and precedence let FlashFill++ search expressive DSLs efficiently while producing readable programs for a wider range of example-driven transformations.

## My notes
