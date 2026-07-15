from uuid import UUID,uuid4

class User:

    def __init__(self, email : str, hashed_password : str, id : UUID = None):
        """
        Pure Python Object-Oriented Entity.
        It encapsulates its own data state and core validation logic.
        """

        self.id = id or uuid4()
        self.email = email
        self.hashed_password = hashed_password
