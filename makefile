.PHONY: dashboard read_sensor gen_config aq_level

dashboard:
	cd dashboard/client && yarn start &
	cd dashboard/server && ./sse &

config:
	gen_config/config

aq_level:
	cd aq_level && python3 aq_level &