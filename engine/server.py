import eel
from features import process_query

eel.init("../www")

@eel.expose
def send_query_to_python(query):
    """Receives query from JavaScript, processes it, and returns a response."""
    response = process_query(query)
    return response

if __name__ == "__main__":
    eel.start("index.html", size=(1000, 600))
