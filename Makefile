build:
	docker build -t driver-pusher .
run:
	docker run driver-pusher

ghost_run:
	docker run -d driver-pusher