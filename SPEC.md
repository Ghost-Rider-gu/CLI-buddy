# Technical Specification: CLI-Buddy

## 🛠️ Technical Stack

| Component | Technology | Why? |
| --- | --- | --- |
| **Runtime** | **Python 3.13+** | Access to latest type-hinting and performance features. |
| **CLI Framework** | **Typer** | Type-safe, fast development, and excellent sub-command support. |
| **UI & Formatting** | **Rich**, **Textual** | Industry standard for tables, progress bars, and beautiful logs. |
| **Package Manager** | **uv** | Extremely fast alternative to `pip`/`poetry`. |
| **Linter/Formatter** | **Ruff** | Blazing fast "all-in-one" linting and formatting. |
| **Database/ORM** | **SQLModel** | Perfect bridge between SQLAlchemy and Pydantic (validation + DB). |
| **Security** | **Keyring** | Securely stores secrets in the OS-level vault. |
| **Environment** | **Platformdirs** | Ensures cross-platform standards for config/cache locations. |

---

## 🏗️ Architecture & Structure

The project follows a **Modular Plugin Architecture**. The core application handles the "plumbing" (Auth, UI, Config), while logic is delegated to sub-command modules or external plugins.

### Directory Layout (src-layout)

```text
cli-buddy/
├── pyproject.toml           # Project metadata and Ruff config
├── src/
│   └── cli_buddy/
│       ├── __init__.py
│       ├── main.py          # Entry point & App Registry
│       ├── core/            # Internal logic
│       │   ├── auth.py      # Auth logic (Hashing, Keyring)
│       │   ├── config.py    # platformdirs + yaml
│       │   ├── database.py  # SQLModel engine & session setup
│       │   └── models.py    # SQLModel definitions
│       ├── commands/        # Built-in categorized commands
│       │   ├── net_tools/
│       │   └── dev_utils/
│       └── plugins/         # User-defined dynamic scripts
└── tests/                   # Pytest suite

```

---

## 🗄️ Database Schema (SQLModel)

CLI-Buddy uses a local **SQLite** database managed via **SQLModel**. While sensitive tokens are stored in the OS `keyring`, user profiles and session metadata are stored locally.

### Schema Definitions

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    """Core user table for CLI-Buddy authentication."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: Optional[str] = None
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationship to sessions
    sessions: list["Session"] = Relationship(back_populates="user")

class Session(SQLModel, table=True):
    """Tracks active login sessions for the CLI."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token_identifier: str = Field(unique=True) # ID to lookup in Keyring
    login_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    
    user: User = Relationship(back_populates="sessions")

```

### Security Best Practices

* **Password Hashing:** Use `argon2-cffi` or `bcrypt` for `hashed_password`. Never store the raw password.
* **Keyring Integration:** The `token_identifier` in the DB maps to a "Secret" stored in the system's secure vault (Keyring). This prevents unauthorized DB access from revealing actual API tokens or session keys.

---

## 🚀 Core Feature Specifications

### 1. Authentication (Gatekeeper)

* **Mechanism:** Users must run `buddy login` before accessing other commands.
* **Validation:** A Typer `Callback` checks for a valid `Session` record and a matching `keyring` entry.

### 2. The Splash Screen

* **Contents:** ASCII Art, Version, and "Logged in as: [Username]".
* **Performance:** Implemented via `rich.live` or a simple `rich.console` print.

### 3. Dynamic Plugin System

* Scans `~/.config/cli-buddy/plugins/`.
* Uses `importlib` to register functions dynamically.

---

## ⚖️ Trade-offs

* **SQLModel vs. SQLAlchemy:** We use **SQLModel** for developer speed and Pydantic integration. *Trade-off:* It is slightly newer, but for a CLI tool, the simplicity outweighs the edge-case limitations of raw SQLAlchemy.
* **Local SQLite vs. Remote Auth:** Local SQLite allows for offline use and faster command execution. *Trade-off:* Requires the user to protect their local machine files (though Keyring mitigates this).

---
## Features
- [ ] Packaging CLI app and installation
- [ ] ASCII logo for the CLI
- [ ] Setup GitHub Actions
- [ ] Static checker - lint
- [ ] Scrape data from Hacker News

---
## Ideas and Questions
1. How to scale the app?
2. Logging for CLI
3. Tools for documentation
4. Think about architecture of the CLI app