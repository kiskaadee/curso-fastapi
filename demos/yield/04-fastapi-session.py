"""
Lifecycle Management - Using `yield` for Resource Cleanup

Problem Statement:
    A web application needs a database connection for every request.

    Each request should:
        1 - Open a Session
        2 - Use the Session
        3 - Close the Session

    Forgetting step 3 can leave connections open and eventually
    exhaust the database connection pool.

    How can we guarantee that every session is cleaned up,
    even if an exception occurs?

In previous examples, we used generators to produce values lazily.

In this example, the generator serves a different purpose:
    It keeps a resource alive while work is being performed.
The lifecycle looks like this:

                setup
                    ↓
                yield resource
                    ↓
                perform work
                    ↓
                resume
                    ↓
                cleanup

FastAPI uses this pattern for dependency injection.

We will try to demonstrate the underlying idea wihtout
requiring FastAPI or a real database.


Lifecycle:

        main()
          │
          ▼
    get_session()
          │
          │ setup
          ▼
    yield session
          │
          ├──────────► endpoint()
          │                │
          │                ▼
          │          use session
          │
          ◄───────────────┘
          │
          │ resume generator
          ▼
       cleanup
          ▼
    FakeSession.__exit__()

"""

from time import sleep

# ------------------------------------------------------------------
# Step 1: Create a fake database session
# ------------------------------------------------------------------
#
# Real database sessions manage connections.
# For demonstration purposes we'll simply print messages.
#


class FakeSession:
    def __enter__(self):
        self.closed = False
        print("OPENING DATABASE CONNECTION")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.closed = True
        print("CLOSING DATABASE CONNECTION")

    def query(self, resource: str):
        if self.closed:
            raise RuntimeError("Cannot use a closed connection.")
        print(f"Retrieving '{resource}'...")
        sleep(0.5)
        print(f"Returned '{resource}'...")


# ------------------------------------------------------------------
# Step 2: Create a generator dependency
# ------------------------------------------------------------------
#
# This resembles a typical FastAPI dependency.
#
# Important:
#   The code before `yield` performs setup
#
#   The generator then pauses and hand the session
#   to the caller
#
#   When resumed, execution continues after the `yield`
#   and performs cleanup.
#


def get_session():
    with FakeSession() as session:
        print("SETUP COMPLETE")
        print("Yielding session...\n")

        yield session

        print("\nTEARDOWN STARTED")
        print("Generator resumed")


# ------------------------------------------------------------------
# Step 3: Simulated endpoint
# ------------------------------------------------------------------
#
# In FastAPI, the session would be injected automatically.
#


def fake_endpoint(resource: str, session: FakeSession):
    print("Endpoint started")

    if resource == "crash":
        raise ValueError("Something went wrong.")

    session.query(resource)

    print("Endpoint finished")


# ------------------------------------------------------------------
# Experiment 1
# ------------------------------------------------------------------
#
# Normal request lifecycle
#


def normal_request_demo():
    print("\n" + "=" * 60)
    print("EXPERIMENT 1 - NORMAL REQUEST")
    print("=" * 60)

    dependency = get_session()

    print("\nRequest arrives")
    print("FastAPI requests a session\n")

    session = next(dependency)

    fake_endpoint("/api/users/", session)

    print("\nRequest completed")
    print("Resuming dependency\n")

    try:
        next(dependency)
    except StopIteration:
        print("Generator exhausted")


# ------------------------------------------------------------------
# Experiment 2
# ------------------------------------------------------------------
#
# Attempting to use a session after cleanup.
#


def closed_session_demo():
    print("\n" + "=" * 60)
    print("EXPERIMENT 2 - USING A CLOSED SESSION")
    print("=" * 60)

    dependency = get_session()

    session = next(dependency)

    fake_endpoint("/api/product/", session)

    try:
        next(dependency)
    except StopIteration:
        pass

    print("\nTrying to reuse the session after cleanup...\n")

    try:
        session.query("/api/orders/")
    except RuntimeError as exc:
        print(exc)


# ------------------------------------------------------------------
# Experiment 3
# ------------------------------------------------------------------
#
# Endpoint crashes.
#
# Cleanup should still occur.
#


def exception_demo():
    print("\n" + "=" * 60)
    print("EXPERIMENT 3 - EXCEPTION DURING REQUEST")
    print("=" * 60)

    dependency = get_session()

    session = next(dependency)

    try:
        fake_endpoint("crash", session)
    except ValueError as exc:
        print(f"Endpoint raised: {exc}")

    finally:
        print("\nRequest aborted")
        print("Running cleanup\n")

        try:
            next(dependency)
        except StopIteration:
            print("Generator exhausted")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------


if __name__ == "__main__":
    normal_request_demo()

    # closed_session_demo()

    # exception_demo()
