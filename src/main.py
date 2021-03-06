from flask import Flask
from src.move import LSMoveProducer
from threading import Thread

LS_SERIAL_PORT = "/dev/ttyUSB0"
ls = LSMoveProducer(file_prefix="/tmp/", serial_port=LS_SERIAL_PORT)

app = Flask(__name__)

form = """
<html>
<body>
  <h1>Mars Rover</h1>
  <form action="/run" method="post">
    <p>
      <br>
      <input style="width:150px; height:150px;" type="submit" value="Drive">
    </p>
  </form>
  <form action="/stop" method="post">
    <p>
      <br>
      <input style="width:150px; height:150px;" type="submit" value="Stop">
    </p>
  </form>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def hello_world_get():
    return form


@app.route('/run', methods=['POST'])
def hello_world_run():
    thread = Thread(target=ls.set_ls_moves)
    thread.start()
    return form


@app.route('/stop', methods=['POST'])
def hello_world_stop():
    ls = LSMoveProducer(file_prefix="/tmp/", serial_port=LS_SERIAL_PORT)
    return form


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
