from file_moover.moover import File_Mover
from file_moover import config
moover=File_Mover(config.FCS_to_ES,config.ES_input)
while True:
    moover.work_cycle()