# The repository dependency catalog: writing it, checking it, and the order it gives (v1)

Remedy can work across several of your repositories at once. When it does, it needs to know
which repository depends on which — a toolbox before the app that uses it, a shared library
before everything that imports it — so that an order spanning several repositories runs its jobs
in a sensible sequence. That knowledge comes from one file you write yourself: the repository
catalog.

## Where the file lives

The catalog is `<data root>/org/catalog.toml`, under Remedy's data root. It is written by hand.
Nothing in Remedy discovers your repositories or their dependencies for you and writes this file
on your behalf — there is deliberately no crawler. You create and edit it the way you would any
other configuration file, and Remedy only ever reads it.

## A small example

A catalog with three repositories, naming every key an entry may carry:

```toml
[[repo]]
pid = "toolbox"
name = "Shared Toolbox"
root = "~/code/toolbox"
owner = "platform-team"
publishes = ["@acme/toolbox"]

[[repo]]
pid = "brain"
name = "Brain Service"
root = "~/code/brain"
owner = "platform-team"
depends_on = ["toolbox"]
publishes = ["@acme/brain-client"]
consumes = ["@acme/toolbox"]

[[repo]]
pid = "app"
name = "Customer App"
root = "~/code/app"
owner = "app-team"
depends_on = ["brain", "toolbox"]
consumes = ["@acme/brain-client"]
```

- `pid` is the only required key: the project's slug or id, the same one an order file names.
- `name`, `root` and `owner` are for a person reading the catalog; `root` is where that
  repository lives on disk (`~` is expanded).
- `depends_on` lists the `pid`s this repository needs built or available first.
- `publishes` and `consumes` name the packages this repository ships and uses — they feed the
  plausibility check below and never the ordering itself.

## What an order over several projects does with it

When you give Remedy an order that spans more than one of your projects, it reads the catalog
and plans the jobs so that a repository's job runs only after the jobs of every repository it
depends on, directly or through others. The plan says so in plain language, citing the
dependency that required the sequence — "app depends on toolbox through brain", for example. A
repository the catalog does not mention, or an order touching only one repository, is unaffected.

## The two commands

- `remedy project catalog-check` reads the catalog and reports whether it is valid, together with
  every plausibility warning (see below) and every repository it could not check.
- `remedy project catalog-show` reads the catalog and prints every entry's fields, then the
  sequence it gives all of the catalog's repositories and the dependency behind each step of
  that sequence.

Both commands accept `--catalog <path>` to read a different file instead of the data root's own,
and `--json` for a machine-readable answer in Remedy's usual envelope shape. Run with no catalog
file in place, both say so and exit 0 — an absent catalog is not an error, just nothing to show.

## A cycle's refusal

A catalog where `app` depends on `brain` and `brain` depends on `app` (directly, or through any
longer chain back to itself) is refused outright: both commands exit 1 and name the exact cycle,
for example `app -> brain -> app`. The same is true of any other broken catalog — invalid TOML,
an unknown key, a missing `pid`, or a dependency on a `pid` the catalog does not hold.

## The warnings and their proofs

`catalog-check` also tries to catch a catalog that has fallen out of date. For each repository,
it reads the lockfile at that repository's own root — `package-lock.json`, `uv.lock`,
`poetry.lock` or `Cargo.lock`, whichever is present — and compares the packages it names against
what every other repository in the catalog `publishes`. A `consumes` entry you wrote by hand is
read the same way. When a repository's lockfile (or its `consumes` list) names a package another
catalog entry publishes, and the catalog gives the first repository no `depends_on` edge to the
second, `catalog-check` prints a warning naming both repositories and the package, with its
proof: the lockfile's file name, or the word `consumes` when a lockfile did not supply it.

## Deliberate absences

- No crawler ever writes or edits the catalog; it is read-only to Remedy and hand-written by you.
- A lockfile is only ever read at a repository's own root — Remedy never walks into
  subdirectories looking for one, so a monorepo's nested workspaces are not read this way.
- A plausibility warning never changes the catalog. The catalog is your word about your
  repositories; the warning only helps you keep it honest.
