import serial
import time
import lewansoul_lx16a
import logging
from typing import List, Tuple, Callable

LS_SPEED = 500


class LSMoveProducer:

    move_sequence: List[Tuple[Callable, float]] = []

    def __init__(self, file_prefix: str, serial_port: str):
        self.file = open(file_prefix + "/ls.txt", "w")
        self.serial: serial.Serial = serial.Serial(serial_port, 115200, timeout=1)
        self.controller = lewansoul_lx16a.ServoController(serial=self.serial)
        self.servo_1 = self.controller.servo(2)
        self.servo_2 = self.controller.servo(3)
        self.servo_3 = self.controller.servo(4)
        self.servo_4 = self.controller.servo(5)
        self.servo_1.set_motor_mode(0)
        self.servo_3.set_motor_mode(0)
        self.servo_2.set_motor_mode(0)
        self.servo_4.set_motor_mode(0)
        self.stop = False
        time.sleep(1)
        self.speed = LS_SPEED
        self.move_sequence = [
            (self.move_forward, 8),
            (self.move_left, 2),
            (self.move_forward, 8),
            (self.move_left, 2),
            (self.move_forward, 8),
            (self.move_left, 2),
            (self.move_forward, 8),
            (self.move_left, 2),
            (self.move_forward, 8),
            (self.move_left, 2),
        ]

    def get_total_move_time(self) -> float:
        total_move_time: float = 0.0
        for move_command, move_time in self.move_sequence:
            total_move_time += move_time
        return total_move_time

    def move_forward(self, move_time: float):
        self.servo_1.set_motor_mode(-self.speed)
        self.servo_3.set_motor_mode(-self.speed)
        self.servo_2.set_motor_mode(self.speed)
        self.servo_4.set_motor_mode(self.speed)
        self.get_ls_data(rec_time_s=move_time)

    def move_backward(self, move_time: float):
        self.servo_1.set_motor_mode(self.speed)
        self.servo_3.set_motor_mode(self.speed)
        self.servo_2.set_motor_mode(-self.speed)
        self.servo_4.set_motor_mode(-self.speed)
        self.get_ls_data(rec_time_s=move_time)

    def move_left(self, move_time: float):
        self.servo_1.set_motor_mode(-self.speed)
        self.servo_3.set_motor_mode(-self.speed)
        self.servo_2.set_motor_mode(-self.speed)
        self.servo_4.set_motor_mode(-self.speed)
        self.get_ls_data(rec_time_s=move_time)

    def move_right(self, move_time: float):
        self.servo_1.set_motor_mode(self.speed)
        self.servo_3.set_motor_mode(self.speed)
        self.servo_2.set_motor_mode(self.speed)
        self.servo_4.set_motor_mode(self.speed)
        self.get_ls_data(rec_time_s=move_time)

    def move_stop(self):
        self.stop = True
        self.servo_1.set_motor_mode(0)
        self.servo_3.set_motor_mode(0)
        self.servo_2.set_motor_mode(0)
        self.servo_4.set_motor_mode(0)

    def get_ls_data(self, rec_time_s) -> None:
        start_time = time.time()
        while time.time() - start_time < rec_time_s:
            s1: int = self.servo_1.get_position()
            s2: int = self.servo_2.get_position()
            s3: int = self.servo_3.get_position()
            s4: int = self.servo_4.get_position()
            self.file.write(f"\"dev\" \"LS\" \"time\" {time.time()} \"s1\" {s1} \"s2\" {s2} \"s3\" {s3} \"s4\" {s4}\n")
        self.move_stop()

    def close(self):
        self.serial.close()
        self.file.close()

    def set_ls_moves(self) -> None:
        self.stop = False
        start_time = time.time()
        logging.info(f"Starting at {start_time}")
        for move_command, move_time in self.move_sequence:
            if not self.stop:
                move_command(move_time)

