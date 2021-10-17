import sys
sys.path.append('/path/to/affirmation/src/Affirmations/')
from Affirm import affirm

@affirm
def hello_world():
    print("hello")

hello_world()