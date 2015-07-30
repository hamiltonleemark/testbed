"""
 Admin interface to test models.
"""
from django.contrib import admin

# Register your models here.
from . import models


class ContextAdmin(admin.ModelAdmin):
    """ View test context content. """
    model = models.Context


class KeyAdmin(admin.ModelAdmin):
    """ View key. """
    model = models.Key


class TestKeyAdmin(admin.ModelAdmin):
    """ View Test Key. """
    model = models.TestKey


class TestAdmin(admin.ModelAdmin):
    """ Show test. """
    model = models.Test


class TestsuiteNameAdmin(admin.ModelAdmin):
    """ Show testsuite name. """
    model = models.TestsuiteName


class TestInlineAdmin(admin.TabularInline):
    """ Show tests inline. """
    model = models.Test
    extra = 0


class TestsuiteFileInlineAdmin(admin.TabularInline):
    """ Show files associated to testsuite inline. """
    model = models.TestsuiteFile
    extra = 0


class TestsuiteKeySetInlineAdmin(admin.TabularInline):
    """ Show set of keys that associate a testsuite. """
    model = models.TestsuiteKeySet
    extra = 0


class TestsuiteAdmin(admin.ModelAdmin):
    """ Show testsuite. """
    list_display = ("context", "name", "timestamp")
    date_hierarchy = "timestamp"
    search_fields = ("context", "name", "timestamp")
    inlines = [TestsuiteKeySetInlineAdmin, TestsuiteFileInlineAdmin,
               TestInlineAdmin]

admin.site.register(models.Context, ContextAdmin)
admin.site.register(models.Key, KeyAdmin)
admin.site.register(models.Test, TestAdmin)
admin.site.register(models.TestKey, TestKeyAdmin)
admin.site.register(models.TestsuiteName, TestsuiteNameAdmin)
admin.site.register(models.Testsuite, TestsuiteAdmin)
