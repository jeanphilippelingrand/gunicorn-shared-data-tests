import threading
import time
from multiprocessing import Lock

from flask import Flask

lock = Lock()

loaded = False
model_parent_thread_id = None


def create_app():
    app = Flask(__name__)

    def load_model():
        print('load model: started')
        global loaded
        global model_parent_thread_id
        lock.acquire()
        loaded = 'not yet'
        time.sleep(10)
        loaded = True
        model_parent_thread_id = threading.get_ident()
        lock.release()
        print('load model: done')

    @app.route("/")
    def hello():
        global loaded
        global model_parent_thread_id
        if loaded is False:
            load_model()

        return f"loaded: {loaded} - parent thread: {model_parent_thread_id} - current thread: {threading.get_ident()}"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False)
