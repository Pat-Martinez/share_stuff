from django import forms
from sharing.models import Member, Item, Group, JoinRequest, BorrowRequest
from django.contrib.auth.models import User

# Part 1 of 2 of the new member registration form.
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	username = forms.CharField(widget=forms.TextInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')


# Part 2 of 2 of the new member registration form.
class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ('zip_code','profile_picture',)


# Add item form
class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		widgets = {'description': forms.Textarea(attrs={'rows':8, 'cols':22}),
		}

		fields = ('name', 'category', 'description', 'photo')


# Add group form
class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ('name', 'description', 'group_picture')


# Form for moderator to accept or reject a request to join his/her group.
class AcceptRequestForm(forms.ModelForm):
	class Meta:
		model = JoinRequest
		fields = ('accept', 'reject')

# Form for a member to accept or reject a request to borrow an item.
class BorrowRequestForm(forms.ModelForm): #TO DO: rename to BorrowReplyForm
	class Meta:
		model = BorrowRequest
		fields = ('accept_request', 'reject_request')

# Form for a member to request to borrow an item.
# class BorrowForm(forms.ModelForm): 
# 	class Meta:
# 		model = BorrowRequest
# 		fields = ('request_date')



	
