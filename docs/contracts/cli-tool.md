# Contract template — cli-tool

The floor of the contract for an order that builds a command-line tool. Every criterion below is
part of such a mission's contract, and the planner adds its own criteria on top; it never drops one
of these. The format is DECISION F269 D1's, and `remedy do --contract cli-tool` forces this
template.

## Proposed when the order mentions

- cli
- command-line
- command line
- cli tool
- terminal tool

## Criteria

- blocking: Every command and option the order names exists, and a test runs each one and checks its output.
- blocking: The help output describes every command and option, and a test proves it.
- blocking: A wrong argument exits with a non-zero status and a message on standard error, and a test proves it.
- blocking: The test suite passes.

## Fixture order

Build a command-line tool that counts the words in the files it is given.
