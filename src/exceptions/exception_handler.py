import sys
from src.logging.logger import get_logger

# Defining custom exception class
class CustomException:
    """
    Custom Exception class that captures error details such as error message,
    script filename and line number.

    """
    def __init__(self, error_message: str, error_details: sys):
        """
        Attributes:
                    error_message(str): The original error message.
                    error_details(sys): sys module to fetch exception details.

        """
        self.detailed_error_message = self.get_detailed_error_message(
            error_message,
            error_details
        )

    def get_detailed_error_message(self,error_message: str, error_details: sys):
        """
        Generates a detailed error message with filename and line number.

        """

        _,_,exc_tb = error_details.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        detailed_error_message = f"Error occured in script [{file_name}] at line number [{line_number}] with message: [{error_message}]."
        return detailed_error_message
    
    def __str__(self):
        """
        When str(exception) is called, return detailed error message.

        """

        return self.detailed_error_message


# Example usage
if __name__ == "__main__":
    logger = get_logger('exception_handler')
    logger.info('The code has started to run')

    def divide(a,b):
        c = a/b
        return c
    
    try:
        print(divide(1,0))
    except Exception as e:
        custom_exc = CustomException(e,sys)
        logger.error(f'{custom_exc}')
    

