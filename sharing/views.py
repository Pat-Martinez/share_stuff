# ****** Sharing Views.py ***********
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sharing.forms import UserForm, MemberForm, ItemForm, GroupForm, AcceptRequestForm
from sharing.models import Member, Group, Item, Moderator, JoinRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
	return render(request, 'sharing/index.html')


def about(request):
    return render(request, 'sharing/about.html')


def register(request):
	registered = False

	if request.method == "POST":
		print request.POST
		user_form = UserForm(data=request.POST)
		member_form = MemberForm(data=request.POST)

		if user_form.is_valid() and member_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			member = member_form.save(commit=False)
			member.user = user

			if 'profile_picture' in request.FILES:
				member.profile_picture = request.FILES['profile_picture']

			member.save()
			registered = True

		else:
			print user_form.errors, member_form.errors

	else:
		user_form = UserForm()
		member_form = MemberForm()
		
	return render(request, 'sharing/register.html', {'user_form': user_form,
				'member_form': member_form, 'registered': registered})


def sign_in(request):
	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		print request.POST

		member = authenticate(username = username, password = password)

		if member:
			if member.is_active:
				login(request, member)
				return HttpResponseRedirect('/sharing/')
			else:
                # An inactive account was used - no logging in!
				return HttpResponse("Your sharing account is disabled.")
		else:
        # Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return render(request, 'sharing/sign_in.html', {'invalid': "Invalid username or password"})
	else:
		return render(request, 'sharing/sign_in.html',)


def sign_out(request):
	logout(request)
	return HttpResponseRedirect('/sharing/')

@login_required
def add_item(request):

	# item_added = False
	context_dict = {}

	if request.method == "POST":
		item_form = ItemForm(data=request.POST)

		if item_form.is_valid():
			# (commit=False) doesn't save data to database
			item = item_form.save(commit=False)
			item.member = request.user.member
			# use item_name as boolean in template.
			context_dict['item_name'] = item.name

			if 'photo' in request.FILES:
				item.photo = request.FILES['photo']

			item.save() # saves form data to database.
			return HttpResponseRedirect('/sharing/inventory/')
		else:
			print item_form.errors

	else:
		item_form = ItemForm()

	context_dict['item_form'] = item_form
		
	return render(request, 'sharing/add_item.html', context_dict)

@login_required
def add_group(request):
	group_added = False

	if request.method == "POST":
		print request.POST
		group_form = GroupForm(data=request.POST)

		if group_form.is_valid():
			# (commit= False) doesn't save data to database 
			group = group_form.save(commit=False) 
			group.moderator = request.user.member

			if 'group_picture' in request.FILES:
				group.photo = request.FILES['group_picture']

			group.save() # saves form data to database.
			group_added = True

		else:
			print group_form.errors

	else:
		group_form = GroupForm()

	return render(request, 'sharing/add_group.html', {'group_form': group_form,
				 'group_added': group_added})

@login_required
def inventory(request):
	# Query for items.
	item_list = Item.objects.filter(member__user=request.user)
	

	context_dict = {'items': item_list,}
	return render(request, 'sharing/inventory.html', context_dict)

@login_required
def member(request):
	group_items = []
	# list of a member's items
	item_list = Item.objects.filter(member__user=request.user)
	# is the member a moderator?
	moderator = Moderator.objects.filter(member__user=request.user)
	# list of join requests for a moderator
	join_requests = JoinRequest.objects.filter(group__moderator=request.user)
	# all groups that a member belongs too
	groups = Group.objects.filter(member_list__user=request.user)
	# list of items for the group.
	for group in groups:
		# get members of this group
		group_members = group.member_list.all()
		# list of items for each member.
		for member in group_members:
			# get items for this member.
			group_items.extend(Item.objects.filter(member=member))


	context_dict = {'items': item_list, 'moderator': moderator, 'requests': join_requests,
			'groups': groups, 'group_members': group_members, 'group_items': group_items}
	return render(request, 'sharing/member.html', context_dict)

@login_required
def join_requests(request):
	join_request_list= JoinRequest.objects.filter(group__moderator__member__user=request.user)
	requests_pending = []
	requests_completed = []

	# Determine which join requests are pending or completed.
	for req in join_request_list:
		if not req.action_date: # indicates moderator hasn't accepted or rejected join request
			requests_pending.append(req)
		else: 
			requests_completed.append(req)

	# Process form with def process(request, request_id).		
	accept_request_form = AcceptRequestForm()

	context_dict = {'join_request_list': join_request_list,
			'accept_request_form': accept_request_form, 'requests_pending': requests_pending,
			'requests_completed': requests_completed}
	return render(request, 'sharing/join_requests.html', context_dict,)

@login_required
def process(request, request_id):

	if request.method == "POST":
		# confirm request exists
		join_request = get_object_or_404(JoinRequest,
				group__moderator__member__user=request.user, id=request_id)
		print request.POST
		accept_request_form = AcceptRequestForm(data=request.POST)

		if accept_request_form.is_valid():
			form = accept_request_form.save(commit = False)

			# Check for valid choices.
			if (form.accept and form.reject) or (not form.accept and not form.reject):

				# return HttpResponseRedirect('/sharing/join_requests/')
				error = "Invalid: select either accept or reject"
				return render(request, 'sharing/join_requests.html',
						{'error': error})

			join_request.action_date =  datetime.now()
			join_request.accept = form.accept
			join_request.reject = form.reject
			join_request.save()

		else:
			print accept_request_form.errors

	else:
		print "process: GET request ignored"

	return HttpResponseRedirect('/sharing/join_requests/')

@login_required
def delete_item (request, item_id): # Process to delete an item.

	item = get_object_or_404(Item, member__user=request.user, id=item_id)
	print item.name
	item.delete()
	return HttpResponseRedirect('/sharing/inventory/')