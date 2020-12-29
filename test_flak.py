from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def index():
    if request.method == "POST":

        req = request.form.to_dict()
        print(req)

        return redirect(request.url)

    return render_template("form.html")
if __name__=="__main__":
    app.run(debug=True)