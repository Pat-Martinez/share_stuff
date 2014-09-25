# ****** Sharing Views.py ***********
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sharing.forms import UserForm, MemberForm, ItemForm, GroupForm, AcceptRequestForm
from sharing.forms import BorrowRequestForm
from sharing.models import Member, Group, Item, Moderator, JoinRequest, BorrowRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages


def index(request):
	groups = Group.objects.all()

	context_dict = {'groups': groups, 'navbar': 'home'}
	return render(request, 'index.html', context_dict)


def about(request):
    return render(request, 'about.html', {'navbar': 'about'})


# View for someone to register as a member.
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
			messages.success(request, 'Thank you for registering!')
			return HttpResponseRedirect('/sharing/sign_in')

		else:
			print user_form.errors, member_form.errors

	else:
		user_form = UserForm()
		member_form = MemberForm()
		
	return render(request, 'register.html', {'user_form': user_form,
				'member_form': member_form, 'registered': registered, 'navbar': 'register'})


def sign_in(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		print request.POST

		member = authenticate(username = username, password = password)

		if member:
			if member.is_active:
				login(request, member)
				return HttpResponseRedirect('/sharing/member')
			else:
                # An inactive account was used - no logging in!
				return HttpResponse("Your sharing account is disabled.")
		else:
        # Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return render(request, 'sign_in.html', {'invalid': "Invalid username or password"})
	else:
		return render(request, 'sign_in.html', {'navbar': 'sign_in'})


def sign_out(request):
	logout(request)
	return HttpResponseRedirect('/sharing/')


@login_required
# View for a member to add an item to share
def add_item(request):
	item_list = Item.objects.filter(member__user=request.user)
	item_added = False
	item = []

	if request.method == "POST":
		item_form = ItemForm(data=request.POST)

		if item_form.is_valid():
			# (commit=False) doesn't save data to database
			item = item_form.save(commit=False)
			item.member = request.user.member

			if 'photo' in request.FILES:
				item.photo = request.FILES['photo']

			item.save() # saves form data to database.
			item_added = True
			messages.success(request, 'Your "%s" was added successfully.' %(item))
			return HttpResponseRedirect('/sharing/inventory/') 
		else:
			print item_form.errors

	else:
		item_form = ItemForm()

	context_dict = {'item_form': item_form, 'item': item, 'item_added': item_added,
			'items': item_list, 'navbar':'add_item'}
		
	return render(request, 'add_item.html', context_dict)


@login_required
# View for a member to add a new sharing group.
def add_group(request):
	group_added = False
	group = []

	if request.method == "POST":
		print request.POST
		group_form = GroupForm(data=request.POST)

		if group_form.is_valid():
			# (commit= False) doesn't save data to database 
			group = group_form.save(commit=False)
			group.moderator = Moderator.objects.get_or_create(member= request.user.member)[0]
			group.save()
			group.member_list.add(request.user.member)

			if 'group_picture' in request.FILES:
				group.photo = request.FILES['group_picture']

			group.save() # saves form data to database.
			group_added = True
			messages.success(request, 'You successfully added the group "%s".' %(group))
			return HttpResponseRedirect('/sharing/')
		else:
			print group_form.errors
	else:
		group_form = GroupForm()

	return render(request, 'add_group.html', {'group_form': group_form,
				'group': group, 'group_added': group_added})

@login_required
# View to show a particular members inventory of items.
def inventory(request):
	# Query for items.
	item_list = Item.objects.filter(member__user=request.user)
	context_dict = {'items': item_list,}
	return render(request, 'inventory.html', context_dict)


@login_required
# View to show info about a specific member.
def member(request):
	group_items = []
	group_members = []

	# list of a member's items
	item_list = Item.objects.filter(member__user=request.user)
	
	# is the member a moderator?
	moderator = Moderator.objects.filter(member__user=request.user)

	# list of join requests for a moderator
	join_requests = JoinRequest.objects.filter(group__moderator__member__user=request.user)
	print "JOIN REQ=  ", join_requests

	# list of borrow requests for member
	borrow_requests = BorrowRequest.objects.filter(item__member__user=request.user)
	print 'BORROW REQ= ', borrow_requests

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

	context_dict = {'items': item_list, 'moderator': moderator, 'join_requests': join_requests,
			'groups': groups, 'group_members': group_members, 'group_items': group_items,
			'borrow_requests': borrow_requests}
	return render(request, 'member.html', context_dict)


@login_required
# View for moderator to see their list of join requests submitted by members.
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

	# Process form with def join_req_process(request, borrow_id).		
	accept_request_form = AcceptRequestForm()

	context_dict = {'join_request_list': join_request_list,
			'accept_request_form': accept_request_form, 'requests_pending': requests_pending,
			'requests_completed': requests_completed}
	return render(request, 'join_requests.html', context_dict,)


@login_required
# function to process a moderator's response to a request to join their Group.
def join_req_process(request, request_id):

	if request.method == "POST":
		# confirm request exists
		join_request = get_object_or_404(JoinRequest,
				group__moderator__member__user=request.user, id=request_id)
		print request.POST
		print "join_request= ", join_request
		accept_request_form = AcceptRequestForm(data=request.POST)

		if accept_request_form.is_valid():
			form = accept_request_form.save(commit = False)

			# Check for valid choices.
			if (form.accept and form.reject) or (not form.accept and not form.reject):
				messages.error (request, 'Invalid: select either accept or reject') 
				# return HttpResponseRedirect('/sharing/join_requests/')
				error = "Invalid: select either accept or reject"
				return render(request, 'join_requests.html',
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
# Process to delete an item.
def delete_item (request, item_id):
	item = get_object_or_404(Item, member__user=request.user, id=item_id)
	item.delete()
	return HttpResponseRedirect('/sharing/inventory/')


# View to list all the available sharing groups.
def groups(request):
	groups = Group.objects.all()
	return render (request, 'groups.html', {'groups': groups})


# View to show the info for a specific group.
def group_info (request, group_id):
	group = get_object_or_404(Group, id=group_id)
	return render (request, 'group_info.html', {'group': group,})

@login_required
# View for member to see their list of people requesting to borrow an item.
def borrow_requests (request):
	borrow_request_list = BorrowRequest.objects.filter(item__member__user=request.user)
	requests_pending = []
	requests_completed = []

	print "Borrow Req List ", borrow_request_list
	# Determine which borrow requests are pending or completed.
	for req in borrow_request_list:
		if not req.action_date:
			requests_pending.append(req)
		else:
			requests_completed.append(req)

	# Process form with def borrow_req_process(request, borrow_id).
	borrow_request_form = BorrowRequestForm()

	context_dict = {'borrow_request_list': borrow_request_list,
			'requests_pending': requests_pending,
			'requests_completed': requests_completed,
			'borrow_request_form': borrow_request_form}
	return render(request, 'borrow_requests.html', context_dict)

@login_required
# function to process a member's response to borrow one of their items
def borrow_req_process(request, borrow_id):
	# confirm request exists
	if request.method == "POST":
		borrow_request = get_object_or_404(BorrowRequest,
				item__member__user=request.user, id=borrow_id)
		borrow_request_form = BorrowRequestForm(data=request.POST)
		print "borrow_request= ", borrow_request

		if borrow_request_form.is_valid():
			form = borrow_request_form.save(commit = False)

			# Check for valid choices.
			if ((form.accept_request and form.reject_request) or 
			(not form.accept_request and not form.reject_request)):
				error = "Invalid: select either accept or reject"
				return render(request, 'borrow_requests.html', {'error': error})

			borrow_request.action_date = datetime.now()
			borrow_request.accept_request = form.accept_request
			borrow_request.reject_request = form.reject_request
			borrow_request.save()
		else:
			print borrow_request_form.errors
	else:
		print "process: GET request ignored"
	return HttpResponseRedirect('/sharing/borrow_requests/')



