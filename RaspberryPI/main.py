#### The FSM for the Raspberry Pi Control System ####
import FSMClasses
from FSMConfig import config
from time import sleep
import can
import piplates.RELAYplate as RELAY
import brakes
import motors

# let the pod coast
def coast():
    pass

# power on the pod systems into start up state
def initialize_pod():
    # check communication with vital sensors and MCUs
    motors.create_motors()     # create motors
    brakes.create_brakes()     # create brake objects
    # initialize other peripherals
    print("I have initalized")

# power off protocol
def power_off():
    print("I am powering off")
    # power off stuff
    motors.motors_off()

# determine if pod is safe to approach
def safe_to_approach_check():
    print("I am checking if I am safe to apprach")
    # by default, safe to approach is false
    SAFE_TO_APPROACH = False
    # TODO: velocity test

    # TODO: power to motor test

    # TODO: power to brakes test

    return SAFE_TO_APPROACH

def main():
    state = state_dict["start_up"] # start in start_up state
    fault = False

    while state != state_dict["fault"]: # check for fault condition
        # START UP STATE
        if state == state_dict["start_up"]:
            print("****START UP****")
            initialize_pod() # power on sequence
            state = state_dict["system_diagnostic"] # always move to system diagnositc state from start up

        # SYSTEM DIAGNOSTIC
        elif state == state_dict["system_diagnostic"]:
            print("****SYSTEM DIAGNOSTIC****")
            if health.safe_to_approach_check() == True:
                state = state_dict["safe_to_approach"]
            else: # if not safe to approach, move to fault state
                fault = True
                state = state_dict["Fault"]

        # SAFE TO APPROACH
        elif state == state_dict["safe_to_approach"]:
            print("****SAFE TO APPROACH****")
            launch = input("Prepare to launch? (True/False) ") #TODO: connect to GUI
            if launch == "True":
                state = state_dict["prepare_to_launch"]
            else:
                sleep(5) # wait 5s before looping
                state = state_dict["safe_to_approach"]

        # PREPARE TO LAUNCH
        elif state == state_dict["prepare_to_launch"]:
            print("****PREPARE TO LAUNCH****")
            # what do we do here?
            state = state_dict["ready_to_launch"]

        elif state == state_dict["ready_to_launch"]:
            print("****READY TO LAUNCH****")
            ready_to_launch = input("Are you sure you want to launch? (True/False) ")
            if ready_to_launch == "True":
                state = state_dict["launching"]
            else:
                state = state_dict["system_diagnostic"]

        elif state == state_dict["launching"]:
            print("****LAUNCHING****")
            while distance < FSMConfig.stop_distance: #TODO: add stop distance threshold
                accelerate()
            state = state_dict["coasting"] # once we are done accelerating

        elif state == state_dict["coasting"]:
            print("****COASTING****")
            motors_off() # cut power to motors
            brakes_off() # disengage brakes
            while distance <= coast_distance:
                # keep coasting
                coast()

        elif state == state_dict["braking"]:
            print("****BRAKING****")
            brakes_full_stop()
            if velocity == 0:
                state = state_dict["safe_to_approach"]
            else:
                fault = True
                state = state_dict["fault"]

        elif state == state_dict["crawling"]:
            print("****CRAWLING****")
            pass

        elif state == state_dict["power_off"]:
            print("****POWER OFF****")
            power_off()
            pass

        else:
            state = state_dict["fault"] # should never reach this state

    else:
        while fault == True:
            if state == state_dict["fault_braking"]:
                # if fault_braking_done ==
                brakes_full_stop()
                if velocity == 0:
                    state = state_dict["fault_stop"]
                else:
                    state = state_dict["fault_braking"]

            elif state == state_dict["fault_stop"]:
                pass

            elif state == state_dict["fault_diagnostic"]:
                print("FAULT: I have entered a FAULT state")

            elif state == state_dict["fault_diagnostic"]:
                print("FAULT: I have entered a FAULT state")

        if velocity != 0:
            #is it safe to stop
            # if moving, determine whether to stop or not
            # if not moving, try to reach safe to approach conditions
            #   determing whether problem is with brakes
            #   if problem is not brakes, apply brakes
            print("I think I am moving")
        elif config["velocity"] == 0:
            # attempt to reach safe to approach conditions
            print("FAULT: but at least I'm not moving")
        else:
            state = state_dict["fault_diagnostic"]
    # end eventually, please
    loop += 1
    if loop >= 100:
        sys.exit()
main()
