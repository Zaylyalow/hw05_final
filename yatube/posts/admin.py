from django.contrib import admin

from .models import Group, Post, Comment, Follow


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'group',
        'image',
        'author',
        'created',
        'count_comments',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'

    def count_comments(self, object):
        return object.comments.count()


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'post',
        'text',
        'author',
        'created',
    )
    search_fields = ('text',)
    list_filter = ('created', 'author',)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
