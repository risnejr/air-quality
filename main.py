from aq_level.aq_level import AQLevel
import json

if __name__ == '__main__':
    with open('../config.json', 'r') as f:
        node_ids = json.load(f)
    demo = AQLevel('install_team_room', 'demo', node_ids)
    demo.main()
