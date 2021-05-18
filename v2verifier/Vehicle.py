import socket
import v2verifier.V2VReceive
import v2verifier.V2VTransmit


class Vehicle:
    """A class to represent a vehicle

    Attributes:
    ----------
    public_key : int
        the vehicle's public key
    private_key : int
        the vehicle's private key

    Methods
    -------


    """

    def __init__(self, public_key: int, private_key: int) -> None:
        """Constructor for the vehicle class

        Parameters:
            public_key (int): the vehicle's public key
            private_key (int): the vehicle's private key

        Returns:
            None
        """

        self.public_key = public_key
        self.private_key = private_key
