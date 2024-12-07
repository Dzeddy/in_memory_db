class TransactionException(Exception):
    """Custom exception for transaction-related errors."""
    pass

class KeyValueStore:
    def __init__(self):
        self.main_store = {}  # Main key-value store
        self.transaction_store = None  # Stores changes during a transaction
        self.in_transaction = False  # Flag to indicate if a transaction is active

    def begin_transaction(self):
        if self.in_transaction:
            raise TransactionException("A transaction is already in progress.")
        self.in_transaction = True
        self.transaction_store = {}
        print("Transaction started.")

    def put(self, key, value):
        if not self.in_transaction:
            raise TransactionException("No active transaction. Cannot perform 'put' operation.")
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        self.transaction_store[key] = value
        print(f"Put operation queued: {key} = {value}")

    def get(self, key):
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        # If in transaction, do not show uncommitted changes
        value = self.main_store.get(key)
        print(f"Get operation: {key} = {value}")
        return value

    def commit(self):
        if not self.in_transaction:
            raise TransactionException("No active transaction to commit.")
        # Apply all changes from the transaction store to the main store
        for key, value in self.transaction_store.items():
            self.main_store[key] = value
            print(f"Committed: {key} = {value}")
        # Clear transaction state
        self.transaction_store = None
        self.in_transaction = False
        print("Transaction committed.")

    def rollback(self):
        if not self.in_transaction:
            raise TransactionException("No active transaction to rollback.")
        # Discard all changes in the transaction store
        self.transaction_store = None
        self.in_transaction = False
        print("Transaction rolled back.")