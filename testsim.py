import pytest
from pathogen import Pathogen
from population import Population
# from simulation import Simulation
import random
import io
import sys

# from logger import logger

# TEST PATHOGEN
def test_print_pathogen_info():
    ebola = Pathogen("ebola", 0.70, 0.25)
    ebola_greeting = ebola.print_info(False)
    assert "ebola" in ebola_greeting
    assert "70" in ebola_greeting
    assert "25" in ebola_greeting

virus = Pathogen("the black plague", 0.5, 0.5)
my_pop = Population("1437 France", 30, virus, 3, 0.5)

def clear_log_file():
    file = open("NO_FILE_SPECIFIED.md", "w+")
    file.write("# this file for testing")
    print("File cleared.")
    print(file.read())

def read_log_file():
    file = open("NO_FILE_SPECIFIED.md", "r")
    print("File read.")
    return file.read()

# TEST PERSON
def test_did_die():
    virus.mortality_rate = 1.0
    my_pop.the_living[0].infection = virus
    my_pop.the_living[0].is_vaccinated = False
    assert not my_pop.the_living[0].did_die()
    assert my_pop.the_living[0].did_die()
    virus.mortality_rate = 0.0
    assert not my_pop.the_living[3].did_die()

def test_battle_infection():
    virus.contagiousness = 1.0
    my_pop.the_living[2].infection = None
    my_pop.the_living[3].infection = None
    assert my_pop.the_living[2].battle_infection(virus)
    assert my_pop.the_living[2].infection is virus
    virus.contagiousness = 0.0
    assert not my_pop.the_living[3].battle_infection(virus)
    assert my_pop.the_living[3].infection is None

def test_interact():
    clear_log_file()
    virus.contagiousness = 1.0
    person = my_pop.the_living[4]
    friend = my_pop.the_living[5]
    # make sure infection is transmitted to non-vaccinated person
    person.is_vaccinated = False
    friend.is_vaccinated = False
    person.infection = None
    friend.infection = virus
    assert person.interact(friend)
    assert person.infection is virus
    # assert "INFECTION TRANSMITTED" in read_log_file()
    # make sure virus is not transmitted to vaccinated person
    clear_log_file()
    person.is_vaccinated = True
    person.infection = None
    friend.infection = virus
    assert not person.interact(friend)
    assert person.infection is None
    # assert "NO TRANSMISSION" in read_log_file()
    # make sure virus is not transmitted to vaccinated friend
    person.is_vaccinated = False
    friend.is_vaccinated = True
    person.infection = virus
    friend.infection = None
    assert not person.interact(friend)
    assert friend.infection is None

# TEST POPULATION
p_virus = Pathogen("lycanthropy", 0.0, 0.0)
p_pop = Population("Forks, Washington", 10, p_virus, 1, 0.1)

def test_init():
    assert len(p_pop.the_living) is 10
    assert p_pop.the_living[0].infection is p_virus
    assert p_pop.the_living[1].is_vaccinated is True

def test_get_number_infected():
    p1_pop = Population("New York", 20, p_virus, 0, 0.5)
    assert p1_pop.get_number_infected() is 0
    p1_pop.the_living[0].infection = p_virus
    assert p1_pop.get_number_infected() is 1
    for person in p1_pop.the_living:
        person.infection = p_virus
    assert p1_pop.get_number_infected() is 20
    p1_pop.the_living[1].infection = None
    p1_pop.the_living[0].infection = None
    assert p1_pop.get_number_infected() is 18

def test_get_number_immune():
    p1_pop = Population("New York", 20, p_virus, 1, 0.5)
    assert p1_pop.get_number_immune() is 10
    p1_pop = Population("New York", 20, p_virus, 1, 1.0)
    assert p1_pop.get_number_immune() is 20

def test_mingle():
    pass
    # TODO not sure how to test this effectively

# commented out because no longer relevant
def test_bury_the_dead():
    p2_virus = Pathogen("Libertarianism", 1.0, 1.0)
    p2_pop = Population("Rapture", 6, p2_virus, 6, 0.0)
    # print(p2_pop.the_living[0].print_greeting())
    assert len(p2_pop.the_living) is 6
    assert len(p2_pop.the_dead) is 0
    for person in p2_pop.the_living:
        person.newly_infected = False
        assert not person.is_dead
    for person in p2_pop.the_living:
        assert person.infection is p2_virus
        # person.print_greeting()
    assert p2_virus.mortality_rate is 1.0
    print("burying the dead")
    index = 0
    p2_pop.bury_the_dead()
    # print(p2_pop.the_living[0].name)
    print("List of living:")
    for person in p2_pop.the_living:
        print(person.id)
    print("List of dead:")
    for person in p2_pop.the_dead:
        print(person.id)
    assert len(p2_pop.the_living) is 0
    assert len(p2_pop.the_dead) is 6

def test_newly_infected():
    p3_virus = Pathogen("This class", 1.0, 1.0)
    p3_pop = Population("My brain cells", 2, p3_virus, 2, 0.0)
    assert p3_pop.the_living[0].newly_infected
    assert not p3_pop.the_living[0].did_die()
    assert not p3_pop.the_living[0].newly_infected
    assert p3_pop.the_living[0].did_die()

# TEST RUN LOOP

# def test_sim():
    # sim = Simulation()

    # sim.pathogen_name = "Ebola"
    # sim.mortality_rate = 1.0
    # sim.infectiousness = 1.0
    # sim.population_size = 10
    # sim.initial_infected = 10
    # sim.percent_vaccinated = 0.0

    # sim.initialize()
    # sim.run(logger)

    # assert len(sim.population.the_living) is 0
