from django.contrib import admin
from sharing.models import Member, Group, Item, Moderator, JoinRequest, BorrowItem

# Register your models here.

admin.site.register(Member)
admin.site.register(Group)
admin.site.register(Item)
admin.site.register(Moderator)
admin.site.register(JoinRequest)
admin.site.register (BorrowItem)
