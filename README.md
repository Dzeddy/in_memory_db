# InMemoryDB

## Overview

InMemoryDB is a simple in-memory key-value database with transaction support. It allows storing string keys with integer values and supports basic transaction operations adhering to ACID properties.

## Features

- **Get and Put Operations:** Retrieve and store key-value pairs.
- **Transaction Management:** Begin, commit, and rollback transactions.
- **ACID Compliance:** Ensures Atomicity, Consistency, Isolation, and Durability (within memory constraints).

## Setup Instructions

### Prerequisites

- Python 3.7 or higher installed on your machine.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/in_memory_db.git
   cd in_memory_db

## Usage Examples

```python

# Initialize the database

db = KeyValueStore()

# Basic operations

db.begin_transaction()

db.put("A", 5)

db.commit()

print(db.get("A"))  # Output: 5

# Transaction rollback example

db.begin_transaction()

db.put("B", 10)

db.rollback()

print(db.get("B"))  # Output: None

```

## Testing

Run the included tests with:

```bash

python -m unittest test_in_memory_db.py

```

## Project Structure

```

in_memory_db.py: Main implementation

test_in_memory_db.py: Unit tests

README.md: Documentation

```

## How to make it a better assignment


Include specific test cases that students must implement, covering edge cases and concurrent access scenarios. This would help ensure thorough understanding of transaction behavior.

Require students to document their design decisions and trade-offs, particularly around memory usage and performance characteristics. This would encourage deeper thinking about system design.

