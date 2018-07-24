from alarm_level.alarm_level import AlarmLevel

if __name__ == '__main__':
	desk = AlarmLevel('desk', 'node_ids.csv')
	desk.main()
