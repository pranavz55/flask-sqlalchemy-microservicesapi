from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# To instantiate the app
app = Flask(__name__)

#
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/mydemo1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db=SQLAlchemy(app)
ma=Marshmallow(app)


class Post(db.Model):
	#__table_args__ = {}
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(20))
	content=db.Column(db.String(20))

	

	def __repr__(self):
		return '<Post %s>' % self.title

class PostSchema(ma.Schema):
	class Meta:
		fields=("id","title","content")

post_schema=PostSchema()
posts_schema=PostSchema(many=True)

@app.route('/posts',methods=['GET'])
def get_allposts():
	posts=Post.query.all()
	return jsonify(posts_schema.dump(posts))


@app.route('/addpost',methods=['POST'])
def add_post():
	new_post=Post(title=request.json['title'],content=request.json['content'])
	
	db.session.add(new_post)
	db.session.commit()
	id=new_post.id
	return 'Post with id='+str(id)+' created'


@app.route('/viewid/<int:post_id>',methods=['GET'])
def get_post(post_id):
	post=Post.query.get_or_404(post_id)
	return post_schema.dump(post)

@app.route('/deletepost/<int:post_id>',methods=['DELETE'])
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	return 'Post deleted Successfully'


@app.route('/updatepost/<int:post_id>',methods=['PUT'])
def update_post(post_id):
	post=Post.query.get_or_404(post_id)
	if 'title' in request.json:
		post.title=request.json['title']
	if 'content' in request.json:
		post.content=request.json['content']
	
	db.session.commit()
	return 'Post Updated Successfully'




if __name__=='__main__':
	app.run(debug=True)
