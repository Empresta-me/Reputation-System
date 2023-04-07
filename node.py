
from hashlib import sha256
from datetime import datetime
from src.crypto import Crypto
import base58
import uuid
import os
import configparser

class Node:
    def __init__(self, name : str):
        """
        Initializes a new Node instance with a random private key and public key.
        """

        # gets public and private key from PEM file
        with open("config/key.pem", "rb") as key_file: 
            self.private_key = Crypto.PEM_to_private_key(key_file.read(), bytes("testpassword",'utf-8'))
            self.public_key =  self.private_key.public_key()
        self.serialized_public_key = base58.b58encode(Crypto.serialize(self.public_key)).decode('utf-8')

        self.name = name
        self.id = str(uuid.uuid4())
        self.vouches = {}  # List to hold all vouches received by this Node
        self.clock = 0  # Clock value to assign to new vouches 

    def vouch(self, recipient, vouch_type, comment):
        """
        Creates a new vouch message and signs it with this Node's private key.

        Args:
            recipient (Node): The Node being vouched for.
            vouch_type (str): The type of vouch being made (True or False).
            comment (str): A comment on the vouch.

        Returns:
            dict: The new vouch message as a dictionary.
        """
        # Create a new vouch message
        self.clock += 1  # Increment the clock value
        timestamp = datetime.now().timestamp()  # Get the current timestamp
        vouch_data = f"{self.serialized_public_key}{recipient.serialized_public_key}{vouch_type}{comment}{timestamp}{self.clock}"  # Concatenate the vouch data
        vouch_hash = sha256(vouch_data.encode()).hexdigest()  # Hash the vouch data
        vouch = {
            "sender": self.serialized_public_key,
            "recipient": recipient.serialized_public_key,
            "recipient_name": recipient.name,
            "vouch_type": vouch_type,
            "comment": comment,
            "timestamp": timestamp,
            "hash": base58.b58encode(vouch_hash.encode()).decode(),
            "clock": self.clock
        }
        
        # Sign the vouch message with this Node's private key
        signature = Crypto.sign(self.private_key, vouch_hash.encode())

        # Add the signature to the vouch message
        vouch['signature'] = base58.b58encode(signature).decode()

        # Add the vouch to our local vouch list
        self.vouches[recipient.name] = vouch

        # Return the new vouch message
        return vouch


    def unvouch(self, recipient_public_key, vouch_hash):
        """
        Removes a vouch message from this Node's local vouch list.

        Args:
            recipient_public_key (str): The public key of the Node being vouched for.
            vouch_hash (str): The hash of the vouch message to be removed.

        Returns:
            None.
        """
        # Find the existing vouch in our local vouch list and remove it
        for i, local_vouch in enumerate(self.vouches):
            if base58.b58decode(local_vouch['recipient']).decode() == recipient_public_key and base58.b58decode(local_vouch['hash']).decode() == vouch_hash:
                self.vouches.pop(i)  # Remove the vouch message from the list
                break


    def update_vouch_type(self, recipient_public_key, vouch_hash, vouch_type):
        """
        Updates an existing vouch message with a new vouch type and signature.

        Args:
            recipient_public_key (str): The public key of the Node being vouched for.
            vouch_hash (str): The hash of the vouch message to be updated.
            vouch_type (int): The new vouch_type of the vouch (-1, 0, or 1).

        Returns:
            dict: The updated vouch message.
        """

        # Find the existing vouch in our local vouch list and update it with the new vouch_type and signature
        for i, local_vouch in enumerate(self.vouches):
            if local_vouch['recipient'] == recipient_public_key and local_vouch['hash'] == vouch_hash:
                # Create the new vouch data string
                vouch_data = f"{self.public_key}{self.serialized_public_key}{local_vouch['vouch_type']}{local_vouch['message']}{local_vouch['comment']}{local_vouch['timestamp']}{local_vouch['clock']}"

                # Update the hash, vouch_type, and clock values in the vouch message
                local_vouch['hash'] = sha256(vouch_data.encode()).hexdigest()
                local_vouch['vouch_type'] = vouch_type
                local_vouch['clock'] += 1

                # Sign the updated vouch message with this Node's private key
                signature = Crypto.sign(self.private_key, local_vouch['hash'].encode())

                # Add the signature to the vouch message
                local_vouch['signature'] = base58.b58encode(signature).decode()

                # Update the vouch in our local vouch list
                self.vouches[i] = local_vouch

                # Return the updated vouch message
                return local_vouch
            
    def update_vouch_comment(self, recipient_public_key, vouch_hash, comment):
        """
        Updates an existing vouch message with a new comment.

        Args:
            recipient_public_key (str): The public key of the Node being vouched for.
            vouch_hash (str): The hash of the vouch message to be updated.
            comment (str): The new comment to be added to the vouch message.

        Returns:
            dict: The updated vouch message.
        """

        # Find the existing vouch in our local vouch list and update it with the new comment
        for i, local_vouch in enumerate(self.vouches):
            if local_vouch['recipient'] == recipient_public_key and local_vouch['hash'] == vouch_hash:
                # Update the comment value in the vouch message
                local_vouch['comment'] = comment

                # Update the vouch in our local vouch list
                self.vouches[i] = local_vouch

                # Return the updated vouch message
                return local_vouch

    def get_vouches(self, recipient_public_key=None):
        """
        Gets all vouch messages received by this Node, optionally filtered by recipient.

        Args:
            recipient_public_key (str): The public key of the Node being vouched for. Optional.

        Returns:
            list: A list of vouch messages as dictionaries.
        """
        if recipient_public_key is None:
            # Return all vouches
            return self.vouches
        else:
            # Convert the recipient's public key to base58
            recipient_public_key_base58 = base58.b58encode(recipient_public_key.encode()).decode()

            # Return vouches for a specific recipient
            return [vouch for vouch in self.vouches if vouch['recipient'] == recipient_public_key_base58]
