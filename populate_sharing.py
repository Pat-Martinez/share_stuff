import os

# Populates database with data for-
#   User (username, first_name, last_name, email, password,)
#   Member (profile_picture, zip_code)
#   Item (member, name, category, description, photo)

def populate():
    # add sample member with two items
    user_1 = add_user('sample_1', 'Bruno', 'Sample', 'test1@gmail.com', 'letstrythis')
    member_1 = add_member(user_1, 'Blank', '97210')
    add_item(member_1, 'Croquet Set', 'Sports', 'The best croquest set ever! Really!', 
            'item_images/croquet.jpg')
    add_item(member_1, 'Flux Capacitor', 'Electronics', 'Use at your own risk!', 
        'item_images/flux_capacitor.jpg')

    # add sample member with two items
    user_4 = add_user('sample_2', 'Ursula', 'Sample', 'test1@gmail.com', 'letstrythis')
    member_4 = add_member(user_4, 'Blank', '97210')
    add_item(member_4, '5 Gallon Stock Pot', 'Home', "Good quality, stainless steel, doesn't have a lid", 
            'item_images/stockpot.jpeg')
    add_item(member_4, 'Karaoke Machine', 'Electronics', 'works OK', 
            'item_images/karaoke.jpg')

    # add sample member with one item
    user_6 = add_user('sample_3', 'Zeus', 'Sample', 'test1@gmail.com', 'letstrythis')
    member_6 = add_member(user_6, 'Blank', '97210')
    add_item(member_6, 'Cordless Drill', 'Tools', 'Comes with two batteries', 
            'item_images/drill.jpeg')

    # add member with two items
    user_2 = add_user('Sean1', 'Sean', 'Johnson', 'test1@gmail.com', 'letstrythis')
    member_2 = add_member(user_2, 'Blank', '97210')
    add_item(member_2, 'Snow Shoes', 'Sports', 'Easy to use.', 
            'item_images/snowshoes.jpg')

    add_item(member_2, 'Juicer', 'Kitchen', 'Omega brand, quite and reliable.', 
            'item_images/juicer.jpeg')

    # add member with no items
    user_3 = add_user('Sally1', 'Sally', 'Smith', 'test1@gmail.com', 'letstrythis')
    member_3 = add_member(user_3, 'Blank', '97210')


    # add member with one item
    user_5 = add_user('Elle1', 'Elle', 'Brown', 'test1@gmail.com', 'letstrythis')
    member_5 = add_member(user_5, 'Blank', '97210')
    add_item(member_5, 'Cuisinart', 'Kitchen', 'Works great!', 
            'item_images/cuisinart.jpeg')

    # add member with one item
    user_7 = add_user('Aphrodite1', 'Aphrodite', 'Odell', 'test1@gmail.com', 'letstrythis')
    member_7 = add_member(user_7, 'Blank', '97210')
    add_item(member_7, 'Harp', 'Other', 'Needs tuning', 'Blank')

    # add member with one item
    user_8 = add_user('zenmaster', 'Jeremy', 'Simantel', 'test1@gmail.com', 'letstrythis')
    member_8 = add_member(user_8, 'Blank', '97210')
    add_item(member_8, 'backpacking stove', 'Sports', 
        "Works great! I bought a jet boil so I rarely use this stove.",
        'item_images/backpacking_stove.jpg')

    # add member with one item
    user_9 = add_user('martinej123', 'Pat', 'Martinez', 'test1@gmail.com', 'letstrythis')
    member_9 = add_member(user_9, 'Blank', '97210')
    add_item(member_9, 'backpacking tent', 'Sports', 'Great for one person, and a little tight for two', 
            'item_images/backpacking_tent.jpg')


    # add group 
    moderator_1 = add_moderator(member_1)
    group_1 = add_group(moderator_1, 'West Side Coders', "The Best Group Ever!",
        'group_images/west_side_coders.jpg')

    # add group 
    moderator_2 = add_moderator(member_7)
    group_2 = add_group(moderator_2, 'Nordic Club', "No we're the Best Group Ever",
        'group_images/nordic_club.png')

    # add group 
    moderator_3 = add_moderator(member_9)
    group_3 = add_group(moderator_3, "Pat's Friends", "We're just an average Group.",
        'group_images/pats_group.jpg')


    for i in Item.objects.all():
        print "- {0}".format(str(i))

    for m in Member.objects.all():
        print "- {0}".format(str(m))

    for m in Moderator.objects.all():
        print "- {0}".format(str(m))

    for g in Group.objects.all():
        print "- {0}".format(str(g))

# ********group.member.add()*************


def add_item(member, name, cat, description, photo):

    i = Item.objects.get_or_create(
                member=member,
                name=name,
                category=cat,
                description=description,
                photo=photo)[0]
    return i


def add_user(username, first, last, email, passw): 
    u = User.objects.get_or_create(username=username,
                first_name=first,
                last_name=last,
                email=email,
                password=passw)[0]
    u.set_password(u.password)
    u.save()

    return u

def add_member(user, pic, zip):
    m = Member.objects.get_or_create(user=user, profile_picture=pic,
                zip_code=zip)[0]
    return m

def add_moderator(member):
    mod = Moderator.objects.get_or_create(member=member)[0]
    return mod

def add_group(moderator, name, description, pic):
    g = Group.objects.get_or_create(moderator=moderator, name=name,
                description=description, group_picture=pic)[0]
    g.member_list.add(moderator.member)
    return g


if __name__ == '__main__':
    print "Starting Sharing population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'share_stuff.settings')
    from sharing.models import Item, Member, Group, Moderator
    from django.contrib.auth.models import User


    populate()

