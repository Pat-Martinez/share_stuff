# ****** Sharing Views.py ***********
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sharing.forms import UserForm, MemberForm, ItemForm, GroupForm, AcceptRequestForm
from sharing.forms import BorrowRequestForm  # BorrowForm
from sharing.models import Member, Group, Item, Moderator, JoinRequest, BorrowRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.contrib import messages


@never_cache
def index(request):
	all_members = []
	item_list = []
	moderator = []
	groups = []
	group_items = []
	group_members = []
	join_requests = []
	join_requests_pending = []
	borrow_requests = []
	borrow_requests_pending = []
	items_to_borrow = []
	all_members = Member.objects.all()
	member = []

	if request.user.is_authenticated() and request.method == 'GET':
		member = Member.objects.get(user=request.user)
		
		# list of a member's items
		item_list = Item.objects.filter(member__user=request.user)
		
		# is the member a moderator?
		moderator = Moderator.objects.filter(member__user=request.user)

		# list of join requests for a moderator
		join_requests = JoinRequest.objects.filter(group__moderator__member__user=request.user)
		# Determine which join requests are pending.
		for req in join_requests:
			if not req.action_date: # indicates moderator hasn't accepted or rejected join request
				join_requests_pending.append(req)

		# list of borrow requests for member
		borrow_requests = BorrowRequest.objects.filter(item__member__user=request.user)
		# Determine which borrow requests are pending.
		for req in borrow_requests: # indicates member hasn't accepted or rejected borrow request
			if not req.action_date:
				borrow_requests_pending.append(req)

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

		#list of items available for a member to borrow.
		for item in group_items:
			if item.member.user != request.user:
				items_to_borrow.append(item)

	context_dict = {'navbar': 'home', 'member': member, 'items': item_list,
			'moderator': moderator, 'join_requests': join_requests,
			'groups': groups, 'group_members': group_members, 'group_items': group_items,
			'borrow_requests': borrow_requests, 'borrow_requests_pending':
			borrow_requests_pending, 'join_requests_pending': join_requests_pending,
			"items_to_borrow": items_to_borrow, 'all_members': all_members,}

	return render(request, 'index.html', context_dict)


def about(request):
   	# list of sample member accounts
	sample_members = Member.objects.filter(user__username__startswith = 'sample_')
	print sample_members
	context_dict = {'navbar': 'about', 'sample_members': sample_members}

	return render(request, 'about.html', context_dict)


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
	user = request.user

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
			# Bad login details were provided.
			messages.error(request, "Invalid Username or Password")
			print "Invalid login details: {0}, {1}".format(username, password)
			return render(request, 'sign_in.html',)
	else:
		return render(request, 'sign_in.html', {'navbar': 'sign_in', 'user': user})


def sign_out(request):
	logout(request)
	return HttpResponseRedirect('/sharing/')


# View for a member to add an item to share
@login_required
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
			messages.success(request, 'Your "%s" was added successfully.' %(item.name))
			return HttpResponseRedirect('/sharing/inventory/') 
		else:
			print item_form.errors

	else:
		item_form = ItemForm()

	context_dict = {'item_form': item_form, 'item': item, 'item_added': item_added,
			'items': item_list, 'navbar':'add_item'}
		
	return render(request, 'add_item.html', context_dict)


# View to show the info for a specific item.
@login_required
def item_info (request, item_id):
	item = get_object_or_404(Item, id=item_id)
	return render (request, 'item_info.html', {'item': item,})


# View for a member to add a new sharing group.
@login_required
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
			messages.success(request, 'You successfully added the group "%s".' %(group.name))
			return HttpResponseRedirect('/sharing/')
		else:
			print group_form.errors
	else:
		group_form = GroupForm()

	return render(request, 'add_group.html', {'group_form': group_form,
				'group': group, 'group_added': group_added})


# View to show a particular members inventory of items.
@login_required
def inventory(request):
	# Query for items.
	item_list = Item.objects.filter(member__user=request.user)
	context_dict = {'items': item_list,}
	return render(request, 'inventory.html', context_dict)


# View for moderator to see their list of join requests submitted by members.
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

	# Process form with def join_req_process(request, borrow_id).		
	accept_request_form = AcceptRequestForm()

	context_dict = {'join_request_list': join_request_list,
			'accept_request_form': accept_request_form, 'requests_pending': requests_pending,
			'requests_completed': requests_completed}
	return render(request, 'join_requests.html', context_dict,)


# function to process a moderator's response to a request to join their Group.
@login_required
def join_req_process(request, request_id):

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
				messages.error (request, 'Invalid: select either Accept or Reject') 
				return HttpResponseRedirect('/sharing/join_requests/')

			join_request.action_date =  datetime.now()
			join_request.accept = form.accept
			join_request.reject = form.reject
			join_request.save()
		else:
			print accept_request_form.errors
	else:
		print "process: GET request ignored"

	return HttpResponseRedirect('/sharing/join_requests/')


# Process to delete an item.
@login_required
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


# View for member to see their list of people requesting to borrow an item.
@login_required
def borrow_requests (request): # TO DO: rename to borrow_reply
	borrow_request_list = BorrowRequest.objects.filter(item__member__user=request.user)
	requests_pending = []
	requests_completed = []

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


# function to process a member's response to borrow one of their items
@login_required
def borrow_req_process(request, borrow_id): # TO DO: rename to borrow_reply_process
	# confirm request exists
	if request.method == "POST":
		borrow_request = get_object_or_404(BorrowRequest,
				item__member__user=request.user, id=borrow_id)
		borrow_request_form = BorrowRequestForm(data=request.POST)

		if borrow_request_form.is_valid():
			form = borrow_request_form.save(commit = False)

			# Check for valid choices.
			if ((form.accept_request and form.reject_request) or 
			(not form.accept_request and not form.reject_request)):
				messages.error (request, 'Invalid: select either Accept or Reject') 
				return HttpResponseRedirect('/sharing/borrow_requests/')

			borrow_request.action_date = datetime.now()
			borrow_request.accept_request = form.accept_request
			borrow_request.reject_request = form.reject_request
			borrow_request.save()
		else:
			print borrow_request_form.errors
	else:
		print "process: GET request ignored"
	return HttpResponseRedirect('/sharing/borrow_requests/')


# View for member to see a list of items that they've requested to borrow.
@login_required
def borrow_req_borrower (request): # TO DO: rename to borrow_requests
	borrow_request_list = BorrowRequest.objects.filter(item__member__user=request.user)


# function to process a member's request to borrow an item.
@login_required
def borrow_req_borrower_process (request, borrow_id): # TO DO: rename to borrow_process
	if request.method == "POST":
		borrow_request = get_object_or_404(BorrowRequest,
				item__member__user=request.user, id=borrow_id)
		borrow_request_form = BorrowRequestForm(data=request.POST)
		print "borrow_request= ", borrow_request


# View to explain features that are in development.
def under_construction (request):
	return render (request, 'under_construction.html',)
