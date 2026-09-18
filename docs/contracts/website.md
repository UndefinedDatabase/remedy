# Contract template — website

The floor of the contract for an order that builds a website. Every criterion below is part of
such a mission's contract, and the planner adds its own criteria on top; it never drops one of
these. The format is DECISION F269 D1's, and `remedy do --contract website` forces this template.

## Proposed when the order mentions

- website
- web site
- landing page
- web page
- homepage
- static site

## Criteria

- blocking: Every page the order names is built, and a test loads each one and checks its main content.
- blocking: Every link between the site's own pages resolves, and a test proves it.
- blocking: The test suite passes.
- advisory: Every page has a title and one top-level heading, and a test proves it.

## Fixture order

Build a small website for a bakery with a home page, a menu page and a contact page.
