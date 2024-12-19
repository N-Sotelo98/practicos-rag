from typing import List,Any
import time
class Formater:
    """
    Class used to format the data prepared it for the presentation layer
    """    
    @staticmethod
    def format_data(response:str):
        # incorporate streaming protocol
        for character in response:
            yield character

        