import random

# Интерфейс State
class State:
    def insert_quarter(self):
        pass

    def eject_quarter(self):
        pass

    def turn_crank(self):
        pass

    def dispense(self):
        pass

# Класс GumballMachine
class GumballMachine:
    def __init__(self, number_gumballs):
        self.sold_out_state = SoldOutState(self)
        self.no_quarter_state = NoQuarterState(self)
        self.has_quarter_state = HasQuarterState(self)
        self.sold_state = SoldState(self)
        self.winner_state = WinnerState(self)

        self.state = self.sold_out_state
        self.count = number_gumballs
        if number_gumballs > 0:
            self.state = self.no_quarter_state

    def insert_quarter(self):
        self.state.insert_quarter()

    def eject_quarter(self):
        self.state.eject_quarter()

    def turn_crank(self):
        self.state.turn_crank()
        self.state.dispense()

    def set_state(self, state):
        self.state = state

    def release_ball(self):
        print("A gumball comes rolling out the slot...")
        if self.count != 0:
            self.count -= 1

    def get_count(self):
        return self.count

    def get_sold_out_state(self):
        return self.sold_out_state

    def get_no_quarter_state(self):
        return self.no_quarter_state

    def get_has_quarter_state(self):
        return self.has_quarter_state

    def get_sold_state(self):
        return self.sold_state

    def get_winner_state(self):
        return self.winner_state

# Класс SoldOutState
class SoldOutState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def insert_quarter(self):
        print("You can't insert a quarter, the machine is sold out")

    def eject_quarter(self):
        print("You can't eject, you haven't inserted a quarter yet")

    def turn_crank(self):
        print("You turned, but there are no gumballs")

    def dispense(self):
        print("No gumball dispensed")

# Класс SoldState
class SoldState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def insert_quarter(self):
        print("Please wait, we’re already giving you a gumball")

    def eject_quarter(self):
        print("Sorry, you already turned the crank")

    def turn_crank(self):
        print("Turning twice doesn’t get you another gumball!")

    def dispense(self):
        self.gumball_machine.release_ball()
        if self.gumball_machine.get_count() > 0:
            self.gumball_machine.set_state(self.gumball_machine.get_no_quarter_state())
        else:
            print("Oops, out of gumballs!")
            self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())

# Класс NoQuarterState
class NoQuarterState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def insert_quarter(self):
        print("You inserted a quarter")
        self.gumball_machine.set_state(self.gumball_machine.get_has_quarter_state())

    def eject_quarter(self):
        print("You haven’t inserted a quarter")

    def turn_crank(self):
        print("You turned, but there’s no quarter")

    def dispense(self):
        print("You need to pay first")

# Класс HasQuarterState
class HasQuarterState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def insert_quarter(self):
        print("You can’t insert another quarter")

    def eject_quarter(self):
        print("Quarter returned")
        self.gumball_machine.set_state(self.gumball_machine.get_no_quarter_state())

    def turn_crank(self):
        print("You turned...")
        winner = random.randint(0, 9)
        if winner == 0 and self.gumball_machine.get_count() > 1:
            self.gumball_machine.set_state(self.gumball_machine.get_winner_state())
        else:
            self.gumball_machine.set_state(self.gumball_machine.get_sold_state())

    def dispense(self):
        print("No gumball dispensed")

# Класс WinnerState
class WinnerState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def insert_quarter(self):
        print("Please wait, we’re already giving you a gumball")

    def eject_quarter(self):
        print("Sorry, you already turned the crank")

    def turn_crank(self):
        print("Turning twice doesn’t get you another gumball!")

    def dispense(self):
        self.gumball_machine.release_ball()
        if self.gumball_machine.get_count() == 0:
            self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())
        else:
            self.gumball_machine.release_ball()
            print("YOU’RE A WINNER! You got two gumballs for your quarter")
            if self.gumball_machine.get_count() > 0:
                self.gumball_machine.set_state(self.gumball_machine.get_no_quarter_state())
            else:
                print("Oops, out of gumballs!")
                self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())

# Тестовый класс GumballMachineTestDrive
if __name__ == "__main__":
    gumball_machine = GumballMachine(5)

    print("\nInitial State:")
    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()

    print("\nAfter one gumball is dispensed:")
    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()

    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()

    print(f"\nRemaining gumballs: {gumball_machine.get_count()}")
