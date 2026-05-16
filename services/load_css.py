def load_css():

    with open("assets/style.css") as f:

        css = f.read()

    return f"<style>{css}</style>"