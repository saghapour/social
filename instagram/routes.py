from flask import Blueprint, render_template, request
from instagram.lib.instagram_profile import InstagramProfile


instagram = Blueprint('instagram', __name__)


@instagram.route('/new_insta_influencer', methods=['GET', 'POST'])
def new_instagram_influencer():
    if request.method == 'GET':
        return render_template('instagram/new_influencer.html')
    elif request.method == 'POST':
        username = request.form['username']
        profile = InstagramProfile()
        result = profile.add_profile(username, return_object=True)
        return render_template('instagram/new_influencer_result.html', result=result)