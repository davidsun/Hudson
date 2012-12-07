# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from sns.models.hudson_model import HudsonModel
from sns.models.post import Post


class PostTag(HudsonModel):
	VALID_TAGS = Post.VALID_TAGS

	content = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Post, related_name="tags")
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, related_name="post_tags")

	class Meta:
		app_label = 'sns'

	def clean(self):
		if (self.content in PostTag.VALID_TAGS) == False :
			raise validators.ValidationError(u'不能添加其他标签')
		objs = PostTag.objects.filter(post_id=self.post_id, user_id=self.user_id).all()
		if len(objs) > 0 and objs[0].id != self.id :
			raise validators.ValidationError(u'不能重复添加标签')



