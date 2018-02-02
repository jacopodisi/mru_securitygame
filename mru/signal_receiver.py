import signal


class SignalReceiver:
    kill_now = False
    jump = False

    def __init__(self, log):
        self.log = log
        signal.signal(signal.SIGUSR1, self.exit_gracefully)
        signal.signal(signal.SIGUSR2, self.avoid_enum)

    def exit_gracefully(self, signum, frame):
        self.log.info("received kill signal")
        self.kill_now = True

    def avoid_enum(self, signum, frame):
        self.log.info("received jump signal")
        self.jump = True
