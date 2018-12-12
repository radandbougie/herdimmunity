from pathogen import Pathogen
import random
from logger import logger as l
random.seed(42)

# here temporarily until I finish the mvp
names = "Alice, Bob, Charlie, Donna, Elizabeth, Fred, Greg, Hailey, Irene, Jake, Katie, Leroy, Mary, Nick, Olivia, Patrick, Quark, Riley, Sarah"

names = names.split(",")

class Person(object):
    def __init__(self, id, is_vaccinated=False, infection=None):
        # TODO: turn the infection var into a dictionary of pathogens with whether or not the person is vaccinated to them
        self.id = id
        self.name = random.choice(names)
        # should be None or a pathogen object
        self.infection = infection
        self.is_vaccinated = is_vaccinated
        self.newly_infected = False
        self.is_dead = False
        self.greetings = []
        self.has_been_sick = False

    def print_greeting(self):
        print("------------------")
        print("Hello! My name is", self.name, "(human #", self.id,")")
        if self.is_vaccinated:
            print("I am vaccinated.")
        else:
            print("I am not vaccinated.")
        if self.has_been_sick:
            print("I survived a disease.")
        if self.infection is None:
            print("Currently, I am not infected with anything.")
        else:
            print("Currently I am infected with", self.infection.name)
        print("------------------")

    def did_die(self):
        if not isinstance(self.infection, Pathogen):
            # print(self.name, "(human #", self.id,") was vaccinated and did not die.\n")
            return False
        elif self.is_vaccinated:
            # l.log_line("\n{}, human#{} did not die because they were immune.".format(self.name, self.id))
            return False
        elif self.newly_infected:
            self.newly_infected = False
            return False
        else:
            luck = random.uniform(0, 1)
            if luck >= self.infection.mortality_rate:
                l.log_line("\n{}, human#{} survives the infection!".format(self.name, self.id))
                # person survives the infection and stops being sick, they are now immune to the virus
                self.infection = None
                # could say if pathogen is a virus they become vaccinated
                self.is_vaccinated = True
                self.has_been_sick = True
                return False
            else:
                # person dies
                # add id after name
                l.log_line("\n{}, human#{}, has died of {}.".format(self.name, self.id, self.infection.name))
                self.is_dead = True
                self.infection = None
                return True

    def battle_infection(self, pathogen):
        luck = random.uniform(0, 1)
        if luck > pathogen.contagiousness:
            # person does not catch the infection
            l.log_line("\n{}, human#{} did not become infected.".format(self.name, self.id))
            return False
        else:
            # person becomes infected
            self.infection = pathogen
            self.newly_infected = True
            l.log_line("\n{}, human#{} has contracted {}!".format(self.name, self.id, self.infection.name))
            return True

    def interact(self, friend):
        # minor shortcut. If one of them is vaccinated there can be no transmission
        # TODO log these interactions
        if self.is_vaccinated or friend.is_vaccinated:
            l.log_line("\n{}, human#{} and human#{} interacted but one of them was either vaccinated or immune.".format(self.name, self.id, friend.id))
            return False # tested
        # neither is infected
        elif self.infection is None and friend.infection is None:
            l.log_line("\n{}, human#{} and human#{} interacted but they were both healthy.".format(self.name, self.id, friend.id))
            return False
        # both are infected so nothing is transmitted
        elif self.infection is not None and friend.infection is not None:
            l.log_line("\n{}, human#{} and human#{} interacted but they were both infected.".format(self.name, self.id, friend.id))
            return False
        # if self is infected but friend is not, expose friend to infection
        elif self.infection is not None and friend.infection is None:
            l.log_line("\n{}, human#{} has exposed {}, human#{} to {}!".format(self.name, self.id, friend.name, friend.id, self.infection.name))
            friend.battle_infection(self.infection)
            return True # tested
        # if self is not infected but friend is, expose self to infection
        elif self.infection is None and friend.infection is not None:
            l.log_line("\n{}, human#{} has exposed {}, human#{} to {}!".format(friend.name, friend.id, self.name, self.id, friend.infection.name))
            self.battle_infection(friend.infection)
            return True # tested

