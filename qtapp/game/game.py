from typing import Callable
from threading import Thread
from collections import deque
from time import time_ns, sleep

from shared.game import Tile, Grid, Direction, Snapshot, UserInput


def time():
    '''time in ms'''
    return time_ns() // 1e6


class Game(Thread):
    def __init__(self, player_id: int):
        super().__init__()
        self._player_id = player_id
        self._stop_flag = False

        self._user_input: UserInput | None = None
        self._send_input_cback: Callable[[UserInput], None] | None = None
        self._server_snapshot: Snapshot | None = None

        self._grid = Grid(8, 8)
        self._stored_commands: deque[UserInput] = deque()
        self._commands_to_execute: deque[UserInput] = deque()

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, val: UserInput):
        self._user_input = val

    @property
    def server_snapshot(self):
        return self._server_snapshot

    @server_snapshot.setter
    def server_snapshot(self, val: Snapshot):
        self._server_snapshot = val

    def onPackageToSend(self, func: Callable[[UserInput], None]):
        '''
        Callback to be called on package ready to send

        Calls with time and input id
        '''
        self._send_input_cback = func

    def onSceneUpdated(self, func: Callable[[list[Tile]], None]):
        '''
        Callback to be called when scene needs to be updated
        '''
        self._update_scene_cback = func

    def _exec_commands(self):
        while self._commands_to_execute:
            cmd = self._commands_to_execute.pop()
            if cmd.time > self._last_snapshot_time:
                self._stored_commands.append(cmd)
            self._grid.move(cmd.player_id, cmd.direction)

    def _updateStateFromSnapshot(self, snapshot: Snapshot):
        self._grid.from_tiles(snapshot.tiles)
        self._commands_to_execute.extendleft(self._stored_commands)
        self._stored_commands.clear()

    def run(self):
        '''
        Steps from Source:
        1. Sample clock to find start time
        2. Sample user input (mouse, keyboard, joystick)
        3. Package up and send movement command using simulation time
        4. Read any packets from the server from the network system
        5. Use packets to determine visible objects and their state
        6. Render Scene
        7. Sample clock to find end time
        8. End time minus start time is the simulation time for the next frame
        '''
        input_sent_time = time()
        while not self._stop_flag:
            start_time = time()

            if self.user_input is not None and \
                    start_time - input_sent_time >= 500:
                input_sent_time = time()
                cmd = UserInput(input_sent_time,
                                self._user_input,
                                self._player_id)
                self._send_input_cback(cmd)
                self._commands_to_execute.append(cmd)
                self.user_input = None

            if self.server_snapshot is not None:
                self._last_snapshot_time = self._server_snapshot.time
                self._updateStateFromSnapshot(self.server_snapshot)
                self.server_snapshot = None
            self._update_scene_cback(self._grid.tiles())

            if self._commands_to_execute:
                self._exec_commands()

            # print(time())
            frame_time = time() - start_time
            sleep_time = (50 - frame_time) / 1e3
            if sleep_time > 0:
                # print(sleep_time)
                sleep(sleep_time)
