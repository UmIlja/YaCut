from string import ascii_lowercase, ascii_uppercase, digits

DEFAULT_SHORT_ID_LENGTH = 6
MIN_USER_SHORT_ID_LENGTH = 1
MAX_USER_SHORT_ID_LENGTH = 16
LETTERS_AND_DIGITS = ascii_lowercase + ascii_uppercase + digits
LETTERS_AND_DIGITS_PATTERN = (
    rf'^[a-zA-Z0-9]{{{MIN_USER_SHORT_ID_LENGTH},'
    f'{MAX_USER_SHORT_ID_LENGTH}}}$'
)