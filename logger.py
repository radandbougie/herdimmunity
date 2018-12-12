# from jinja2 but I have no idea how this works, I probably should stop using random things I find on the internet
def float_to_percent(my_float):
    return str( int(my_float * 100) ) + "%"



# basically where all interactions are
class Logger(object):
    def __init__(self):
        self.custom = ["","",""]
        self.file_name = "NO_FILE_SPECIFIED.md"
        # pretty sure nothing needs to be initialized, but if it does, insert here

    def add_file_name(self, sim):
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.md".format(sim.pathogen.name, sim.population.size, sim.population.percent_vaccinated, sim.population.initial_infected)

    def write_start_stats(self, sim):
        # code quality is approaching hell levels rn (really bad)
        t = open("start_stats.md", 'r').read()
        summary = t.format(
            sim.population_size,
            float_to_percent(sim.percent_vaccinated),
            sim.pathogen.name,
            float_to_percent(sim.pathogen.mortality_rate), float_to_percent(sim.pathogen.contagiousness), sim.initial_infected)
        # deleted code
        file = open("summaries/" + self.file_name, "w+")
        file.write(summary)
        file.close()

    def write_end_stats(self, sim, steps):
    
        t = open("end_stats.md", 'r').read()
        summary = t.format(
            len(sim.population.the_dead),
            len(sim.population.the_living) - sim.population.vaccinated_people_num,
            steps
            )
        file = open("summaries/" + self.file_name, "a")
        file.write(summary)
        file.close()

    def log_line(self, line):
        file = open("logs/" + self.file_name, "a")
        file.write(line)
        file.close()

    def log(self, sim, id):
        file_name = "logs/{}_simulation_pop_{}_vp_{}_infected_{}.md".format(sim.pathogen.name, sim.population.size, sim.population.percent_vaccinated, sim.population.initial_infected)
        file = open(file_name, "a")

        infected = sim.population.get_number_infected()
        dead = len(sim.population.the_dead)
        now_immune = sim.population.get_number_immune()
        new_infected = sim.population.get_number_newly_infected()

        info = "{}: {} dead, {} newly infected out of {} sick, {} now immune".format(id, dead, new_infected, infected, now_immune)
        print(info)
        file.write("\n\n"+info+"\n\n")

        file.close()

logger = Logger()