class Population(object):
    def __init__(self, name, people, pathogen, initial_infected, percent_vaccinated=0.0):
        self.size = people
        self.initial_infected = initial_infected
        self.name = name
        self.percent_vaccinated = percent_vaccinated
        self.the_living = []
        self.the_dead = []
        vaccinated_people_num = int( people * percent_vaccinated)
        self.vaccinated_people_num = vaccinated_people_num
        # initialize patient zeroes
        id = 0
        for i in range(0, initial_infected):
            person = Person(id, False, infection=pathogen)
            person.newly_infected = True
            id += 1
            self.the_living += [person]
        # initialize number of vaccinated peeps
        for i in range(0, vaccinated_people_num):
            person = Person(id, True, infection=None)
            self.the_living += [person]
            id += 1
        # add everyone else to the population
        for i in range(0, (people - (vaccinated_people_num + initial_infected))):
            person = Person(id, False, infection=None)
            self.the_living += [person]
            id += 1

    def get_number_infected(self):
        people_infected = 0
        for person in self.the_living:
            if isinstance(person.infection, Pathogen):
                people_infected +=1
        return people_infected

    def get_number_immune(self):
        people_immune = 0
        for person in self.the_living:
            if person.is_vaccinated:
                people_immune +=1
        return people_immune

    def get_number_newly_infected(self):
        people = 0
        for person in self.the_living:
            if person.newly_infected:
                people +=1
        return people

    # TODO: currently bury the dead should wipe all infection from the game
    def mingle(self, interactions, pathogen):
        if len(self.the_living) <= interactions:
            print("Everyone died :(")
            return False
        else:
        # interactions defines how sociable people in this population are
        # each person interacts with a number of friends equal to interactions
            for person in self.the_living:
                person.greetings = []
                while len(person.greetings) < interactions:
                    # print("My name is {} and I have interacted with {}".format(person.id, person.greetings))
                    friend = random.choice(self.the_living)
                    # makes sure neither of them have seen each other today
                    if friend not in person.greetings and person not in friend.greetings:
                    # TODO adapt this for multiple pathogens
                        person.interact(friend)
                        person.greetings.append(friend)
            return True

    def get_dead(self):
        poppable = []
        index = 0
        for person in self.the_living:
            if person.newly_infected:
                person.newly_infected = False
            elif person.did_die():
                self.the_dead.append(person)
                poppable += [index]
        return poppable

    def bury_the_dead(self):
        pop_these = self.get_dead()
        for i in pop_these:
            self.the_living.pop(i)

    def print_info(self):
        population_num = str( len(self.the_living) + len(self.the_dead) )
        infected_num = str( self.get_number_infected() )
        dead_num = str( len(self.the_dead) )
        vaccination_rate = str( int( self.percent_vaccinated * 100 ) ) + "%"

        print("This population is known as", self.name, ". \n", vaccination_rate, "of the humans in this population are vaccinated.")

        print("Out of " + population_num + " people, " + infected_num, "are infected and " + dead_num + " have died.")

def test():
    # Population(self, name, people, pathogen, initial_infected, percent_vaccinated=0.0)
    virus = Pathogen("the gay agenda", 0.5, 0.5)
    # person1 = Person()
    # person1.print_greeting()
    # person1.get_infected(stale_memes)
    # person1.get_infected(dank_memes)
    # person1.print_greeting()
    # person1.did_die()
    # print("above human should have died\n")
    # person2 = Person()
    # person2.is_vaccinated = True
    # person2.get_infected(stale_memes)
    # person2.get_infected(dank_memes)
    # person2.did_die()
    make_school = Population("Make School", 30, virus, 3, 0.5)
    make_school.print_info()
    make_school.mingle(2, virus)
    make_school.bury_the_dead()
    make_school.print_info()

# test()
