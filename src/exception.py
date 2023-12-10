import sys
import logging

def error_message_detail(error,error_detail:sys):
    """
    error_message_detail function returns a string describing 
    the error message that occurred during the execution.
    """
    _,_,exc_tb =  error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )
    return error_message


class CustomException(Exception):	
    """
    CustomException class is a subclass of Exception class that return the errors that occurs.

    """
    def __init__(self,error_message,error_detail:sys):
        ''' Create a instance of CustomException'''
        super().__init__(error_message)
        self.error_message = error_message_detail(error_detail,error_detail=error_detail)

    def __str__(self):
        '''
        returns a string representation of the error message
        '''
        return self.error_message
