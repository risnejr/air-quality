.PHONY: dashboard read_sensor gen_config aq_level

dashboard:
	cd dashboard/client && yarn start &
	cd dashboard/server && ./sse &

config:
	cd gen_config && python3 gen_config.py --id 9eed7c12-e97a-47ff-bac7-d38eef1f0c4c

aq_level:
	cd aq_level && python3 aq_level &