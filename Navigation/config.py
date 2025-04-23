# NETPIE setting
MQTT_CLIENT = "b1896fc3-dd7b-4528-bca1-a114f533b1d3"
MQTT_USERNAME = "4s5Pk9TSYLXi7yZEaC1p717KgTjq5Agq"
MQTT_PASSWORD = "Zk9gT4MD3tGxR8LP5K6ZwMmx9AEnfx6x"
MQTT_SERVER = "broker.netpie.io"
MQTT_PORT = 1883
MQTT_TOPIC = "@msg/data"

# CSV File
CSV_FILENAME = "Database.csv"

# For Navigation
GRAPH = {'B1': ['W', 'R'], 'B2': ['W'], 'B3': ['W'], 'H': ['M', 'W'], 'M': ['H'],
         'R': ['B1', 'W'], 'W': ['B1', 'B2', 'B3', 'H', 'R']}

DISTANCES = {('B1', 'W'): 2.44+1.06, ('B1', 'R'): 2.07+1.13,
             ('B2', 'W'): 2.44+1.06,
             ('B3' ,'W'): 4.12,
             ('H', 'M'): 1.72+0.90, ('H', 'W'): 3.51,
             ('R', 'W'): 1.25+1.17}

COORDINATES = {'B1': (838, 179), 'B2': (840, 868), 'B3': (237, 873),
               'H': (286, 239), 'M': (181, 522), 'R': (831, 522), 'W': (580, 522),
               'Beacon1': (975, 1044), 'Beacon2':(97, 647), 'Beacon3':(494, 77)}

PATH_POINTS = {('B1', 'W'): (605,417), ('B1', 'R'): (753,417),
               ('B2', 'W'): (605,637),
#               ('B3' ,'W'): (480,637),
               ('H', 'M'): (181,417),
               ('R', 'W'): (699,482)}

FULL_NAMES = {'Bedroom1':'B1', 'Bedroom2':'B2', 'Bedroom3':'B3',
              'Hall':'H', 'Living room':'M', 'Bathroom':'R', 'Corridor':'W',
              'Current Location':'Current Location'}
