from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from flask_login.utils import login_required
from .models import User, Post, Comment
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def welcome():
    return render_template("welcome_page.html", user=current_user)

@views.route('/archive')
def archive():
    posts = Post.query.all()
    return render_template('archive.html', user=current_user, posts=posts)

@views.route('/archive/<id>', methods=['GET','POST'])
def post(id):
    if request.method == 'POST':
        # if a user isnt logged in they can't comment
        if not current_user.is_authenticated:
            flash('Must be logged in to make a comment.', category='error')
        else:
            comment = request.form.get('comment')
            
            # comments can't be empty
            if not comment:
                flash('Comment can\'t be empty.', category='error')
            else:
                # add commment to database
                new_comment = Comment(data=comment, post_id=id, user_name=current_user.username)
                db.session.add(new_comment)
                db.session.commit()
                flash('Comment posted.', category='success')
                return redirect('/archive/' + id)

    post = Post.query.filter_by(id=id).first()
    # check if the post requested is the most recent one
    posts = Post.query.all()
    most_recent_post = (post.id == len(posts))
    # get all the comments in this post
    comments = Comment.query.filter_by(post_id=id).all()

    return render_template('blog_post.html', comments=comments, user=current_user, post=post, most_recent_post=most_recent_post)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/new-post', methods=['GET','POST'])
@login_required
def new_post():
    if current_user.username != 'Docas95':
        return redirect(url_for('views.welcome'))

    if request.method == 'POST':
        # get the title and content of the new post
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title:
            flash('Title can\'t be empty.', category='error')
        elif not content:
            flash('Content can\'t be empty.', category='error')
        # add post to database
        else:
            new_post = Post(title=title, data=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post made with success!', category='success')
            return redirect(url_for('views.archive'))

    return render_template('create_post.html', user=current_user)

@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    # get the post to be deleted
    post = Post.query.filter_by(id=id).first()

    # check if the post exists
    if not post:
        flash('Post does not exist.', category='error')
    # check if the user has permission to delete the post
    elif current_user.id != post.user_id:
        flash('You do not have permission to delete this post.', category='error')
    # delete the post from the database
    else:
        post_id = post.id

        # delete all the comments associated with the post
        post_comments = Comment.query.filter_by(post_id=post_id).all()
        for comment in post_comments:
            db.session.delete(comment)
            db.session.commit()
        
        db.session.delete(post)
        db.session.commit()
        
        posts = Post.query.all()
        if posts:
            for post in posts:
                if post.id > post_id:
                    post.id -= 1
                    db.session.commit()

        flash('Post deleted successfully.', category='success')
    
    return redirect(url_for('views.archive'))

@views.route('/delete-comment/<id>')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()

    # check if comment exists
    if not comment:
        flash('Comment does not exist.', category='error')
        return redirect(url_for('views.archive'))
    # users can only delete comments they posted
    elif current_user.username != comment.user_name:
        flash('You do not have permission to delete this comment.', category='error')
        return redirect(url_for('views.archive'))
    else:
        db.session.delete(comment)
        db.session.commit()
        return redirect('/archive/' + str(comment.post_id))

