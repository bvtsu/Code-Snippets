import sys
sys.path.append('/Users/britsu/GitHub/affirmation/src/Affirmations/')
from Affirmations import affirm

@affirm
def hello_world():
    print("hello")

hello_world()