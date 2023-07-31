
from scenic.simulators.airsim.simulator import AirSimSimulator    # for use in scenarios

# ---------- global parameters ----------
# Parameters of a scene like weather or time of day which are not associated with any object. 
# These are defined using the param statement, and can be overridden from the command line with the --param option.

# setting Default global parameters for any missing parameters
# TODO
param timestep = 4


# applying global parameters
simulator AirSimSimulator(None, timestep=globalParameters.timestep) 



class AirSimActor:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    