import unittest
from typing import Optional
from in_memory_db import KeyValueStore, TransactionException


class TestKeyValueStore(unittest.TestCase):
    def setUp(self):
        """Set up a new KeyValueStore instance before each test."""
        self.store = KeyValueStore()

    def test_put_without_transaction(self):
        """Test that put() raises an exception when no transaction is in progress."""
        with self.assertRaises(TransactionException):
            self.store.put("key1", 100)

    def test_get_without_transaction(self):
        """Test that get() works outside of a transaction."""
        # Setup: Start transaction, put a value, and commit
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.commit()

        # Test: Get should work without a transaction
        self.assertEqual(self.store.get("key1"), 100)

    def test_begin_transaction_nested(self):
        """Test that nested transactions are not allowed."""
        self.store.begin_transaction()
        with self.assertRaises(TransactionException):
            self.store.begin_transaction()

    def test_transaction_isolation(self):
        """Test that changes in a transaction are not visible until commit."""
        # Setup: Add initial value
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.commit()

        # Start new transaction and modify value
        self.store.begin_transaction()
        self.store.put("key1", 200)

        # Get should still return old value
        self.assertEqual(self.store.get("key1"), 100)

    def test_successful_commit(self):
        """Test that committed changes become visible."""
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.commit()

        self.assertEqual(self.store.get("key1"), 100)

    def test_successful_rollback(self):
        """Test that rolled back changes are discarded."""
        # Setup: Add initial value
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.commit()

        # Start new transaction and modify value
        self.store.begin_transaction()
        self.store.put("key1", 200)
        self.store.rollback()

        # Value should remain unchanged
        self.assertEqual(self.store.get("key1"), 100)

    def test_multiple_operations_in_transaction(self):
        """Test multiple operations within a single transaction."""
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.put("key2", 200)
        self.store.put("key1", 300)  # Update existing key
        self.store.commit()

        self.assertEqual(self.store.get("key1"), 300)
        self.assertEqual(self.store.get("key2"), 200)

    def test_get_nonexistent_key(self):
        """Test that get() returns None for non-existent keys."""
        self.assertIsNone(self.store.get("nonexistent"))

    def test_commit_without_transaction(self):
        """Test that commit() raises an exception when no transaction is in progress."""
        with self.assertRaises(TransactionException):
            self.store.commit()

    def test_rollback_without_transaction(self):
        """Test that rollback() raises an exception when no transaction is in progress."""
        with self.assertRaises(TransactionException):
            self.store.rollback()

    def test_input_validation(self):
        """Test input validation for keys and values."""
        self.store.begin_transaction()

        # Test invalid key type
        with self.assertRaises(ValueError):
            self.store.put(123, 100)  # Key must be string

        # Test invalid value type
        with self.assertRaises(ValueError):
            self.store.put("key1", "100")  # Value must be integer

        # Test invalid key type for get
        with self.assertRaises(ValueError):
            self.store.get(123)

    def test_transaction_state_after_commit(self):
        """Test that transaction state is properly reset after commit."""
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.commit()

        # Verify transaction state is reset
        with self.assertRaises(TransactionException):
            self.store.put("key2", 200)  # Should fail as no transaction is active

    def test_transaction_state_after_rollback(self):
        """Test that transaction state is properly reset after rollback."""
        self.store.begin_transaction()
        self.store.put("key1", 100)
        self.store.rollback()

        # Verify transaction state is reset
        with self.assertRaises(TransactionException):
            self.store.put("key2", 200)  # Should fail as no transaction is active


if __name__ == '__main__':
    unittest.main()