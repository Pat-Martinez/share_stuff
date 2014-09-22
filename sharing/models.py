from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
	user = models.OneToOneField(User)
	profile_picture = models.ImageField(upload_to='profile_images', blank=True)
	zip_code = models.CharField(max_length=5)

	def __unicode__(self):
		return "%s %s (%s)" %(self.user.first_name, self.user.last_name,
			self.user.username)

	class Meta:
		verbose_name_plural = "Members"


class Moderator(models.Model):
	member = models.ForeignKey(Member, related_name = 'moderator')

	def __unicode__(self):
		return "%s %s (%s)" %(self.member.user.first_name, self.member.user.last_name,
			self.member.user.username)

	class Meta:
		verbose_name_plural = "Moderators"


class Item(models.Model):
	name = models.CharField(max_length=30)
	category_choices = (
		('Tools', 'Tools & Gardening'),
		('Home', 'Home & Appliances'), 
		('Sports', 'Sports & Outdoors'),
		('Electronics', 'Electronics'),
		('Arts_etc', 'Arts & Crafts'),
		('Movies_etc', 'Movies, Music, & Books'),
		('Other', 'Other')
	)
	category = models.CharField(max_length=30, choices=category_choices)
	description = models.TextField()
	photo = models.ImageField(upload_to='item_images', blank=True)
	member = models.ForeignKey(Member, related_name='item_owner')
	# loaned = ????

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Items"


class Group(models.Model):
	name = models.CharField(max_length=30)
	description= models.TextField()
	moderator= models.ForeignKey(Moderator, related_name="moderator")
	member_list = models.ManyToManyField(Member, related_name='group_members', blank=True)
	item_list  = models.ManyToManyField(Item, related_name='group_items', blank=True)
	group_picture = models.ImageField(upload_to='group_images', blank=True)


	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Groups"


class JoinRequest(models.Model):
	requestor = models.ForeignKey(Member, related_name = 'requestor')
	group = models.ForeignKey(Group)
	request_date = models.DateTimeField()
	accept = models.BooleanField()
	reject = models.BooleanField()
	action_date = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return "Member: %s --- Moderator: %s" %(self.requestor.user, self.group.moderator)

	class Meta:
		verbose_name_plural = "Join Requests"
		

class BorrowRequest(models.Model):
	item = models.ForeignKey(Item, related_name = 'item')
	borrower = models.ForeignKey(Member, related_name = 'borrower')
	loaner = models.ForeignKey(Member, related_name = 'loaner')
	loan_status = models.BooleanField()
	request_date = models.DateTimeField()
	accept_request = models.BooleanField()
	reject_request = models.BooleanField()
	# Date that member (loaner) accepted or rejected request.
	action_date = models.DateTimeField(null=True, blank=True)
	
	# *** Consider adding in later versions of app ***
	# pickup_date = models.DateTimeField()
	# expected_return_date = models.DateTimeField()
	# actual_return_date = models.DateTimeField()

	def __unicode__(self):
		return "Item: %s-- Borrower: %s, Loaner: %s" %(self.item, self.borrower,
				self.loaner)
	class Meta:
		verbose_name_plural = "Borrow Requests"


