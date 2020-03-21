import json
config = {}
config['lastfiles'] = []
#config['lastfiles'].append({'name': 'mai2019.mp3', 'path': 'C:\\Users\\toshiba\\Desktop\\2020\\02 transcript\\mai2019.mp3'})
config['options'] = {'openlast': 'True', 'playlast': 'True' ,'lastpos': 'True'}
with open('config.json', 'w') as outfile:
    json.dump(config, outfile)
