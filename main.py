from turtle import title
from flask import Flask, render_template, url_for
app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='static',
)

postlist = [
    {
        'author': 'User',
        'title': 'Some thoughts ive been keeping for a while',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus iaculis metus vel ex fringilla ornare vitae eget elit. Suspendisse efficitur congue eros, et tempus arcu. Mauris mollis, lectus et vehicula pellentesque, nibh ex rutrum lorem, ut sagittis enim odio quis nulla. Sed vehicula egestas cursus. Ut commodo eleifend condimentum. Nullam aliquam nunc imperdiet, euismod dui sed, bibendum turpis. Mauris eros est, feugiat a consequat in, lobortis eget leo. Morbi eleifend erat diam, in dapibus metus viverra vel.',
        'date': 'July 16, 2022'
    },
    {
        'author': 'User',
        'title': 'Une hirondelle ne fait pas le printemps',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus iaculis metus vel ex fringilla ornare vitae eget elit. Suspendisse efficitur congue eros, et tempus arcu. Mauris mollis, lectus et vehicula pellentesque, nibh ex rutrum lorem, ut sagittis enim odio quis nulla. Sed vehicula egestas cursus. Ut commodo eleifend condimentum. Nullam aliquam nunc imperdiet, euismod dui sed, bibendum turpis. Mauris eros est, feugiat a consequat in, lobortis eget leo. Morbi eleifend erat diam, in dapibus metus viverra vel.',
        'date': 'July 16, 2022'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('blog/home.html', posts=postlist)

@app.route("/about")
def about():
    return render_template('blog/about.html', title='About')

if __name__ == "__main__":
    app.run(debug=True)
 