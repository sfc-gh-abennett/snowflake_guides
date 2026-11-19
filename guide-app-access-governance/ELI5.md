# Decide in the Gateway, Enforce in Snowflake: Plain Language Version

Pair-programmed by SE Community + Cortex Code

> Simplified from: [Decide in the Gateway, Enforce in Snowflake](README.md)

## One-Sentence Version

Let the front desk send people to the right room, but let every room's own lock decide who gets in, based on whose badge it is.

## The Story

Imagine an office building where every room holds a different client's files. Today, a receptionist takes each visitor's request, walks into the rooms with a master key, collects the files, and hands over only the ones she thinks that visitor should see. If she makes one mistake, or someone tricks her, the master key opens every room.

The better design gives every visitor their own badge. The receptionist still greets people and points them to the right floor, but each room's lock reads the visitor's own badge and opens only for the rooms they are allowed into. Each lock also writes down whose badge opened it.

Who gets which badge is written in one rulebook. When someone needs access, they ask for a change to the rulebook, someone reviews it, and the badges update everywhere at once. Every few months, the building checks which badges have gone unused and takes those permissions back.

The receptionist keeps a shelf of copies so repeat requests are fast. Each copy is labeled with exactly which rooms its owner can enter, so a copy is never handed to someone with different access. Even so, good badges and locks do not make a building perfectly safe: you still have to test that each lock behaves the way the rulebook says.

## The Cast

- **Gateway:** The receptionist who routes requests and keeps copies. She should not hold a master key.
- **Service identity:** A master key used by the receptionist or an app. One per app is safer than one for everyone.
- **External OAuth:** The badge a person carries into Snowflake, so Snowflake knows who they are.
- **Workload identity federation:** A badge for an app that comes from where the app runs, with no password to lose.
- **Agentic session:** A badge marked "assistant," so locks and logs can tell an AI agent from a person.
- **Entitlement catalog:** The rulebook of who may enter which rooms.
- **Database role:** A standard key ring for one set of rooms, either "read" or "read and write."
- **Row access policy:** The lock on each room that checks the visitor's own badge.
- **Masking policy:** A lock on individual drawers inside a room.
- **Access history:** The sign-in sheet each lock keeps.
- **Least-privilege report:** The review that finds badges nobody has used in 90 days.
- **App Runtime:** An option to move internal apps into the building itself, so visitors badge straight in.
- **Snowflake Postgres:** A filing cabinet for an app's working papers, copied into the main archive automatically.

## What Changed

These are the workflow changes the guide recommends:

- Replace one master key with a badge for every person, app, and agent.
- Replace filtering in app code with locks that Snowflake enforces on every request.
- Replace grants made by hand in each account with one reviewed rulebook applied everywhere.
- Replace a shared shelf of copies with copies labeled by exactly what their owner may see.
- Replace guesswork about access with a sign-in sheet and a regular review of unused permissions.

## What to Watch Out For

- A lock can only check the badge it is shown. If the receptionist still uses her master key, the locks cannot help.
- Some badge systems write their permissions in a format Snowflake reads differently. Test badges early, because this can need help from Snowflake Support.
- A visitor with no rooms assigned should hear "you have no clients yet," not "there is nothing here."
- A copy on the shelf without its access label can leak one client's files to another.
- The unused-badge review finds candidates to look at, not permissions to delete automatically.
- Some of the in-building options are still preview features with fixed sizes, and the Postgres cabinet is always on, so plan for its cost.
- Copies from the Postgres cabinet need a unique label on every file (a primary key). Without one, the cabinet stops allowing edits to those files.

## The One Thing to Remember

Pass the real caller through to Snowflake, so the data's own locks decide what each person, app, or agent can see.

> For the full technical details, see the source document.
